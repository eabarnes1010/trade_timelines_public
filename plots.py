"""Metrics for generic plotting.

Functions
---------
plot_metrics(history,metric)
plot_metrics_panels(history, settings)
plot_map(x, clim=None, title=None, text=None, cmap='RdGy')
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy as ct
import numpy.ma as ma
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import palettable
from matplotlib.colors import ListedColormap
import data_processing
from scipy.cluster.hierarchy import dendrogram

mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["figure.dpi"] = 150


def savefig(filename, fig_format=(".png",), dpi=300):
    for fig_format in fig_format:  # (".png", ".pdf"):
        plt.savefig(filename + fig_format, bbox_inches="tight", dpi=dpi)


def set_equal_xy(ax):
    ylims = ax.get_ylim()
    xlims = ax.get_xlim()

    max_lim = np.max([xlims, ylims])
    min_lim = np.min([xlims, ylims])

    ax.set_xlim(min_lim, max_lim)
    ax.set_ylim(min_lim, max_lim)

    ax.set_aspect("equal", adjustable="box")


def get_qual_cmap():
    cmap = palettable.colorbrewer.qualitative.Accent_7.mpl_colormap
    cmap = ListedColormap(cmap(np.linspace(0, 1, 11)))
    cmap2 = cmap.colors
    cmap2[6, :] = cmap.colors[0, :]
    cmap2[2:6, :] = cmap.colors[5:1:-1, :]
    cmap2[1, :] = (0.95, 0.95, 0.95, 1)
    cmap2[0, :] = (1, 1, 1, 1)
    cmap2[5, :] = cmap2[6, :]
    cmap2[6, :] = [0.7945098, 0.49647059, 0.77019608, 1.0]
    cmap2 = np.append(cmap2, [[0.2, 0.2, 0.2, 1]], axis=0)
    cmap2 = np.delete(cmap2, 0, 0)

    return ListedColormap(cmap2)


def drawOnGlobe(
    ax,
    map_proj,
    data,
    lats,
    lons,
    cmap="coolwarm",
    vmin=None,
    vmax=None,
    inc=None,
    cbarBool=True,
    contourMap=[],
    contourVals=[],
    fastBool=False,
    extent="both",
    norm=None,
    cb_shrink=0.45,
):
    data_crs = ct.crs.PlateCarree()
    # fixes white line by adding point#data,lons#ct.util.add_cyclic_point(data, coord=lons) #fixes white line by adding point
    data_cyc, lons_cyc = add_cyclic_point(data, coord=lons)
    data_cyc = data
    lons_cyc = lons

    #     ax.set_global()
    #     ax.coastlines(linewidth = 1.2, color='black')
    #     ax.add_feature(cartopy.feature.LAND, zorder=0, scale = '50m', edgecolor='black', facecolor='black')

    # ADD COASTLINES
    land_feature = cfeature.NaturalEarthFeature(
        category="physical",
        name="land",
        scale="50m",
        facecolor="None",
        edgecolor="k",
        linewidth=0.5,
    )
    ax.add_feature(land_feature)

    # ADD COUNTRIES
    country_feature = cfeature.NaturalEarthFeature(
        category="cultural",
        name="admin_0_countries",
        scale="50m",
        facecolor="None",
        edgecolor="k",
        linewidth=0.25,
        alpha=0.25,
    )
    ax.add_feature(country_feature)

    # ax.GeoAxes.patch.set_facecolor('black')

    if fastBool:
        image = ax.pcolormesh(
            lons_cyc,
            lats,
            data_cyc,
            transform=data_crs,
            cmap=cmap,
            norm=norm,
        )
    #         image = ax.contourf(lons_cyc, lats, data_cyc, np.linspace(0,vmax,20),transform=data_crs, cmap=cmap)
    else:
        image = ax.pcolor(
            lons_cyc, lats, data_cyc, transform=data_crs, cmap=cmap, shading="auto"
        )

    if np.size(contourMap) != 0:
        contourMap_cyc, __ = add_cyclic_point(
            contourMap, coord=lons
        )  # fixes white line by adding point
        ax.contour(
            lons_cyc,
            lats,
            contourMap_cyc,
            contourVals,
            transform=data_crs,
            colors="fuchsia",
        )

    if cbarBool:
        cb = plt.colorbar(
            image, shrink=cb_shrink, orientation="horizontal", pad=0.02, extend=extent
        )
        cb.ax.tick_params(labelsize=8)
    else:
        cb = None

    image.set_clim(vmin, vmax)

    return cb, image


def add_cyclic_point(data, coord=None, axis=-1):
    # had issues with cartopy finding utils so copied for myself

    if coord is not None:
        if coord.ndim != 1:
            raise ValueError("The coordinate must be 1-dimensional.")
        if len(coord) != data.shape[axis]:
            raise ValueError(
                "The length of the coordinate does not match "
                "the size of the corresponding dimension of "
                "the data array: len(coord) = {}, "
                "data.shape[{}] = {}.".format(len(coord), axis, data.shape[axis])
            )
        delta_coord = np.diff(coord)
        if not np.allclose(delta_coord, delta_coord[0]):
            raise ValueError("The coordinate must be equally spaced.")
        new_coord = ma.concatenate((coord, coord[-1:] + delta_coord[0]))
    slicer = [slice(None)] * data.ndim
    try:
        slicer[axis] = slice(0, 1)
    except IndexError:
        raise ValueError(
            "The specified axis does not correspond to an array dimension."
        )
    new_data = ma.concatenate((data, data[tuple(slicer)]), axis=axis)
    if coord is None:
        return_value = new_data
    else:
        return_value = new_data, new_coord
    return return_value


def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(("outward", 5))
        else:
            spine.set_color("none")
    if "left" in spines:
        ax.yaxis.set_ticks_position("left")
    else:
        ax.yaxis.set_ticks([])
    if "bottom" in spines:
        ax.xaxis.set_ticks_position("bottom")
    else:
        ax.xaxis.set_ticks([])


def format_spines(ax):
    adjust_spines(ax, ["left", "bottom"])
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["left"].set_color("dimgrey")
    ax.spines["bottom"].set_color("dimgrey")
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)
    ax.tick_params("both", length=4, width=2, which="major", color="dimgrey")


#     ax.yaxis.grid(zorder=1,color='dimgrey',alpha=0.35)


def plot_import_cov(
    reporter_country,
    data_trade,
    reporter_response_vector,
    partner_response_vector,
    trade_data_year,
    trade_summary=False,
):
    import scipy.stats as stats

    cmap = ListedColormap(palettable.scientific.diverging.Roma_10_r.mpl_colors)
    cmap.set_bad(color="white", alpha=0.8)

    if trade_summary:
        x = partner_response_vector
        top_partners = data_trade
        TOP_N = len(top_partners)
    else:
        TOP_N = 5
        top_partners = data_trade.sort_values(by="TotValue", ascending=False)[:TOP_N]
        print(top_partners)
        x = partner_response_vector[:, top_partners.index.values]
    x = np.insert(x, 0, reporter_response_vector, axis=1)

    print(x.shape)
    cov = stats.spearmanr(x).correlation
    cov = remove_offdiagonal(cov)

    plt.pcolormesh(np.ma.masked_invalid(cov), edgecolors="k", linewidths=4, cmap=cmap)

    reporter_country_name = data_processing.get_name_from_code(
        [
            reporter_country,
        ]
    )
    names = [
        "Total",
    ] + list(data_processing.get_name_from_code(top_partners["Source"].values))
    # names = ["Total", ] + list(top_partners["Source"].values)
    plt.xticks(np.arange(0.5, TOP_N + 1 + 0.5, 1.0), names, rotation=45)
    plt.yticks(np.arange(0.5, TOP_N + 1 + 0.5, 1.0), names, rotation=45)
    plt.clim(-1.0, 1.0)
    plt.colorbar(shrink=0.5, ticks=np.arange(-1, 1.2, 0.2))
    plt.xlim(0.0 - 0.025, TOP_N + 1 + 0.025)
    plt.ylim(0.0 - 0.025, TOP_N + 1 + 0.025)

    plt.title(
        str(reporter_country_name)
        + " Top "
        + str(TOP_N)
        + " Importers\nSpearman Correlation Across Members"
    )
    plt.gca().set_aspect("equal")

    return x, cov


def remove_offdiagonal(x, remove_diagonal=False):
    if remove_diagonal:
        for i in np.arange(0, x.shape[0]):
            for j in np.arange(0, x.shape[1]):
                if i <= j:
                    x[i, j] = np.nan
    else:
        for i in np.arange(0, np.shape(x)[0]):
            for j in np.arange(0, np.shape(x)[1]):
                if i < j:
                    x[i, j] = np.nan
    return x


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    R = dendrogram(linkage_matrix, **kwargs)
    return R, linkage_matrix


def schematic_maps(map_to_plot, lat, lon, cmap, vmin=None, vmax=None, xticks=None, xticklabels=None, country_list=(), reg_bnds=[0, 360, -90, 90]):
    from cartopy.io import shapereader
    import geopandas

    # get country borders
    resolution = "10m"
    category = "cultural"
    name = "admin_0_countries"

    shpfilename = shapereader.natural_earth(resolution, category, name)
    # read the shapefile using geopandas
    df = geopandas.read_file(shpfilename)

    # make the plot
    fig = plt.figure(figsize=(4.75 * 2.0, 3.0 * 1.75), dpi=150)
    data_crs = ct.crs.PlateCarree()
    map_proj = ct.crs.EqualEarth(central_longitude=0.0)

    ax = fig.add_subplot(2, 2, 1, projection=map_proj)
    cb, __ = drawOnGlobe(
        ax,
        map_proj,
        data=map_to_plot,
        lats=lat,
        lons=lon,
        fastBool=True,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        cbarBool=True,
        extent="neither",
        cb_shrink=0.2,
    )
    cb.set_ticks(xticks)
    cb.set_ticklabels(xticklabels)
    cb.ax.tick_params(labelsize=6)

    for ic, c in enumerate(country_list):
        poly = df.loc[df["ADMIN"] == c]["geometry"].values[0]
        if ic == 0:
            color = "darkviolet"
        else:
            color = "dodgerblue"
        ax.add_geometries(
            poly,
            crs=ccrs.PlateCarree(),
            facecolor="none",
            edgecolor=color,
            linewidth=0.7,
        )
    ax.set_extent(reg_bnds, crs=data_crs)

    plt.tight_layout()
    plt.box(False)
