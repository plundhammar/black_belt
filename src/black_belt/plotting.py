import matplotlib.pyplot as plt
import geopandas as gpd


def plot_side_by_side(
    gdf: gpd.GeoDataFrame,
    coast_lines: gpd.GeoDataFrame,
    vote_col: str = "dem_margin_2party",
    dist_col: str = "dist_km",
):
    states = gdf.dissolve(by="STATEFP").boundary
    xmin, ymin, xmax, ymax = gdf.total_bounds

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)

    gdf.plot(
        column=vote_col,
        cmap="RdBu",
        vmin=-1,
        vmax=1,
        linewidth=0,
        ax=axes[0],
        legend=True,
        legend_kwds={"label": "Democratic two-party margin"},
        missing_kwds={"color": "lightgrey"},
    )
    states.plot(ax=axes[0], color="black", linewidth=0.35)
    coast_lines.plot(ax=axes[0], color="black", linewidth=0.9)
    axes[0].set_title("County voting pattern (2020)")
    axes[0].set_axis_off()

    gdf.plot(
        column=dist_col,
        cmap="viridis_r",
        linewidth=0,
        ax=axes[1],
        legend=True,
        legend_kwds={"label": "Distance to paleo-boundary (km)"},
        missing_kwds={"color": "lightgrey"},
    )
    states.plot(ax=axes[1], color="black", linewidth=0.35)
    coast_lines.plot(ax=axes[1], color="black", linewidth=0.9)
    axes[1].set_title("Distance to paleo-boundary")
    axes[1].set_axis_off()

    for ax in axes:
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

    return fig, axes