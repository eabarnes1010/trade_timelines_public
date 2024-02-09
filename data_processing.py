"""Analysis functions.

Functions
---------

"""

import numpy as np
import xarray as xr
import geopandas as gpd
import regionmask
import os
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import file_handling

SEASONS_DIRECTORY = "data/sacks_etal_2010/"
LONGNAME_FILE = "data/GTAP_data/2023-06-16-LongName.xlsx"


def quantile_fun(x, perc):
    return x.quantile(perc / 100.0, dim=("member", "time"))


def get_population(filepath, da_grid):
    da_pop = xr.load_dataarray(filepath)
    da_pop.coords["lon"] = np.mod(da_pop["lon"], 360)
    da_pop = da_pop.sortby(da_pop.lon)
    print(da_pop.sum(("lat", "lon")))

    # da_pop_regrid = np.zeros((len(da_all["lat"].values), len(da_all["lon"].values)))
    da_pop_regrid = xr.zeros_like(da_grid[:, :].squeeze())

    for ilat, lat in enumerate(da_grid["lat"].values[:-1]):
        for ilon, lon in enumerate(da_grid["lon"].values):
            if ilon == len(da_grid["lon"].values) - 1:
                eval_lon = 361.0
            else:
                eval_lon = da_grid["lon"][ilon + 1]
            ilat_pop = np.where((da_pop["lat"] >= da_grid["lat"][ilat]) & (da_pop["lat"] < da_grid["lat"][ilat + 1]))[0]
            ilon_pop = np.where((da_pop["lon"] >= da_grid["lon"][ilon]) & (da_pop["lon"] < eval_lon))[0]

            da_pop_regrid[ilat, ilon] = da_pop[ilat_pop, ilon_pop].sum(("lat", "lon"))

    print(da_pop_regrid.sum(("lat", "lon")))

    return da_pop_regrid


def compute_extremes_response(settings, data_directory):
    data_out = None

    for var, tail, perc in zip(settings["var_list"], settings["response_tail"], settings["response_threshold"]):
        print(f"computing extremes for {var}, {tail}, {perc}")

        settings.update({"var": var})
        data = file_handling.load_climate_data(settings, data_directory)
        da_response = xr.zeros_like(data)

        # define baseline months
        data_baseline = (
            data.loc[:, str(settings["baseline_years"][0]) : str(settings["baseline_years"][1]), :, :]
            .groupby("time.month")
            .mean(("member", "time"))
        )

        # get growing season mask
        if settings["growing_season_only"]:
            print("    naning out everything not in the growing season.")
            data_baseline = growing_season_mask(data_baseline, settings)

        # define anomalies based on monthly baselines, nan out non-growing seasons
        for month in np.arange(1, 13):
            data[:, data.time.dt.month == month, :, :] = (
                data[:, data.time.dt.month == month, :, :] - data_baseline[month - 1, :, :]
            )

        # define extremes based on percentiles
        # yes, i loop through month again, which is not necessary, but it is more understandable
        for month in np.arange(1, 13):
            da_month = data[:, data.time.dt.month == month, :, :]
            baseline_threshold = np.percentile(
                da_month.loc[:, str(settings["baseline_years"][0]) : str(settings["baseline_years"][1]), :, :],
                perc,
                axis=(0, 1),
            )

            if tail == "above":
                da_response[:, data.time.dt.month == month, :, :] = xr.where(da_month > baseline_threshold, 1.0, 0.0)
            elif tail == "below":
                da_response[:, data.time.dt.month == month, :, :] = xr.where(da_month < baseline_threshold, 1.0, 0.0)
            elif tail == "below_above":
                baseline_threshold_above = np.percentile(
                    da_month.loc[:, str(settings["baseline_years"][0]) : str(settings["baseline_years"][1]), :, :],
                    100.0 - perc,
                    axis=(0, 1),
                )

                da_response[:, data.time.dt.month == month, :, :] = xr.where(
                    (da_month < baseline_threshold) | (da_month > baseline_threshold_above), 1.0, 0.0
                )

                # da_response[:, data.time.dt.month == month, :, :] = xr.where(
                #     (da_month < baseline_threshold), 1.0, 0.0
                # )
            else:
                raise NotImplementedError

        if data_out is None:
            data_out = da_response
        else:
            data_out = data_out + da_response

    data_out = xr.where(data_out == len(settings["var_list"]), 1.0, 0.0)

    # WINDOW THE DATA OVER WINDOW LENGTHS WITHIN THE RESPONSE_YEARS_RANGE and TAKE THE MEAN
    # data_out = window_data_w_mean(data_out, settings)
    data_out = window_data_w_max(data_out, settings)

    return data_out


