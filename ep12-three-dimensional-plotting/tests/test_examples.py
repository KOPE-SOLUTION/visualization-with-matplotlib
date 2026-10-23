"""Headless checks for EP12 data, figures, runnable README blocks, and paths."""

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

import matplotlib.pyplot as plt
import numpy as np

EPISODE = Path(__file__).resolve().parents[1]
SOURCE = EPISODE / "source-code"
sys.path.insert(0, str(SOURCE))

from stockpile_data import load_grid, load_irregular, load_profile
from points_and_profile import build_figure as build_points
from surface_views import build_overview, build_view_comparison
from contour_comparison import build_figure as build_contours
from irregular_surface import build_figure as build_irregular


@contextlib.contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def draw_and_close():
    for number in plt.get_fignums():
        fig = plt.figure(number)
        fig.canvas.draw()
        plt.close(fig)


class LessonTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_grid_coordinate_mapping(self):
        x, y, height = load_grid()
        X, Y = np.meshgrid(x, y)
        self.assertEqual(height.shape, (4, 5))
        self.assertEqual(X.shape, height.shape)
        self.assertEqual(Y.shape, height.shape)
        self.assertEqual((X[2, 2], Y[2, 2], height[2, 2]), (10, 10, 7.5))
        self.assertEqual((X[2, 3], Y[2, 3], height[2, 3]), (15, 10, 4.6))
        self.assertTrue(np.isfinite(height).all())
        self.assertEqual(height.max(), 7.5)

    def test_profile_is_the_same_grid_row(self):
        x, y, height = load_grid()
        xp, yp, hp = load_profile()
        np.testing.assert_array_equal(xp, x)
        np.testing.assert_array_equal(yp, np.full(x.size, y[1]))
        np.testing.assert_array_equal(hp, height[1])
        self.assertTrue((np.diff(xp) > 0).all())
        self.assertEqual(hp.max(), 6.2)

    def test_data_calls_return_independent_arrays(self):
        for loader in [load_grid, load_profile, load_irregular]:
            original = loader()
            changed = loader()
            changed[-1].flat[0] = 999
            np.testing.assert_array_equal(original[-1], loader()[-1])

    def test_irregular_coordinates_are_valid_for_triangulation(self):
        x, y, height = load_irregular()
        self.assertEqual(x.shape, (11,))
        self.assertEqual(x.shape, y.shape)
        self.assertEqual(x.shape, height.shape)
        self.assertEqual(np.unique(np.column_stack([x, y]), axis=0).shape[0], x.size)
        self.assertEqual(np.linalg.matrix_rank(np.column_stack([x - x.mean(), y - y.mean()])), 2)

    def test_points_and_line_use_identical_coordinates(self):
        fig = build_points()
        points, profile = fig.axes
        xp, yp, hp = load_profile()
        actual = profile.lines[0].get_data_3d()
        for values, expected in zip(actual, [xp, yp, hp]):
            np.testing.assert_array_equal(values, expected)
        # Scatter stores the samples in one collection; the profile is one line.
        self.assertEqual(len(points.collections), 1)
        self.assertEqual(len(profile.lines), 1)
        fig.canvas.draw()

    def test_3d_figures_keep_ranges_and_box_proportions(self):
        for build in [build_points, build_overview, build_view_comparison,
                      build_contours, build_irregular]:
            with self.subTest(builder=build.__name__):
                fig = build()
                for ax in fig.axes:
                    if ax.name == "3d":
                        self.assertEqual(ax.get_xlim(), (0, 20))
                        self.assertEqual(ax.get_ylim(), (0, 15))
                        self.assertEqual(ax.get_zlim(), (0, 10))
                        aspect = ax.get_box_aspect()
                        np.testing.assert_allclose(aspect / aspect[0], [1, 0.75, 0.5])
                        self.assertEqual(ax.get_zlabel(), "Height (m)")
                fig.canvas.draw()
                plt.close(fig)

    def test_shared_colour_limits(self):
        for build in [build_overview, build_view_comparison, build_irregular]:
            fig = build()
            coloured = [
                artist for ax in fig.axes if ax.name == "3d"
                for artist in ax.collections if artist.get_array() is not None
            ]
            self.assertEqual(len(coloured), 2)
            for artist in coloured:
                self.assertEqual(artist.get_clim(), (0, 8))
            plt.close(fig)

    def test_figure_labels_fit_inside_canvas(self):
        for build in [build_points, build_overview, build_view_comparison,
                      build_contours, build_irregular]:
            fig = build()
            fig.canvas.draw()
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            for ax in fig.axes:
                labels = [ax.title, ax.xaxis.label, ax.yaxis.label]
                if ax.name == "3d":
                    labels.append(ax.zaxis.label)
                for label in labels:
                    if not label.get_text():
                        continue
                    bounds = label.get_window_extent(renderer)
                    with self.subTest(builder=build.__module__, label=label.get_text()):
                        self.assertGreaterEqual(bounds.x0, 0)
                        self.assertGreaterEqual(bounds.y0, 0)
                        self.assertLessEqual(bounds.x1, fig.bbox.width)
                        self.assertLessEqual(bounds.y1, fig.bbox.height)
            plt.close(fig)

    def test_view_angles_and_data_preservation(self):
        baseline = load_grid()[-1]
        fig = build_view_comparison()
        axes = [ax for ax in fig.axes if ax.name == "3d"]
        self.assertEqual([(ax.elev, ax.azim) for ax in axes], [(25, -60), (60, 30)])
        np.testing.assert_array_equal(load_grid()[-1], baseline)
        # The two surfaces use identical colour-driving height values.
        np.testing.assert_array_equal(
            axes[0].collections[0].get_array(), axes[1].collections[0].get_array(),
        )

    def test_contour_levels_and_2d_extent(self):
        fig = build_contours()
        ax3d, ax2d = fig.axes[:2]
        np.testing.assert_array_equal(ax3d.collections[0].levels, [1, 3, 5, 7])
        self.assertEqual(ax2d.get_xlim(), (0, 20))
        self.assertEqual(ax2d.get_ylim(), (0, 15))
        self.assertEqual(ax2d.get_aspect(), 1.0)
        np.testing.assert_array_equal(ax2d.collections[0].levels, np.arange(0, 9))
        fig.canvas.draw()

    def test_scripts_run_from_root_and_source_directory(self):
        names = ["points_and_profile.py", "surface_views.py",
                 "contour_comparison.py", "irregular_surface.py"]
        with patch.object(plt, "show", side_effect=draw_and_close):
            for cwd in [EPISODE.parent, SOURCE]:
                with working_directory(cwd):
                    for name in names:
                        with self.subTest(cwd=cwd, name=name):
                            runpy.run_path(str(SOURCE / name), run_name="__main__")

    def test_all_readme_python_blocks(self):
        text = (EPISODE / "README.md").read_text(encoding="utf-8")
        blocks = re.findall(r"~~~python\n(.*?)\n~~~", text, re.DOTALL)
        self.assertGreaterEqual(len(blocks), 20)
        namespace = {}
        with tempfile.TemporaryDirectory() as temp:
            with working_directory(temp), plt.style.context("default"):
                with patch.object(plt, "show", side_effect=draw_and_close):
                    with contextlib.redirect_stdout(io.StringIO()):
                        for index, block in enumerate(blocks):
                            exec(compile(block, f"README block {index}", "exec"), namespace)
            self.assertTrue((Path(temp) / "stockpile-3d.png").is_file())
        x, y, height = load_grid()
        for name, expected in [("x", x), ("y", y), ("height", height)]:
            np.testing.assert_array_equal(namespace[name], expected)
        for name, expected in zip(
            ["x_points", "y_points", "height_points"], load_profile(),
        ):
            np.testing.assert_array_equal(namespace[name], expected)
        for name, expected in zip(
            ["sample_x", "sample_y", "sample_height"], load_irregular(),
        ):
            np.testing.assert_array_equal(namespace[name], expected)

    def test_generator_from_three_working_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            for index, cwd in enumerate([EPISODE.parent, SOURCE, Path(temp)]):
                destination = Path(temp) / str(index) / "nested" / "plots"
                result = subprocess.run(
                    [sys.executable, "-B", str(SOURCE / "generate_lesson_figures.py"),
                     "--output-dir", str(destination)],
                    cwd=cwd, capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                images = list(destination.glob("*.png"))
                self.assertEqual(len(images), 5)
                for image in images:
                    pixels = plt.imread(image)
                    self.assertGreater(pixels.shape[1], 1000)
                    self.assertGreater(pixels.shape[0], 500)

    def test_reader_facing_docs_and_relative_links(self):
        paths = [EPISODE / "README.md", EPISODE / "exercises" / "exercise01.md"]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<details>"), text.count("</details>"))
            self.assertEqual(len(re.findall(r"^~~~", text, re.MULTILINE)) % 2, 0)
            for phrase in ["ไม่ต้องพูด", "บทพูด", "สำหรับผู้สอน", "จุดที่ต้องเน้น"]:
                self.assertNotIn(phrase, text)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if not target.startswith(("https://", "http://", "#")):
                    self.assertTrue((path.parent / target).exists(), target)
        text = paths[0].read_text(encoding="utf-8")
        headings = re.findall(r"^## (\d+)\.", text, re.MULTILINE)
        self.assertEqual(headings, [str(n) for n in range(1, 13)])


if __name__ == "__main__":
    unittest.main()
