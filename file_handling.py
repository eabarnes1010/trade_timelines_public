"""File handling.

Functions
---------

"""

import numpy as np
import pandas as pd
import xarray as xr
import gzip
import pickle
import os
import data_processing

DATA_DIRECTORY = "/Users/eabarnes/big_data/"
PROCESSED_DIRECTORY = "processed_data/"


def load_metrics(filename):
    with gzip.open(filename, "rb") as fp:
        reporter_code_list = pickle.load(fp)
        traded_stress = pickle.load(fp)
        unweighted_stress = pickle.load(fp)
        df_stress = pickle.load(fp)
        df_metrics = pickle.load(fp)

    return (
        reporter_code_list,
        traded_stress,
        unweighted_stress,
        df_stress,
        df_metrics,
    )


def save_metrics(
    filename,
    reporter_code_list,
    traded_stress,
    unweighted_stress,
    df_stress,
    df_metrics,
):
    with gzip.open(filename, "wb") as fp:
        pickle.dump(reporter_code_list, fp)
        pickle.dump(traded_stress, fp)
        pickle.dump(unweighted_stress, fp)
        pickle.dump(df_stress, fp)
        pickle.dump(df_metrics, fp)


def load_reanalysis_data(settings, DATA_DIRECTORY, data_like=None):
    da = xr.open_dataarray(DATA_DIRECTORY + "ERA5_t2m_mon_197901-202200.nc")[:, 0, :, :]
    da = da.rename({"latitude": "lat", "longitude": "lon"})
    da = da - 273.15

    if data_like is not None:
        da = da.interp_like(data_like)

    return da


def load_climate_data(settings, DATA_DIRECTORY):
    da_all = None

    # MPI -----------------------
    if settings["gcm"] == "mpi":
        for ens in range(settings["n_members"]):
            # get member
            member_text = f"{ens+1:03}"
            print("ensemble member = " + member_text)

            if settings["var"] == "mrsos":
                realm = "Lmon"
            else:
                realm = "Amon"

            filename_hist = (
                DATA_DIRECTORY
                + "mpi/"
                + settings["var"]
                + "_"
                + realm
                + "_MPI-ESM_historical_r"
                + member_text
                + "i1850p3_185001-200512.nc"
            )
            dah = xr.open_dataset(filename_hist)[settings["var"]].squeeze()
            dah = dah.resample(time="1M").mean()

            filename_ssp = (
                DATA_DIRECTORY
                + "mpi/"
                + settings["var"]
                + "_"
                + realm
                + "_MPI-ESM_rcp45_r"
                + member_text
                + "i2005p3_200601-209912.nc"
            )
            das = xr.open_dataset(filename_ssp)[settings["var"]].squeeze()
            das = das.resample(time="1M").mean()

            # CONCATENATE SCENARIOS
            da = xr.concat([dah, das], "time")

            # PROCESS THE ENSEMBLE MEMBER
            da = data_processing.process_member(settings, da)

            # CONCATENATE MEMBERS
            if da_all is None:
                da_all = da.expand_dims(dim="member")
            else:
                da_all = xr.concat([da_all, da], dim="member")

    # CESM2 -----------------------
    elif settings["gcm"] == "cesm2":
        inityears = [
            1001,
            1011,
            1021,
            1031,
            1041,
            1051,
            1061,
            1071,
            1081,
            1091,
            1101,
            1111,
            1121,
            1131,
            1141,
            1151,
            1161,
            1171,
            1181,
            1191,
            1231,
            1251,
            1281,
            1301,
        ]

        break_out_flag = False
        for start_text in ("CMIP6", "smbb"):

            if break_out_flag:
                break

            for iy in inityears:

                if break_out_flag:
                    break

                for ens in np.arange(0, 20):
                    member_text = f"{iy}.{ens+1:03}"
                    realm = "mon"
                    if settings["var"] == "tas":
                        var = "TREFHT"
                    elif settings["var"] == "pr":
                        var = "PRECT"

                    filename = (
                        DATA_DIRECTORY
                        + "cesm2_le/"
                        + realm
                        + "/"
                        + start_text
                        + ".LE2-"
                        + member_text
                        + "."
                        + var
                        + ".1850-2100.shifted.nc"
                    )
                    if not os.path.isfile(filename):
                        continue
                    print(filename)
                    da = xr.open_dataset(filename)[var].squeeze()
                    da = da.resample(time="1M").mean()

                    # PROCESS THE ENSEMBLE MEMBER
                    da = data_processing.process_member(settings, da)

                    # CONCATENATE MEMBERS
                    if da_all is None:
                        da_all = da.expand_dims(dim="member")
                    else:
                        da_all = xr.concat([da_all, da], dim="member")

                    if da_all.shape[0] > settings["n_members"]:
                        break_out_flag = True
                        break

    else:
        raise NotImplementedError()

    print("    da_shape = " + str(da_all.shape))

    return da_all