def compute_reanalysis_baseline(settings, data_directory, data_like):
    assert len(settings["var_list"]) == 1, "not implemented yet."
    var = settings["var_list"][0]

    print("loading the reanalysis data")
    settings.update({"var": var})
    data = file_handling.load_reanalysis_data(settings, data_directory, data_like)

    # define baseline months
    data_baseline = (
        data.loc[str(settings["baseline_years"][0]) : str(settings["baseline_years"][1]), :, :]
        .groupby("time.month")
        .mean("time")
    )

    # get growing season mask
    data_baseline = growing_season_mask(data_baseline, settings)

    return data_baseline


def compute_anomalies(settings, data_directory):
    assert len(settings["var_list"]) == 1, "not implemented yet."
    var = settings["var_list"][0]

    print("loading the data")
    settings.update({"var": var})
    data = file_handling.load_climate_data(settings, data_directory)

    # define baseline months
    data_baseline = (
        data.loc[:, str(settings["baseline_years"][0]) : str(settings["baseline_years"][1]), :, :]
        .groupby("time.month")
        .mean(("member", "time"))
    )

    # get growing season mask
    data_baseline = growing_season_mask(data_baseline, settings)

    # define anomalies based on monthly baselines
    for month in np.arange(1, 13):
        data[:, data.time.dt.month == month, :, :] = (
            data[:, data.time.dt.month == month, :, :] - data_baseline[month - 1, :, :]
        )

    # WINDOW THE DATA OVER WINDOW LENGTHS WITHIN THE RESPONSE_YEARS_RANGE and TAKE THE MEAN
    data = window_data_w_mean(data, settings)

    return data, data_baseline


def growing_season_mask(data, settings):
    # define growing enddates
    # grow_start, grow_stop = "plant.end", "harvest.start"
    grow_start, grow_stop = "plant", "harvest"
    # grow_start, grow_stop = "plant.start", "harvest.start"

    # get growing seasons
    da_grow, da_grow2 = get_growing_seasons_data(settings)

    # get the growing season months only
    all_months = np.arange(1, 13)

    # check longitudes and convert if necessary for the growing season data
    if np.min(data["lon"] >= 0):
        data_lon = (data["lon"].values + 180) % 360 - 180
    else:
        data_lon = data["lon"].values

    # loop through all gridpoints
    for ilat in range(len(data["lat"])):
        ilat_grab = np.argmin(np.abs(data["lat"][ilat].values - da_grow["latitude"].values))

        for ilon in range(len(data_lon)):
            ilon_grab = np.argmin(np.abs(data_lon[ilon] - da_grow["longitude"].values))

            # # get the growing season start and end for each gridpoint
            month_list = get_growing_month_list(
                da_grow[grow_start][ilat_grab, ilon_grab].values, da_grow[grow_stop][ilat_grab, ilon_grab].values
            )

            # check if there is a second growing season, if so, append months to the first season
            if da_grow2 is not None:
                month_list_second = get_growing_month_list(
                    da_grow2[grow_start][ilat_grab, ilon_grab].values,
                    da_grow2[grow_stop][ilat_grab, ilon_grab].values,
                )
                month_list = np.unique(np.append(month_list, month_list_second, axis=0).astype(int))

            # nan out the baseline for not the growing season
            month_mask = np.isin(all_months, month_list, assume_unique=True)
            data[~month_mask, ilat, ilon] = np.nan

    return data


