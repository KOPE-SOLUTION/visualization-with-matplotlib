"""Headless checks for coordinates, data encodings, README examples, and output."""

import contextlib
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
from matplotlib.collections import PathCollection
from matplotlib.text import Annotation
import numpy as np
from PIL import Image

EPISODE = Path(__file__).resolve().parents[1]
SOURCE = EPISODE / "source-code"
sys.path.insert(0, str(SOURCE))

from network_data import load_sites
from map_helpers import make_map, add_graticule
from site_locations import build_figure as build_locations
from network_report import build_figure as build_report
from map_extent import build_figure as build_extent


@contextlib.contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def scatters(ax):
    return [artist for artist in ax.collections if isinstance(artist, PathCollection)]


def draw_and_close():
    for number in plt.get_fignums():
        fig = plt.figure(number)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for ax in fig.axes:
            if ax.title.get_text():
                bbox = ax.title.get_window_extent(renderer)
                if bbox.y1 > fig.bbox.height + 1:
                    raise AssertionError(f"Title outside canvas: {ax.title.get_text()}")
        plt.close(fig)


class LessonTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_site_data_is_aligned_and_finite(self):
        names, lon, lat, users, traffic = load_sites()
        for values in [names, lon, lat, users, traffic]:
            self.assertEqual(values.shape, (6,))
        self.assertEqual(len(set(names)), 6)
        for values in [lon, lat, users, traffic]:
            self.assertTrue(np.isfinite(values).all())
        self.assertTrue(((lon >= -180) & (lon <= 180)).all())
        self.assertTrue(((lat >= -90) & (lat <= 90)).all())
        self.assertEqual(names[np.argmax(traffic)], "Site D")
        self.assertEqual(names[np.argmax(users)], "Site D")
        self.assertEqual(traffic.max(), 680)
        self.assertEqual(users.max(), 360)

    def test_load_returns_independent_arrays(self):
        changed = load_sites()
        changed[1][0] = 0
        changed[-1][0] = 0
        self.assertEqual(load_sites()[1][0], 99.2)
        self.assertEqual(load_sites()[-1][0], 180)

    def test_projection_round_trip_and_all_sites_inside(self):
        _, lon, lat, _, _ = load_sites()
        fig, ax = plt.subplots()
        m = make_map(ax)
        x, y = m(lon, lat)
        lon_back, lat_back = m(x, y, inverse=True)
        np.testing.assert_allclose(lon_back, lon, atol=1e-10)
        np.testing.assert_allclose(lat_back, lat, atol=1e-10)
        self.assertTrue(((x > m.xmin) & (x < m.xmax)).all())
        self.assertTrue(((y > m.ymin) & (y < m.ymax)).all())
        self.assertFalse(np.allclose(x, lon))

    def test_sites_are_on_land_in_the_bundled_map(self):
        _, lon, lat, _, _ = load_sites()
        fig, ax = plt.subplots()
        m = make_map(ax)
        x, y = m(lon, lat)
        self.assertTrue(all(m.is_land(xi, yi) for xi, yi in zip(x, y)))

    def test_explicit_projection_matches_latlon_scatter(self):
        _, lon, lat, _, _ = load_sites()
        fig, ax = plt.subplots()
        m = make_map(ax)
        x, y = m(lon, lat)
        explicit = ax.scatter(x, y)
        implicit = m.scatter(lon, lat, latlon=True)
        np.testing.assert_allclose(explicit.get_offsets(), implicit.get_offsets())

    def test_site_label_coordinates_match_markers(self):
        fig = build_locations()
        self.assertEqual(len(scatters(fig.axes[0])), 0)
        ax = fig.axes[1]
        points = scatters(ax)[0]
        labels = [text for text in ax.texts if isinstance(text, Annotation)]
        self.assertEqual([label.get_text() for label in labels], list(load_sites()[0]))
        np.testing.assert_allclose([label.xy for label in labels], points.get_offsets())

    def test_traffic_colorbar_uses_scatter(self):
        fig = build_report(show_users=False)
        points = scatters(fig.axes[0])[0]
        np.testing.assert_array_equal(points.get_array(), load_sites()[-1])
        np.testing.assert_array_equal(points.get_sizes(), [150])
        self.assertEqual(points.get_clim(), (0, 800))
        self.assertIs(points.colorbar.mappable, points)
        self.assertEqual(points.colorbar.ax.get_ylabel(), "Traffic (Mbps)")

    def test_marker_area_and_legend_share_same_scale(self):
        fig = build_report()
        points, *proxies = scatters(fig.axes[0])
        np.testing.assert_array_equal(points.get_sizes(), load_sites()[3] * 1.5)
        self.assertEqual(len(proxies), 3)
        for proxy, users in zip(proxies, [120, 240, 360]):
            self.assertEqual(proxy.get_offsets().shape, (0, 2))
            np.testing.assert_array_equal(proxy.get_sizes(), [users * 1.5])
        legend = fig.axes[0].get_legend()
        self.assertEqual([text.get_text() for text in legend.get_texts()],
                         ["120 users", "240 users", "360 users"])

    def test_zoom_selects_same_values_and_color_scale(self):
        original = load_sites()
        fig = build_extent()
        full = scatters(fig.axes[0])[0]
        zoomed = scatters(fig.axes[1])[0]
        self.assertEqual(full.get_offsets().shape, (6, 2))
        self.assertEqual(zoomed.get_offsets().shape, (3, 2))
        np.testing.assert_array_equal(zoomed.get_array(), original[-1][3:])
        self.assertEqual(full.get_clim(), zoomed.get_clim())
        np.testing.assert_allclose(full.to_rgba(original[-1][3:]),
                                   zoomed.to_rgba(zoomed.get_array()))
        labels = [text.get_text() for text in fig.axes[1].texts
                  if isinstance(text, Annotation)]
        self.assertEqual(labels, ["Site D", "Site E", "Site F"])
        for before, after in zip(original, load_sites()):
            np.testing.assert_array_equal(before, after)

    def test_exercise_extent_selects_first_three(self):
        names, lon, lat, _, _ = load_sites()
        visible = (lon >= 98) & (lon <= 104) & (lat >= 15.5) & (lat <= 17.5)
        np.testing.assert_array_equal(names[visible], ["Site A", "Site B", "Site C"])

    def test_figure_text_fits_canvas(self):
        builders = [build_locations, lambda: build_report(False), build_report, build_extent]
        for builder in builders:
            fig = builder()
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            width, height = fig.bbox.width, fig.bbox.height
            texts = list(fig.texts)
            for ax in fig.axes:
                texts.extend([ax.title, ax.xaxis.label, ax.yaxis.label])
                texts.extend(ax.texts)
                if ax.get_legend():
                    texts.extend(ax.get_legend().get_texts())
            for text in texts:
                if not text.get_text() or not text.get_visible():
                    continue
                bbox = text.get_window_extent(renderer)
                self.assertGreaterEqual(bbox.x0, -1, text.get_text())
                self.assertGreaterEqual(bbox.y0, -1, text.get_text())
                self.assertLessEqual(bbox.x1, width + 1, text.get_text())
                self.assertLessEqual(bbox.y1, height + 1, text.get_text())
            plt.close(fig)

    def test_readme_blocks_run_in_order_and_match_source_data(self):
        readme = (EPISODE / "README.md").read_text(encoding="utf-8")
        blocks = re.findall(r"~~~python\n(.*?)\n~~~", readme, re.S)
        self.assertGreaterEqual(len(blocks), 10)
        namespace = {"__name__": "__lesson__"}
        with tempfile.TemporaryDirectory() as folder, working_directory(folder):
            with patch.object(plt, "show", side_effect=draw_and_close):
                for index, block in enumerate(blocks, start=1):
                    exec(compile(block, f"README block {index}", "exec"), namespace)
            self.assertTrue((Path(folder) / "output" / "telecom-map.png").is_file())
        names, lon, lat, users, traffic = load_sites()
        for key, expected in [("site_names", names), ("longitude", lon), ("latitude", lat),
                              ("connected_users", users), ("traffic_mbps", traffic)]:
            np.testing.assert_array_equal(namespace[key], expected)
        # The README and source helper use the same map parameters and transforms.
        fig, axes = plt.subplots(1, 2)
        actual = namespace["make_map"](axes[0])
        expected = make_map(axes[1])
        np.testing.assert_allclose(actual(lon, lat), expected(lon, lat))

    def test_scripts_run_from_root_and_source(self):
        environment = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        for cwd in [EPISODE.parent, SOURCE]:
            for name in ["site_locations.py", "network_report.py", "map_extent.py"]:
                result = subprocess.run([sys.executable, "-B", str(SOURCE / name)],
                                        cwd=cwd, env=environment, capture_output=True,
                                        text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_generator_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "new" / "plots"
            result = subprocess.run(
                [sys.executable, "-B", str(SOURCE / "generate_lesson_figures.py"),
                 "--output-dir", str(output)],
                cwd=folder, capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(list(output.glob("*.png"))), 4)
            for path in output.glob("*.png"):
                with Image.open(path) as image:
                    self.assertGreater(image.width, 800)
                    self.assertGreater(image.height, 600)
                    image.verify()

    def test_document_links_headings_and_assets(self):
        readme = (EPISODE / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (\d+)\.", readme, re.M),
                         [str(number) for number in range(1, 11)])
        self.assertEqual(readme.count("<details>"), readme.count("</details>"))
        for document in [EPISODE / "README.md", EPISODE / "exercises" / "exercise01.md"]:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith("./") or target == "../README.md":
                    self.assertTrue((document.parent / target).is_file(), target)
            for phrase in ["บทพูด", "ไม่ต้องพูด", "คนสอน", "ผู้สอน", "เน้นพูด", "ข้ามส่วนนี้"]:
                self.assertNotIn(phrase, text)
        for name in ["site-locations", "traffic-map", "network-report", "map-extent"]:
            with Image.open(EPISODE / "assets" / "plots" / f"{name}.png") as image:
                image.verify()


if __name__ == "__main__":
    unittest.main()
