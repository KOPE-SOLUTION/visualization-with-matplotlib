"""Compare a map background with the same map containing six sites."""

import matplotlib.pyplot as plt

from network_data import load_sites
from map_helpers import make_map, label_sites, add_data_note


def build_figure():
    names, longitude, latitude, _, _ = load_sites()
    fig, axes = plt.subplots(1, 2, figsize=(11, 7), layout="constrained")
    for ax in axes:
        m = make_map(ax)
        if ax is axes[1]:
            # Basemap converts longitude/latitude to this map's x/y coordinates.
            x, y = m(longitude, latitude)
            ax.scatter(x, y, s=90, color="tab:blue", edgecolors="white", zorder=4)
            label_sites(ax, m, names, longitude, latitude)
    axes[0].set_title("1. Map background")
    axes[1].set_title("2. Add six fictional sites")
    add_data_note(fig)
    return fig


if __name__ == "__main__":
    build_figure()
    plt.show()
