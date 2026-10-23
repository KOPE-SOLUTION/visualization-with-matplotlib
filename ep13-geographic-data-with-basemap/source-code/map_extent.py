"""Compare geographic bounds without changing the site measurements."""

import matplotlib.pyplot as plt
import numpy as np

from network_data import load_sites
from map_helpers import make_map, add_graticule, label_sites, add_data_note


def build_figure():
    names, longitude, latitude, _, traffic_mbps = load_sites()
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.5), layout="constrained")
    bounds = [(97.5, 104.5, 11.5, 18.5), (99.3, 103.5, 12.5, 15.4)]
    for ax, (west, east, south, north) in zip(axes, bounds):
        m = make_map(ax, west=west, east=east, south=south, north=north)
        add_graticule(m)
        visible = ((longitude >= west) & (longitude <= east)
                   & (latitude >= south) & (latitude <= north))
        points = m.scatter(
            longitude[visible], latitude[visible], latlon=True,
            s=150, c=traffic_mbps[visible], cmap="viridis", vmin=0, vmax=800,
            edgecolors="white", zorder=4,
        )
        label_sites(ax, m, names[visible], longitude[visible], latitude[visible])
        ax.set_title(f"{np.count_nonzero(visible)} sites inside this view")
    colorbar = fig.colorbar(points, ax=axes, shrink=0.65, pad=0.02)
    colorbar.set_label("Traffic (Mbps)")
    add_data_note(fig)
    return fig


if __name__ == "__main__":
    build_figure()
    plt.show()