def get_growing_month_list(start_doy, end_doy):
    try:
        start_month = datetime.datetime(2030, 1, 1) + datetime.timedelta(start_doy - 1)
        end_month = datetime.datetime(2030, 1, 1) + datetime.timedelta(end_doy - 1)

        start_month = start_month.month
        end_month = end_month.month
    except:
        start_month = np.nan
        end_month = np.nan

    # get list of month numbers
    if np.isnan(start_month) or np.isnan(end_month):
        month_list = []
    else:
        start_date = "2030-" + str(int(start_month)) + "-01"
        end_date = "2030-" + str(int(end_month)) + "-01"
        month_list = np.asarray(pd.date_range(start_date, end_date, freq="MS").strftime("%m").tolist(), dtype=int)

        if not np.any(month_list):
            end_date = "2031-" + str(int(end_month)) + "-01"
            month_list = np.asarray(pd.date_range(start_date, end_date, freq="MS").strftime("%m").tolist(), dtype=int)

    return month_list


def window_data_w_mean(data, settings):
    data = data.loc[
        {data.dims[1]: slice(str(settings["response_year_range"][0]), str(settings["response_year_range"][1]))}
    ]

    d = None
    response_years = np.unique(data["time.year"])
    for year in np.arange(response_years[0], response_years[-1] + 1, settings["window_len"]):
        if (year + settings["window_len"]) - 1 > response_years[-1]:
            break

        if d is None:
            d = (
                data.loc[{data.dims[1]: slice(str(year), str((year + settings["window_len"]) - 1))}]
                .mean(axis=1, skipna=True)
                .expand_dims({"window": np.arange(year, year + 1)})
            )

        else:
            d = xr.concat(
                [
                    d,
                    data.loc[{data.dims[1]: slice(str(year), str((year + settings["window_len"]) - 1))}]
                    .mean(axis=1, skipna=True)
                    .expand_dims({"window": np.arange(year, year + 1)}),
                ],
                dim="window",
            )

    return d.transpose("member", "window", "lat", "lon")


def window_data_w_max(data, settings):
    data = data.loc[
        {data.dims[1]: slice(str(settings["response_year_range"][0]), str(settings["response_year_range"][1]))}
    ]

    d = None
    response_years = np.unique(data["time.year"])
    for year in np.arange(response_years[0], response_years[-1] + 1, settings["window_len"]):
        if (year + settings["window_len"]) - 1 > response_years[-1]:
            break

        if d is None:
            d = (
                data.loc[{data.dims[1]: slice(str(year), str((year + settings["window_len"]) - 1))}]
                .max(axis=1, skipna=True)
                .expand_dims({"window": np.arange(year, year + 1)})
            )

        else:
            d = xr.concat(
                [
                    d,
                    data.loc[{data.dims[1]: slice(str(year), str((year + settings["window_len"]) - 1))}]
                    .max(axis=1, skipna=True)
                    .expand_dims({"window": np.arange(year, year + 1)}),
                ],
                dim="window",
            )

    return d.transpose("member", "window", "lat", "lon")


def get_growing_seasons_data(settings):
    if settings["product"] == "pdr":
        file = SEASONS_DIRECTORY + "Rice.crop.calendar.fill.nc"
        file2 = SEASONS_DIRECTORY + "Rice.2.crop.calendar.fill.nc"
    elif settings["product"] == "wht":
        file = SEASONS_DIRECTORY + "Wheat.Winter.crop.calendar.fill.nc"
        file2 = SEASONS_DIRECTORY + "Wheat.crop.calendar.fill.nc"
    elif settings["product"] == "gro":
        file = SEASONS_DIRECTORY + "Maize.crop.calendar.fill.nc"
        file2 = SEASONS_DIRECTORY + "Maize.2.crop.calendar.fill.nc"
    elif settings["product"] == "osd":
        file = SEASONS_DIRECTORY + "Soybeans.crop.calendar.fill.nc"
        file2 = None
    elif settings["product"] == "all":
        raise ValueError("there is not way to define a growing seasons across multiple crops.")
    else:
        raise NotImplementedError("no such file.")

    if file2 is None:
        return xr.load_dataset(file), None
    else:
        print("    loading two growing seasons")
        return xr.load_dataset(file), xr.load_dataset(file2)


def build_response_data(settings, data_directory):
    if settings["response_type"] == "extremes":
        data = compute_extremes_response(settings, data_directory)

    elif settings["response_type"] == "anomalies":
        data, data_baseline = compute_anomalies(settings, data_directory)
        # return data, data_baseline
        return data

    else:
        raise NotImplementedError("no such response_type")

    print("response data.shape = " + str(data.shape))

    return data


