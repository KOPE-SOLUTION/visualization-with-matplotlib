"""Shared axis labels and limits for comparing the same synthetic survey."""


def configure_3d(ax, title, *, elev=30, azim=-60):
    ax.set(
        title=title,
        xlabel="X position (m)",
        ylabel="Y position (m)",
        zlabel="Height (m)",
        xlim=(0, 20),
        ylim=(0, 15),
        zlim=(0, 10),
        xticks=[0, 5, 10, 15, 20],
        yticks=[0, 5, 10, 15],
        zticks=[0, 2, 4, 6, 8, 10],
    )
    # Match box proportions to axis ranges; all three axes use metres.
    ax.set_box_aspect((20, 15, 10), zoom=0.85)
    ax.view_init(elev=elev, azim=azim)
