"""Regression checks for lesson data, styles, runnable examples, and README code."""

import contextlib
import io
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


EPISODE = Path(__file__).resolve().parents[1]
SOURCE = EPISODE / "source-code"
sys.path.insert(0, str(SOURCE))

from custom_style_report import STYLE_PATH, build_report
from report_helpers import make_report
from style_comparison import build_context_comparison, build_style_comparison
from water_data import create_water_week


@contextlib.contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def draw_and_close_figures():
    for number in plt.get_fignums():
        plt.figure(number).canvas.draw()
    plt.close("all")


class LessonTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_data_is_reproducible_and_independent(self):
        days, produced, distributed = create_water_week()
        np.testing.assert_array_equal(days, np.arange(1, 8))
        self.assertEqual(produced.shape, (7,))
        self.assertEqual(distributed.shape, (7,))
        self.assertEqual(produced[0], 4100)
        self.assertEqual(distributed[0], 3900)
        produced[0] = -1
        self.assertEqual(create_water_week()[1][0], 4100)

    def test_stylesheet_is_valid(self):
        settings = mpl.rc_params_from_file(
            STYLE_PATH, fail_on_error=True, use_default_template=False
        )
        self.assertEqual(settings["lines.linewidth"], 2.6)
        self.assertFalse(settings["axes.spines.top"])
        self.assertFalse(settings["legend.frameon"])
        self.assertEqual(
            settings["axes.prop_cycle"].by_key()["color"],
            ["steelblue", "darkorange"],
        )

    def test_style_does_not_change_data_or_scales(self):
        days, produced, distributed = create_water_week()
        fig = build_style_comparison()
        for ax in fig.axes:
            np.testing.assert_array_equal(ax.lines[0].get_xdata(), days)
            np.testing.assert_array_equal(ax.lines[0].get_ydata(), produced)
            np.testing.assert_array_equal(ax.lines[1].get_ydata(), distributed)
            self.assertEqual(ax.get_xlim(), (0.7, 7.3))
            self.assertEqual(ax.get_ylim(), (3600, 4800))
            self.assertEqual(ax.lines[0].get_marker(), "o")
            self.assertEqual(ax.lines[1].get_marker(), "s")
            self.assertEqual(ax.lines[1].get_linestyle(), "--")
        self.assertEqual(fig.axes[0].lines[0].get_linewidth(), 1.5)
        self.assertEqual(fig.axes[1].lines[0].get_linewidth(), 2.6)
        fig.canvas.draw()

    def test_context_restores_previous_custom_values(self):
        with mpl.rc_context({"lines.linewidth": 7}):
            with mpl.rc_context({"lines.linewidth": 4}):
                fig, ax = make_report(*create_water_week())
                self.assertEqual(mpl.rcParams["lines.linewidth"], 4)
            self.assertEqual(mpl.rcParams["lines.linewidth"], 7)
            self.assertEqual(ax.lines[0].get_linewidth(), 4)

    def test_explicit_linewidth_overrides_default(self):
        with mpl.rc_context({"lines.linewidth": 4}):
            fig, ax = plt.subplots()
            default_line, = ax.plot([1, 2], [3, 4])
            explicit_line, = ax.plot([1, 2], [2, 3], linewidth=1)
        self.assertEqual(default_line.get_linewidth(), 4)
        self.assertEqual(explicit_line.get_linewidth(), 1)

    def test_setting_order_and_style_context_restoration(self):
        with mpl.rc_context({"lines.linewidth": 7}):
            with plt.style.context(["default", STYLE_PATH, {"lines.linewidth": 5}]):
                self.assertEqual(mpl.rcParams["lines.linewidth"], 5)
                mpl.rcParams["lines.linewidth"] = 6
                self.assertEqual(mpl.rcParams["lines.linewidth"], 6)
                plt.style.use(STYLE_PATH)
                self.assertEqual(mpl.rcParams["lines.linewidth"], 2.6)
            self.assertEqual(mpl.rcParams["lines.linewidth"], 7)

    def test_context_figure_before_inside_after(self):
        fig = build_context_comparison()
        widths = [ax.lines[0].get_linewidth() for ax in fig.axes]
        self.assertEqual(widths, [1.5, 4, 1.5])
        fig.canvas.draw()

    def test_custom_report_keeps_appearance_after_context(self):
        with mpl.rc_context({"lines.linewidth": 8}):
            fig, ax = build_report()
            self.assertEqual(mpl.rcParams["lines.linewidth"], 8)
            self.assertEqual(ax.lines[0].get_linewidth(), 2.6)
            self.assertEqual(ax.lines[0].get_color(), "steelblue")
            fig.canvas.draw()

    def test_entry_points_from_root_and_source_folder(self):
        names = [
            "rcparams_demo.py", "builtin_styles.py",
            "custom_style_report.py", "style_comparison.py",
        ]
        with patch.object(plt, "show", side_effect=draw_and_close_figures):
            with contextlib.redirect_stdout(io.StringIO()):
                for cwd in [EPISODE.parent, SOURCE]:
                    with working_directory(cwd):
                        for name in names:
                            with self.subTest(cwd=cwd, name=name):
                                runpy.run_path(str(SOURCE / name), run_name="__main__")

    def test_readme_python_blocks(self):
        text = (EPISODE / "README.md").read_text(encoding="utf-8")
        blocks = re.findall(r"~~~python\n(.*?)\n~~~", text, flags=re.DOTALL)
        self.assertGreaterEqual(len(blocks), 15)
        with tempfile.TemporaryDirectory() as temp:
            # Only the export target is redirected; plotting and style loading run unchanged.
            original_savefig = mpl.figure.Figure.savefig

            def save_to_temp(fig, filename, *args, **kwargs):
                return original_savefig(fig, Path(temp) / Path(filename).name, *args, **kwargs)

            for from_root in [False, True]:
                cwd = EPISODE.parent if from_root else EPISODE
                namespace = {}
                with self.subTest(from_root=from_root), working_directory(cwd):
                    with mpl.rc_context(), contextlib.redirect_stdout(io.StringIO()):
                        with patch.object(plt, "show", side_effect=draw_and_close_figures):
                            with patch.object(mpl.figure.Figure, "savefig", save_to_temp):
                                for index, block in enumerate(blocks):
                                    compile(block, f"README block {index}", "exec")
                                    # The explicitly documented alternative path replaces the local one.
                                    if 'Path("ep11-configurations-and-stylesheets")' in block:
                                        continue
                                    if from_root:
                                        block = block.replace(
                                            'Path("styles")',
                                            'Path("ep11-configurations-and-stylesheets") / "styles"',
                                        )
                                    exec(block, namespace)
            self.assertTrue((Path(temp) / "water-week-report.png").is_file())

    def test_generator_accepts_independent_working_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            for index, cwd in enumerate([EPISODE.parent, SOURCE, Path(temp)]):
                target = Path(temp) / str(index) / "plots"
                result = subprocess.run(
                    [sys.executable, "-B", str(SOURCE / "generate_lesson_figures.py"),
                     "--output-dir", str(target)],
                    cwd=cwd, capture_output=True, text=True, timeout=45,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(len(list(target.glob("*.png"))), 3)
                for path in target.glob("*.png"):
                    image = plt.imread(path)
                    self.assertGreaterEqual(image.shape[1], 1400)

    def test_readme_resources_and_reader_facing_content(self):
        for path in [EPISODE / "README.md", EPISODE / "exercises" / "exercise01.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<details>"), text.count("</details>"))
            for phrase in ["ไม่ต้องพูด", "บทพูด", "สำหรับผู้สอน", "จุดที่ต้องเน้น"]:
                self.assertNotIn(phrase, text)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if not target.startswith(("https://", "http://", "#")):
                    self.assertTrue((path.parent / target).exists(), target)


if __name__ == "__main__":
    unittest.main()
