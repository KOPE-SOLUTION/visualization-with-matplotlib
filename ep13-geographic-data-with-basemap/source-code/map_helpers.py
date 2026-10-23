"""Shared map background, coordinate labels, and site annotations."""

from mpl_toolkits.basemap import Basemap


def make_map(ax, west=97.5, east=104.5, south=11.5, north=18.5):
    """Create a Mercator map; bounds are longitude/latitude in degrees."""
    m = Basemap(
        projection="merc",
        llcrnrlon=west,
        llcrnrlat=south,
        urcrnrlon=east,
        urcrnrlat=north,
        resolution="l",
        ax=ax,
    )
    m.drawmapboundary(fill_color="#e7f1f6")
    m.fillcontinents(color="#f1efe7", lake_color="#e7f1f6")
    m.drawcoastlines(color="0.4", linewidth=0.6)
    m.drawcountries(color="0.5", linewidth=0.6)
    return m


def add_graticule(m):
    """Label latitude on the left and longitude along the bottom."""
    m.drawparallels([12, 14, 16, 18], labels=[1, 0, 0, 0],
                   linewidth=0.4, color="0.65", fontsize=9)
    m.drawmeridians([98, 100, 102, 104], labels=[0, 0, 0, 1],
                   linewidth=0.4, color="0.65", fontsize=9)


def label_sites(ax, m, names, longitude, latitude):
    """Offset each label from its projected data position, in points."""
    x, y = m(longitude, latitude)
    for name, xi, yi in zip(names, x, y):
        ax.annotate(name, xy=(xi, yi), xytext=(9, 9),
                    textcoords="offset points", fontsize=10, zorder=5)


def add_data_note(fig):
    fig.supxlabel("Fictional sites and measurements | Not a coverage map", fontsize=9)
