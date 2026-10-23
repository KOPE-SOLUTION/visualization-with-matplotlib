"""Check data, plotted summaries, README examples, and off-screen exports."""

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
import seaborn as sns

EPISODE = Path(__file__).resolve().parents[1]
SOURCE = EPISODE / "source-code"
sys.path.insert(0, str(SOURCE))

from housekeeping_data import load_jobs
from plot_helpers import ROOM_ORDER, PERIOD_ORDER, PALETTE, TIME_BINS, lesson_theme
from relationships import build_scatter_comparison, build_facets
from distributions import build_figure as build_distribution
from category_comparison import build_figure as build_categories
from summary_heatmap import build_figure as build_heatmap, make_summary
from optional_views import build_patterns, build_pairs


def python_blocks(path):
    return re.findall(r"~~~python\s*\n(.*?)\n~~~", path.read_text(encoding="utf-8"), re.S)


def scatter_points(ax):
    groups = [collection.get_offsets() for collection in ax.collections
              if hasattr(collection, "get_offsets") and len(collection.get_offsets())]
    return np.concatenate(groups) if groups else np.empty((0, 2))


class LessonTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_data_schema_and_balanced_groups(self):
        jobs = load_jobs()
        self.assertEqual(jobs.shape, (18, 4))
        self.assertEqual(list(jobs), ["room_type", "period", "area_m2", "cleaning_min"])
        self.assertFalse(jobs.isna().any().any())
        numeric = jobs[["area_m2", "cleaning_min"]].to_numpy()
        self.assertTrue(np.isfinite(numeric).all())
        self.assertTrue((numeric > 0).all())
        self.assertEqual(jobs.groupby("room_type").size().tolist(), [6, 6, 6])
        self.assertEqual(jobs.groupby("period").size().tolist(), [9, 9])
        self.assertTrue((jobs.groupby(["room_type", "period"]).size() == 3).all())

    def test_data_loader_returns_independent_frames(self):
        jobs = load_jobs()
        jobs.loc[0, "cleaning_min"] = -99
        self.assertEqual(load_jobs().loc[0, "cleaning_min"], 22)

    def test_means_medians_and_boxplot_assumptions(self):
        grouped = load_jobs().groupby("room_type")["cleaning_min"]
        np.testing.assert_allclose(grouped.mean().reindex(ROOM_ORDER), [26, 34, 46.5])
        np.testing.assert_allclose(grouped.median().reindex(ROOM_ORDER), [25.5, 33.5, 45.5])
        for _, values in grouped:
            self.assertTrue(values.is_unique)
            q1, q3 = values.quantile([0.25, 0.75])
            self.assertTrue(values.between(q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)).all())

    def test_scatter_positions_and_category_colors(self):
        fig = build_scatter_comparison()
        jobs = load_jobs()
        expected = jobs[["area_m2", "cleaning_min"]].to_numpy()
        for ax in fig.axes:
            np.testing.assert_allclose(scatter_points(ax), expected)
        expected_colors = [to_rgba(PALETTE[name]) for name in jobs["room_type"]]
        np.testing.assert_allclose(fig.axes[1].collections[0].get_facecolors(), expected_colors)
        self.assertEqual([t.get_text() for t in fig.axes[1].get_legend().get_texts()], ROOM_ORDER)

    def test_histogram_bin_edges_and_total(self):
        ax = build_distribution().axes[0]
        bars = ax.patches
        np.testing.assert_allclose([bar.get_x() for bar in bars], TIME_BINS[:-1])
        np.testing.assert_allclose([bar.get_width() for bar in bars], [5] * 7)
        np.testing.assert_allclose([bar.get_height() for bar in bars], [2, 3, 5, 2, 2, 2, 2])
        self.assertEqual(sum(bar.get_height() for bar in bars), 18)

    def test_category_dots_and_mean_bar_heights(self):
        box_ax, mean_ax = build_categories().axes
        jobs = load_jobs()
        expected = np.column_stack([
            np.repeat(np.arange(3), 6), jobs["cleaning_min"].to_numpy(),
        ])
        np.testing.assert_allclose(scatter_points(box_ax), expected)
        np.testing.assert_allclose([bar.get_height() for bar in mean_ax.patches], [26, 34, 46.5])
        self.assertEqual([text.get_text() for text in mean_ax.texts], ["26.0", "34.0", "46.5"])
        self.assertEqual(mean_ax.get_ylim()[0], 0)

    def test_facets_filter_data_and_keep_colors_and_scales(self):
        g = build_facets()
        self.assertIsInstance(g, sns.FacetGrid)
        self.assertEqual(g.axes.shape, (1, 2))
        jobs = load_jobs()
        for ax, period in zip(g.axes.flat, PERIOD_ORDER):
            subset = jobs.loc[jobs["period"] == period]
            np.testing.assert_allclose(scatter_points(ax), subset[["area_m2", "cleaning_min"]])
            colors = [to_rgba(PALETTE[name]) for name in subset["room_type"]]
            np.testing.assert_allclose(ax.collections[0].get_facecolors(), colors)
            self.assertEqual(ax.get_xlim(), (18, 47))
            self.assertEqual(ax.get_ylim(), (18, 56))
            self.assertEqual(ax.get_title(), period)

    def test_summary_order_and_values(self):
        summary = make_summary(load_jobs())
        self.assertEqual(list(summary.index), ROOM_ORDER)
        self.assertEqual(list(summary.columns), PERIOD_ORDER)
        np.testing.assert_allclose(summary, [[24, 28], [32, 36], [44, 49]])

    def test_missing_group_stays_missing(self):
        jobs = load_jobs()
        keep = ~((jobs["room_type"] == "Suite") & (jobs["period"] == "Afternoon"))
        summary = make_summary(jobs.loc[keep])
        self.assertEqual(summary.shape, (3, 2))
        self.assertTrue(pd.isna(summary.loc["Suite", "Afternoon"]))
        self.assertEqual(summary.isna().sum().sum(), 1)
        fig, ax = plt.subplots()
        sns.heatmap(summary, annot=True, ax=ax)
        self.assertEqual(np.ma.getmaskarray(ax.collections[0].get_array()).sum(), 1)
        self.assertEqual(len(ax.texts), 5)

    def test_heatmap_labels_values_and_color_scale(self):
        fig = build_heatmap()
        ax = fig.axes[0]
        np.testing.assert_allclose(ax.collections[0].get_array(), [[24, 28], [32, 36], [44, 49]])
        self.assertEqual(ax.collections[0].get_clim(), (20, 55))
        self.assertEqual([text.get_text() for text in ax.texts],
                         ["24.0", "28.0", "32.0", "36.0", "44.0", "49.0"])
        self.assertEqual(fig.axes[1].get_ylabel(), "Mean time (min)")

    def test_optional_density_and_linear_fit(self):
        density_ax, fit_ax = build_patterns().axes
        self.assertEqual(len(density_ax.lines), 2)
        for line in density_ax.lines:
            np.testing.assert_allclose(line.get_xdata()[[0, -1]], [22, 52])
            self.assertTrue(np.isfinite(line.get_ydata()).all())
            self.assertTrue((line.get_ydata() >= 0).all())
        jobs = load_jobs()
        slope, intercept = np.polyfit(jobs["area_m2"], jobs["cleaning_min"], 1)
        line = fit_ax.lines[0]
        np.testing.assert_allclose(line.get_ydata(), slope * line.get_xdata() + intercept)
        self.assertEqual(len(scatter_points(fit_ax)), 18)

    def test_pair_grid_contains_two_numeric_variables(self):
        g = build_pairs()
        self.assertIsInstance(g, sns.PairGrid)
        self.assertEqual(g.axes.shape, (2, 2))
        self.assertEqual(list(g.x_vars), ["area_m2", "cleaning_min"])
        self.assertEqual(len(scatter_points(g.axes[0, 1])), 18)
        self.assertEqual(len(scatter_points(g.axes[1, 0])), 18)
        self.assertTrue(all(len(ax.patches) > 0 for ax in g.diag_axes))

    def test_theme_is_temporary(self):
        before = dict(plt.rcParams)
        with lesson_theme():
            self.assertTrue(plt.rcParams["axes.grid"])
        self.assertEqual(dict(plt.rcParams), before)

    def test_figure_text_and_legends_fit_inside_canvas(self):
        builders = [build_scatter_comparison, build_distribution, build_categories,
                    lambda: build_facets().figure, build_heatmap,
                    build_patterns, lambda: build_pairs().figure]
        for build in builders:
            fig = build()
            with self.subTest(title=fig.axes[0].get_title()):
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                width, height = fig.canvas.get_width_height()
                artists = list(fig.texts) + list(fig.legends)
                for ax in fig.axes:
                    if not ax.get_visible():
                        continue
                    artists.append(ax.title)
                    artists += list(ax.texts)
                    # Locators also return ticks outside the view; Matplotlib does not draw those.
                    for axis, limits in [(ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())]:
                        if not ax.axison or not axis.get_visible():
                            continue
                        artists.append(axis.label)
                        lower, upper = sorted(limits)
                        for tick in axis.get_major_ticks() + axis.get_minor_ticks():
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
            plt.close(fig)

    def test_readme_python_blocks_run_in_order(self):
        namespace = {"__name__": "__lesson__"}
        blocks = python_blocks(EPISODE / "README.md")
        self.assertEqual(len(blocks), 14)
        original_cwd = Path.cwd()

        def draw_and_close(*args, **kwargs):
            for number in plt.get_fignums():
                plt.figure(number).canvas.draw()
            plt.close("all")

        with tempfile.TemporaryDirectory() as tmp, plt.rc_context():
            try:
                os.chdir(tmp)
                with patch.object(plt, "show", side_effect=draw_and_close), redirect_stdout(io.StringIO()):
                    for i, block in enumerate(blocks, 1):
                        exec(compile(block, f"README block {i}", "exec"), namespace)
                pd.testing.assert_frame_equal(namespace["jobs"], load_jobs())
                np.testing.assert_allclose(namespace["summary"], make_summary(load_jobs()))
                self.assertIsInstance(namespace["g"], sns.FacetGrid)
                self.assertIsInstance(namespace["pairs"], sns.PairGrid)
                for filename in ["hotel-chart.png", "hotel-periods.png"]:
                    with Image.open(Path(tmp) / "output" / filename) as image:
                        image.verify()
            finally:
                os.chdir(original_cwd)

    def test_exercise_code_and_answer_values(self):
        namespace = {"jobs": load_jobs()}
        for block in python_blocks(EPISODE / "exercises" / "exercise01.md"):
            exec(block, namespace)
        self.assertEqual(len(namespace["jobs_missing"]), 15)
        self.assertEqual(len(namespace["jobs"]), 18)
        self.assertTrue(pd.isna(make_summary(namespace["jobs_missing"]).loc["Suite", "Afternoon"]))
        values = namespace["jobs"].query("room_type == 'Standard' and period == 'Afternoon'")["cleaning_min"]
        self.assertEqual(values.median(), 29)
        self.assertEqual(values.mean(), 28)
        for bins in [TIME_BINS, [20, 30, 40, 50, 60]]:
            self.assertEqual(np.histogram(load_jobs()["cleaning_min"], bins)[0].sum(), 18)

    def test_readme_structure_and_episode_local_links(self):
        readme = (EPISODE / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (\d+)\.", readme, re.M), [str(n) for n in range(1, 11)])
        for path in [EPISODE / "README.md", EPISODE / "exercises" / "exercise01.md"]:
            content = path.read_text(encoding="utf-8")
            self.assertEqual(content.count("<details>"), content.count("</details>"))
            self.assertNotRegex(content, r"บทพูด|ผู้สอน|ผู้ชม|ไม่ต้องพูด|พูดพร้อมกัน|เน้นตอนสอน")
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if target.startswith(("./", "../")):
                    resolved = (path.parent / target).resolve()
                    # Cross-episode links are checked after installation into the repository.
                    if resolved.is_relative_to(EPISODE):
                        self.assertTrue(resolved.is_file(), str(resolved))

    def test_scripts_run_from_an_unrelated_working_directory(self):
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        with tempfile.TemporaryDirectory() as tmp:
            for name in ["relationships.py", "distributions.py", "category_comparison.py",
                         "summary_heatmap.py", "optional_views.py"]:
                with self.subTest(script=name):
                    result = subprocess.run([sys.executable, "-B", str(SOURCE / name)],
                                            cwd=tmp, env=env, capture_output=True, text=True, timeout=60)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_generator_creates_seven_valid_images_in_nested_output(self):
        expected = {"scatter-groups.png", "cleaning-distribution.png", "room-type-comparison.png",
                    "period-facets.png", "mean-time-heatmap.png", "optional-patterns.png", "pairwise-views.png"}
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "plots"
            result = subprocess.run([sys.executable, "-B", str(SOURCE / "generate_lesson_figures.py"),
                                     "--output-dir", str(output)], cwd=tmp, env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in output.iterdir()}, expected)
            for path in output.glob("*.png"):
                with Image.open(path) as image:
                    self.assertGreaterEqual(min(image.size), 600)
                    image.verify()
        self.assertEqual({p.name for p in (EPISODE / "assets" / "plots").glob("*.png")}, expected)


if __name__ == "__main__":
    unittest.main()