def process_member(settings, da):
    # SELECT DATA YEARS
    da = da.loc[str(settings["data_years"][0]) : str(settings["data_years"][1]), :, :]

    # CHOOSE AVERAGING FREQUENCY
    if settings["avg_frequency"] == "annual":
        da = da.groupby("time.year").mean("time")
    elif settings["avg_frequency"] == "month":
        pass
    else:
        raise NotImplementedError("no such avg_frequency")

    return da


def get_cropped_area_mask(CROP_DIRECTORY, settings):
    filename = CROP_DIRECTORY + settings["product"] + "_cropped_regrid_" + settings["gcm"] + ".nc"
    print("loading crop areas from " + filename)

    return xr.load_dataarray(filename)


def get_country_masks(settings, SHAPE_DIRECTORY, DATA_DIRECTORY):

    country_loadfile = SHAPE_DIRECTORY + "countries_10m_" + settings["gcm"] + ".nc"
    regs_shp = gpd.read_file(SHAPE_DIRECTORY + "20230301_gtapv11.shp")
    regs_shp = regs_shp.dissolve(by="REG", as_index=False).sort_values(by="GTAPID").reset_index(drop=True)

    if os.path.exists(country_loadfile):
        print("loading " + country_loadfile)
        mask_country = xr.load_dataarray(SHAPE_DIRECTORY + "countries_10m_" + settings["gcm"] + ".nc")
    else:
        pass_settings = {"gcm": settings["gcm"], "var": "tas", "n_members": 1, "data_years": (2020, 2040), "avg_frequency": "month"}

        da_all = file_handling.load_climate_data(pass_settings, DATA_DIRECTORY)
        mask_country = regionmask.mask_geopandas(regs_shp, da_all.lon, da_all.lat)
        mask_country.to_netcdf(SHAPE_DIRECTORY + "countries_10m_" + settings["gcm"] + ".nc")

    return mask_country, regs_shp


def get_ocean_mask(mask_country):
    return xr.where(np.isnan(mask_country), 1.0, np.nan)


def positive_values(x):
    return np.where(x > 0, x, np.nan)


def compute_global_mean(da):
    weights = np.cos(np.deg2rad(da.lat))
    weights.name = "weights"
    temp_weighted = da.weighted(weights)
    global_mean = temp_weighted.mean(("lon", "lat"), skipna=True)

    return global_mean


def compute_global_sum(da):
    weights = np.cos(np.deg2rad(da.lat))
    weights.name = "weights"
    temp_weighted = da.weighted(weights)
    global_sum = temp_weighted.sum(("lon", "lat"), skipna=True)

    return global_sum


def get_name_from_code(codes):
    da = pd.read_excel(LONGNAME_FILE, "regions")

    names = []
    for code_val in codes:
        i = np.where(da["GTAP Region Code"] == code_val)[0]
        names.append(da["Long Name"][i].values[0])

    if len(names) == 1:
        return names[0]
    else:
        return names


def map_to_shapefile(regs_shp, code):
    ishp = regs_shp[regs_shp["REG"] == code].index.to_numpy()[0]

    if ishp is None:
        raise NameError

    return ishp


def convert_lons(x):
    if x < 0:
        x = 360.0 + x
    return x


def get_closest_gridpoint(regs_shp, code, mask_country):
    country_centroid = regs_shp[regs_shp["REG"] == code].centroid
    ilat = np.argmin(np.abs(mask_country["lat"] - country_centroid.y.values[0]).values)
    ilon = np.argmin(np.abs(mask_country["lon"] - convert_lons(country_centroid.x.values[0])).values)

    return ilat, ilon


def create_country_mask(country_code, regs_shp, mask_country):
    ishp_reporter = map_to_shapefile(regs_shp, country_code)

    mask_reporter = xr.where(mask_country == ishp_reporter, 1.0, np.nan)
    if mask_reporter.max().values != 1.0:
        ilat, ilon = get_closest_gridpoint(regs_shp, country_code, mask_country)
        mask_reporter[ilat, ilon] = 1.0

    return mask_reporter
