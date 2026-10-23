"""Validate the synthetic report, reusable plots, documentation, and PNG exports."""

from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import numpy as np
import pandas as pd
from PIL import Image

EPISODE = Path(__file__).resolve().parents[1]
SOURCE = EPISODE / "source-code"
sys.path.insert(0, str(SOURCE))

from service_data import load_jobs, validate_jobs, summarize_jobs, HOURS, SERVICE_ORDER, SERVICE_COLORS, WAIT_BINS
from service_plots import plot_wait_distribution, plot_service_time
from service_report import build_dashboard, build_individual_figures, summary_note


def python_blocks(path):
    return re.findall(r"~~~python\s*\n(.*?)\n~~~", path.read_text(encoding="utf-8"), re.S)


class LessonTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_data_schema_counts_and_independent_copies(self):
        jobs = load_jobs()
        self.assertEqual(jobs.shape, (24, 5))
        self.assertEqual(list(jobs), ["job_id", "hour", "service_type", "wait_min", "service_min"])
        self.assertEqual(jobs["service_type"].value_counts().tolist(), [8, 8, 8])
        validate_jobs(jobs)
        jobs.loc[0, "wait_min"] = 999
        self.assertEqual(load_jobs().loc[0, "wait_min"], 5)

    def test_validator_rejects_empty_missing_and_duplicate_jobs(self):
        cases = [load_jobs().iloc[:0], load_jobs().drop(columns="hour")]
        missing = load_jobs()
        missing.loc[0, "service_type"] = None
        cases.append(missing)
        duplicate = load_jobs()
        duplicate.loc[1, "job_id"] = duplicate.loc[0, "job_id"]
        cases.append(duplicate)
        for jobs in cases:
            with self.subTest(shape=jobs.shape), self.assertRaises(ValueError):
                validate_jobs(jobs)

    def test_validator_rejects_invalid_numeric_and_category_values(self):
        cases = [("hour", 8.5), ("hour", 16), ("wait_min", -1), ("wait_min", np.inf),
                 ("service_min", 0), ("service_min", np.nan), ("service_type", "Unknown")]
        for column, value in cases:
            jobs = load_jobs()
            if column != "service_type":
                jobs[column] = jobs[column].astype(float)
            jobs.loc[0, column] = value
            with self.subTest(column=column, value=value), self.assertRaises(ValueError):
                validate_jobs(jobs)
        strings = load_jobs().astype({"wait_min": str})
        with self.assertRaisesRegex(ValueError, "numeric"):
            validate_jobs(strings)

    def test_summaries_and_exercise_medians(self):
        jobs = load_jobs()
        hourly, means = summarize_jobs(jobs)
        self.assertEqual(list(hourly.index), HOURS)
        np.testing.assert_array_equal(hourly, [2, 3, 4, 3, 4, 3, 2, 3])
        self.assertEqual(hourly.sum(), len(jobs))
        self.assertEqual(list(means.index), SERVICE_ORDER)
        np.testing.assert_allclose(means, [26, 41, 61])
        medians = jobs.groupby("service_type")["service_min"].median().reindex(SERVICE_ORDER)
        np.testing.assert_allclose(medians, [25, 40, 60])
        self.assertEqual(hourly[hourly == hourly.max()].index.tolist(), [10, 12])

    def test_zero_count_is_not_a_zero_mean(self):
        jobs = load_jobs()
        without_hour = jobs.loc[jobs["hour"] != 11]
        hourly, _ = summarize_jobs(without_hour)
        self.assertEqual(hourly.loc[11], 0)
        self.assertEqual(hourly.sum(), 21)
        self.assertIn("9/21", summary_note(without_hour))
        without_type = jobs.loc[jobs["service_type"] != "Tire service"]
        _, means = summarize_jobs(without_type)
        self.assertTrue(pd.isna(means.loc["Tire service"]))
        fig, ax = plt.subplots()
        plot_service_time(ax, means)
        np.testing.assert_allclose([bar.get_width() for bar in ax.patches], [26, 41])

    def test_strict_wait_threshold_and_mean(self):
        jobs = load_jobs()
        self.assertEqual(jobs["wait_min"].mean(), 21.375)
        self.assertEqual((jobs["wait_min"] > 20).sum(), 12)
        self.assertEqual((jobs["wait_min"] >= 20).sum(), 13)
        self.assertEqual((jobs["wait_min"] > 30).sum(), 4)
        self.assertEqual((jobs["wait_min"] >= 30).sum(), 6)
        self.assertIn("Mean wait: 21.4 min", summary_note(jobs))
        self.assertIn("Wait > 30 min: 4/24", summary_note(jobs, 30))

    def test_hourly_line_data_and_tick_labels(self):
        ax = build_dashboard().axes[0]
        np.testing.assert_array_equal(ax.lines[0].get_xdata(), HOURS)
        np.testing.assert_array_equal(ax.lines[0].get_ydata(), [2, 3, 4, 3, 4, 3, 2, 3])
        ax.figure.canvas.draw()
        self.assertEqual([text.get_text() for text in ax.get_xticklabels()],
                         [f"{hour:02d}:00" for hour in HOURS])

    def test_bar_values_colors_and_zero_baseline(self):
        ax = build_dashboard().axes[1]
        np.testing.assert_allclose([bar.get_width() for bar in ax.patches], [26, 41, 61])
        np.testing.assert_allclose([bar.get_facecolor() for bar in ax.patches],
                                   [to_rgba(SERVICE_COLORS[name]) for name in SERVICE_ORDER])
        self.assertEqual([text.get_text() for text in ax.texts], ["26.0", "41.0", "61.0"])
        self.assertTrue(ax.yaxis_inverted())
        self.assertEqual(ax.get_xlim()[0], 0)

    def test_histogram_bins_counts_and_reference(self):
        ax = build_dashboard().axes[2]
        np.testing.assert_allclose([bar.get_x() for bar in ax.patches], WAIT_BINS[:-1])
        np.testing.assert_allclose([bar.get_height() for bar in ax.patches], [3, 8, 7, 5, 1])
        np.testing.assert_allclose(ax.lines[0].get_xdata(), [20, 20])
        self.assertEqual(sum(bar.get_height() for bar in ax.patches), 24)

    def test_histogram_rejects_silent_data_loss(self):
        jobs = load_jobs()
        jobs.loc[0, "wait_min"] = 55
        validate_jobs(jobs)  # A valid duration can still exceed the chosen plotting bins.
        fig, ax = plt.subplots()
        with self.assertRaisesRegex(ValueError, "WAIT_BINS"):
            plot_wait_distribution(ax, jobs)
        jobs.loc[0, "wait_min"] = 50
        plot_wait_distribution(ax, jobs)
        self.assertEqual(sum(bar.get_height() for bar in ax.patches), 24)

    def test_scatter_uses_all_rows_and_consistent_colors(self):
        jobs = load_jobs()
        ax = build_dashboard().axes[3]
        np.testing.assert_allclose(ax.collections[0].get_offsets(), jobs[["hour", "wait_min"]])
        np.testing.assert_allclose(ax.collections[0].get_facecolors(),
                                   [to_rgba(SERVICE_COLORS[name]) for name in jobs["service_type"]])
        self.assertEqual([text.get_text() for text in ax.get_legend().get_texts()],
                         SERVICE_ORDER + ["Example target: 20 min"])

    def test_annotation_points_to_the_longest_wait(self):
        ax = build_dashboard().axes[3]
        annotation = ax.texts[0]
        self.assertEqual(annotation.get_text(), "J15: 45 min")
        self.assertEqual(annotation.xy, (12, 45))
        self.assertEqual(annotation.xycoords, "data")
        self.assertEqual(annotation.get_anncoords(), "offset points")
        self.assertEqual(annotation.get_position(), (0, 12))

    def test_target_change_updates_both_lines_and_summary(self):
        fig = build_dashboard(wait_target=30)
        reference_lines = []
        for ax in fig.axes[2:]:
            # Seaborn also adds empty Line2D objects for category legend entries.
            matches = [line for line in ax.lines if line.get_label() == "Example target: 30 min"]
            self.assertEqual(len(matches), 1)
            reference_lines.append(matches[0])
        np.testing.assert_allclose(reference_lines[0].get_xdata(), [30, 30])
        np.testing.assert_allclose(reference_lines[1].get_ydata(), [30, 30])
        self.assertTrue(any("Wait > 30 min: 4/24" in text.get_text() for text in fig.texts))
        for ax in fig.axes[2:]:
            self.assertIn("Example target: 30 min", [t.get_text() for t in ax.get_legend().get_texts()])
        for bad in [-1, np.nan, np.inf]:
            with self.subTest(target=bad), self.assertRaises(ValueError):
                build_dashboard(wait_target=bad)

    def test_dashboard_has_independent_axes_and_no_mutation(self):
        jobs = load_jobs()
        before = jobs.copy(deep=True)
        with plt.rc_context({"axes.facecolor": "pink", "font.size": 15}):
            style_before = dict(plt.rcParams)
            fig = build_dashboard(jobs)
            self.assertEqual(dict(plt.rcParams), style_before)
        pd.testing.assert_frame_equal(jobs, before)
        self.assertEqual(len(fig.axes), 4)
        np.testing.assert_allclose(fig.get_size_inches(), [12, 8])
        for ax in fig.axes[1:]:
            self.assertFalse(fig.axes[0].get_shared_x_axes().joined(fig.axes[0], ax))
            self.assertFalse(fig.axes[0].get_shared_y_axes().joined(fig.axes[0], ax))

    def test_all_five_figures_have_unclipped_labels(self):
        figures = build_individual_figures()
        self.assertEqual(len(figures), 4)
        figures["dashboard"] = build_dashboard()
        for name, fig in figures.items():
            with self.subTest(figure=name):
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                width, height = fig.canvas.get_width_height()
                artists = list(fig.texts)
                for ax in fig.axes:
                    artists += [ax.title, ax.xaxis.label, ax.yaxis.label] + list(ax.texts)
                    for axis, limits in [(ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())]:
                        lower, upper = sorted(limits)
                        for tick in axis.get_major_ticks():
                            if lower <= tick.get_loc() <= upper:
                                artists += [tick.label1, tick.label2]
                    if ax.get_legend() is not None:
                        artists.append(ax.get_legend())
                for artist in artists:
                    if not artist.get_visible() or (hasattr(artist, "get_text") and not artist.get_text()):
                        continue
                    box = artist.get_window_extent(renderer)
                    self.assertGreaterEqual(box.x0, -2, str(artist))
                    self.assertGreaterEqual(box.y0, -2, str(artist))
                    self.assertLessEqual(box.x1, width + 2, str(artist))
                    self.assertLessEqual(box.y1, height + 2, str(artist))

    def test_readme_code_runs_in_order_and_matches_source(self):
        blocks = python_blocks(EPISODE / "README.md")
        self.assertEqual(len(blocks), 9)
        namespace = {"__name__": "__lesson__"}
        original_cwd = Path.cwd()

        def draw_and_close(*args, **kwargs):
            for number in plt.get_fignums():
                plt.figure(number).canvas.draw()
            plt.close("all")

        with tempfile.TemporaryDirectory() as tmp, plt.rc_context():
            try:
                os.chdir(tmp)
                with patch.object(plt, "show", side_effect=draw_and_close), redirect_stdout(io.StringIO()):
                    for number, block in enumerate(blocks, 1):
                        exec(compile(block, f"README block {number}", "exec"), namespace)
                pd.testing.assert_frame_equal(namespace["jobs"], load_jobs())
                hourly, means = summarize_jobs(load_jobs())
                pd.testing.assert_series_equal(namespace["hourly_jobs"], hourly)
                pd.testing.assert_series_equal(namespace["mean_service"], means)
                self.assertEqual(namespace["over_target"], 12)
                self.assertEqual(len(namespace["fig"].axes), 4)
                np.testing.assert_allclose(namespace["fig"].axes[1].containers[0].datavalues, means)
                self.assertEqual(namespace["fig"].axes[3].texts[0].xy, (12, 45))
                with Image.open(Path(tmp) / "output" / "service-center-report.png") as image:
                    self.assertEqual(image.size, (1800, 1200))
                    image.verify()
            finally:
                os.chdir(original_cwd)

    def test_exercise_copy_does_not_change_original(self):
        namespace = {"jobs": load_jobs()}
        for block in python_blocks(EPISODE / "exercises" / "exercise01.md"):
            exec(block, namespace)
        self.assertEqual(namespace["jobs"].loc[0, "wait_min"], 5)
        self.assertEqual(namespace["jobs_bad"].loc[0, "wait_min"], -5)
        with self.assertRaises(ValueError):
            validate_jobs(namespace["jobs_bad"])
        self.assertEqual(np.histogram(load_jobs()["wait_min"], list(range(0, 51, 5)))[0].sum(), 24)

    def test_documents_have_numbered_topics_and_existing_local_assets(self):
        readme = (EPISODE / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (\d+)\.", readme, re.M), [str(n) for n in range(1, 11)])
        for path in [EPISODE / "README.md", EPISODE / "exercises" / "exercise01.md"]:
            content = path.read_text(encoding="utf-8")
            self.assertEqual(content.count("<details>"), content.count("</details>"))
            self.assertNotRegex(content, r"บทพูด|ผู้สอน|ผู้ชม|ไม่ต้องพูด|พูดพร้อมกัน|เน้นตอนสอน")
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if target.startswith(("./", "../")):
                    resolved = (path.parent / target).resolve()
                    if resolved.is_relative_to(EPISODE):
                        self.assertTrue(resolved.is_file(), str(resolved))

    def test_report_cli_from_root_source_and_unrelated_directory(self):
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        script = SOURCE / "service_report.py"
        for cwd in [EPISODE.parent, SOURCE]:
            with self.subTest(cwd=cwd):
                result = subprocess.run([sys.executable, "-B", str(script), "--no-show"],
                                        cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Wait > 20 min: 12/24", result.stdout)
        with tempfile.TemporaryDirectory() as tmp:
            relative = Path("nested") / "exports" / "target30.png"
            result = subprocess.run([sys.executable, "-B", str(script), "--wait-target", "30",
                                     "--output", str(relative), "--no-show"], cwd=tmp, env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Wait > 30 min: 4/24", result.stdout)
            with Image.open(Path(tmp) / relative) as image:
                self.assertEqual(image.size, (1800, 1200))
                image.verify()

    def test_generator_outputs_five_png_files(self):
        expected = {"hourly-intake.png", "mean-service-time.png", "wait-distribution.png",
                    "wait-by-hour.png", "service-center-dashboard.png"}
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "plots"
            result = subprocess.run([sys.executable, "-B", str(SOURCE / "generate_lesson_figures.py"),
                                     "--output-dir", str(output)], cwd=tmp, env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path.name for path in output.iterdir()}, expected)
            for path in output.glob("*.png"):
                with Image.open(path) as image:
                    target_size = (1800, 1200) if "dashboard" in path.name else (1200, 720)
                    self.assertEqual(image.size, target_size)
                    image.verify()
        self.assertEqual({p.name for p in (EPISODE / "assets" / "plots").glob("*.png")}, expected)


if __name__ == "__main__":
    unittest.main()
