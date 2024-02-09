"""Analysis functions.

Functions
---------

"""

import numpy as np
import pandas as pd
import xarray as xr
import os

import data_processing
import metrics
import file_handling

DATA_DIRECTORY = "/Users/eabarnes/big_data/"
GTAP_DATA_DIRECTORY = "data/GTAP_data/"
PROCESSED_DIRECTORY = "processed_data/"
SHAPE_DIRECTORY = "shapefiles/gadm_shapefiles_20230301_gtapv11/"
CROP_DIRECTORY = "data/cropland/regridded_cropland/"
PROCESSED_METRICS_DIRECTORY = "processed_metrics/"


def crop_name(product):
    if product == "pdr":
        cropname = "rice"
    elif product == "wht":
        cropname = "wheat"
    elif product == "gro":
        cropname = "maize"
    elif product == "osd":
        cropname = "soy"
    elif product == "all":
        cropname = "all"
    elif product == "calories":
        cropname = "calories"
    else:
        raise NotImplementedError("no such file.")

    return cropname


def fill_map(x, mask, value):
    if np.isscalar(value):
        return x + mask.fillna(0) * value
    else:
        return x + mask.fillna(0).expand_dims(dim={"sample": len(np.asarray(value))}) * value[:, np.newaxis, np.newaxis]


def replace_zeros(x, fill_value=np.nan):
    return xr.where(x == 0.0, fill_value, x)


def get_processed_metrics(data, settings, rewrite=False, save=True, calories=False):
    metrics_savename = PROCESSED_METRICS_DIRECTORY + settings["exp_name"] + "_processed_metrics.pickle"

    if os.path.isfile(metrics_savename) and not rewrite:
        print(f"   loading pre-saved data from {metrics_savename}")
        (
            reporter_code_list,
            traded_stress,
            unweighted_stress,
            df_stress,
            df_metrics,
        ) = file_handling.load_metrics(metrics_savename)

    else:
        (
            reporter_code_list,
            traded_stress,
            unweighted_stress,
            df_stress,
            df_metrics,
        ) = compute_cropstress_trade(data, settings)

        # save the data
        if save:
            print(f"   saving data to {metrics_savename}")
            file_handling.save_metrics(
                metrics_savename,
                reporter_code_list,
                traded_stress,
                unweighted_stress,
                df_stress,
                df_metrics,
            )

    return (
        reporter_code_list,
        traded_stress,
        unweighted_stress,
        df_stress,
        df_metrics,
    )


def get_trade_data(settings, convert_to_calories=False):
    # GET TRADE DATA
    assert settings["trade_data_year"] == 2017, "we only have data for 2017 from GTAPv11"

    print("reading trade data: " + GTAP_DATA_DIRECTORY + settings["gtap_filename"])
    data_trade = pd.read_csv(GTAP_DATA_DIRECTORY + settings["gtap_filename"])
    data_trade = pd.DataFrame(data_trade.fillna(0))

    # grab product of interest
    if (settings["product"] != "all") & (settings["product"] != "calories"):
        data_trade = data_trade[
            data_trade["COMM"].isin(
                [
                    settings["product"],
                ]
            )
        ].reset_index(drop=True)
    # print(data_trade.head())

    if convert_to_calories:
        for product in ("gro", "osd", "wht", "pdr"):
            data_trade.loc[data_trade["COMM"] == product, "TotValue"] = data_trade.TotValue * get_nutritive_factors(product)

    data_trade = data_trade.groupby(by=["Source", "Destination"]).sum("TotValue").reset_index()
    if not settings["include_self"]:
        data_trade = data_trade[data_trade["Source"] != data_trade["Destination"]].reset_index(drop=True)

    reporter_code_list = np.unique(data_trade["Destination"])
    reporter_code_list = np.delete(
        reporter_code_list, np.where(np.isin(reporter_code_list, settings["exclude_regions"]))[0]
    )
    print(f"{len(reporter_code_list) = }")

    n_partners = len(np.unique(data_trade["Source"]))
    print(f"{n_partners = }")

    # print(data_trade.head())

    return data_trade, reporter_code_list, n_partners


def compute_cropstress_trade(data, settings):
    return compute_cropstress_trade_percentage(data, settings)


