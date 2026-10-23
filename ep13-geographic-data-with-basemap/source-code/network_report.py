"""Map traffic by color and, optionally, connected users by marker area."""

import matplotlib.pyplot as plt

from network_data import load_sites
from map_helpers import make_map, add_graticule, label_sites, add_data_note


def build_figure(show_users=True):
    names, longitude, latitude, connected_users, traffic_mbps = load_sites()
    fig, ax = plt.subplots(figsize=(8, 7), layout="constrained")
    m = make_map(ax)
    add_graticule(m)
    # s is marker area in points squared, not a coverage radius on the ground.
    sizes = connected_users * 1.5 if show_users else 150
    points = m.scatter(
        longitude, latitude, latlon=True,
        s=sizes, c=traffic_mbps, cmap="viridis", vmin=0, vmax=800,
        edgecolors="white", linewidths=0.8, zorder=4,
    )
    label_sites(ax, m, names, longitude, latitude)
    colorbar = fig.colorbar(points, ax=ax, shrink=0.75, pad=0.03)
    colorbar.set_label("Traffic (Mbps)")
    if show_users:
        # Empty scatter objects provide correctly scaled size samples for the legend.
        for users in [120, 240, 360]:
            ax.scatter([], [], s=users * 1.5, color="0.5", edgecolors="white",
                       label=f"{users} users")
        ax.legend(title="Connected users", loc="lower left", labelspacing=1.1,
                  borderpad=0.9, fontsize=9, framealpha=0.95)
    title = "Telecom Sites - Traffic and Users" if show_users else "Telecom Sites - Traffic"
    ax.set_title(title)
    add_data_note(fig)
    return fig


if __name__ == "__main__":
    build_figure(show_users=False)
    build_figure(show_users=True)
    plt.show()
