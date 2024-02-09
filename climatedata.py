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


def get_climate_data(settings, rewrite, save):
    if settings["presaved_processed_data"] is None:
        filename = PROCESSED_DIRECTORY + settings["exp_name"] + "_processed_data.nc"
    else:
        filename = PROCESSED_DIRECTORY + settings["presaved_processed_data"]

    if os.path.exists(filename) and not rewrite:
        print(filename + ": loading saved data.")
        data = xr.open_dataarray(filename)
    else:
        data = data_processing.build_response_data(settings, DATA_DIRECTORY)
        if save:
            data.to_netcdf(filename)

    # STACK THE DATA (members x windows) INTO SAMPLES
    # the stacked data cannot be serialized, so we do this after the fact.
    data = data.stack(sample=("member", "window")).transpose("sample", "lat", "lon")
    print(f"final samples.shape = {data.shape}")

    return data


def get_reanalysis_baseline(settings, data_like=None):

    data_baseline = data_processing.compute_reanalysis_baseline(settings, DATA_DIRECTORY, data_like)
    print(f"{data_baseline.shape = }")
    return data_baseline