def compute_cropstress_trade_percentage(data, settings):
    # get trade data
    data_trade, reporter_code_list, n_partners = get_trade_data(settings)

    # get masks
    mask_country, regs_shp = data_processing.get_country_masks(settings, SHAPE_DIRECTORY, DATA_DIRECTORY)

    # get cropped area
    da_crop_area = data_processing.get_cropped_area_mask(CROP_DIRECTORY, settings)

    # Initalize arrays and maps
    traded_stress = np.zeros((len(reporter_code_list), np.shape(data)[0], n_partners)) * np.nan
    unweighted_stress = np.zeros((len(reporter_code_list), np.shape(data)[0], n_partners)) * np.nan

    # START THE LOOP THROUGH REPORTERS
    reporter_code_summary = []
    metrics_dict = {}
    stress_dict = {}

    for irep, reporter_code in enumerate(reporter_code_list):
        # GET REPORTER DATA
        data_reporter = data_trade[data_trade["Destination"] == reporter_code]

        reporter_name = data_processing.get_name_from_code((data_reporter["Destination"].values[0],))
        reporter_import_dollars = data_reporter["TotValue"].sum()
        reporter_code_summary.append(reporter_code)
        print(f"{reporter_code}, {reporter_name}, ${reporter_import_dollars:.3f},", end=" ", flush=True)

        # GET PARTNER NAMES and DOLLARS
        dollars = data_reporter["TotValue"].values
        partner_code_list = data_reporter["Source"].values
        print(f"n_partners = {len(np.unique(partner_code_list))},", end=" ", flush=True)
        assert len(np.unique(partner_code_list)) == len(partner_code_list)

        # COMPUTE QUANTITIES
        for ip, partner_code in enumerate(partner_code_list):
            # partner_name = data_processing.get_name_from_code((partner_code,))

            if (
                partner_code == reporter_code and not settings["include_self"]
            ):  # do not look at the reporter itself (focused on imports)
                raise ValueError("something is not right")

            # compute trade fraction over the commodities of interest
            partner_trade_frac = dollars[ip] / reporter_import_dollars
            if partner_trade_frac == 0 or np.isin(partner_code, settings["exclude_regions"]):
                continue

            # find partner in shapefile dataframe for geographic points
            mask_partner = data_processing.create_country_mask(partner_code, regs_shp, mask_country)

            # further mask the partner and reporter by cropped area
            mask_partner_crop = mask_partner * da_crop_area
            # mask_reporter_crop = mask_reporter * da_crop_area

            # RESPONSE CALCULATIONS ACROSS MAPS over CROP AREA ONLY
            crop_response = data_processing.compute_global_sum(
                data * mask_partner_crop / data_processing.compute_global_sum(mask_partner_crop)
            )
            if np.isnan(crop_response[0]):
                continue

            traded_stress[irep, :, ip] = crop_response * partner_trade_frac
            unweighted_stress[irep, :, ip] = crop_response

        # SUMMARIZING METRICS
        total_stress = np.nansum(traded_stress[irep, :, :], axis=-1)
        corr_localimports = metrics.correlation_localimports(
            traded_stress[irep, :, :], reporter_code, partner_code_list
        )
        corr_toptwo = metrics.correlation_toptwo(dollars, traded_stress[irep, :, :])

        # FILL DICTIONARIES
        stress_dict[reporter_code] = total_stress
        metrics_dict[reporter_code] = {
            "corr_localtotal": corr_localimports,
            "corr_toptwo": corr_toptwo,
        }

        print(f"{corr_localimports = :.2f}, {corr_toptwo = :.2f}", end="\n", flush=True)

    return (
        reporter_code_list,
        traded_stress,
        unweighted_stress,
        pd.DataFrame(stress_dict).T,
        pd.DataFrame(metrics_dict).T,
    )


def get_moore_coefs(product):
    if product == "wht":
        coefs = [-5.59488, 1.8706, 0.16121, -0.18006]  # for wheat
    elif product == "gro":
        coefs = [3.71419, -0.88715, -0.40331, 0.03767]  # maize
    elif product == "pdr":
        coefs = [50.37358, -12.77784, -2.22263, 0.521]  # rice
    elif product == "osd":
        coefs = [-144.92566, 61.70978, 5.81824, -2.72308]  # soy
    else:
        raise NotImplementedError

    return coefs


def get_nutritive_factors(product):
    # data/nutritive_factors/20230921_NutritiveFactors.xlsx

    if product == "wht":
        factor = 13.14  # for wheat
    elif product == "gro":
        factor = 17.67  # maize
    elif product == "pdr":
        factor = 5.66  # rice
    elif product == "osd":
        factor = 8.08  # soy
    else:
        raise NotImplementedError

    return factor
