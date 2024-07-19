"""Experimental settings

Functions
---------
get_settings(experiment_name)
"""
import numpy as np

__author__ = "Elizabeth A. Barnes"
__date__ = "01 July 2023"

# ["pdr" = rice, "wht" = wheat, "gro" = maize, "osd" = soy, "all" = all four]


def get_settings(experiment_name):
    experiments = {

        "exp600": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "subexperiments": ("exp601", "exp602", "exp603", "exp604"),
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "calories",
        },

        "exp601": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },
        "exp602": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",  # maize
        },
        "exp603": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "var_list": ("tas", "pr"),
            "include_self": True,
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",  # rice
        },
        "exp604": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",  # soy
        },

        "exp500": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "subexperiments": ("exp501", "exp502", "exp503", "exp504"),
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "calories",
        },

        "exp501": {
            "presaved_processed_data": "exp501_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },

        "exp502": {
            "presaved_processed_data": "exp502_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",  # maize
        },
        "exp503": {
            "presaved_processed_data": "exp503_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "var_list": ("tas", "pr"),
            "include_self": True,
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",  # rice
        },
        "exp504": {
            "presaved_processed_data": "exp504_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",  # soy
        },

        "exp400": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "subexperiments": ("exp401", "exp402", "exp403", "exp404"),
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "calories",
        },

        "exp401": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },
        "exp402": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",  # maize
        },
        "exp403": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "var_list": ("tas", "pr"),
            "include_self": True,
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",  # rice
        },
        "exp404": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",  # soy
        },

        "exp300": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "subexperiments": ("exp301", "exp302", "exp303", "exp304"),
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "calories",
        },

        "exp301": {
            "presaved_processed_data": "exp201_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },

        "exp302": {
            "presaved_processed_data": "exp202_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",  # maize
        },
        "exp303": {
            "presaved_processed_data": "exp203_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "var_list": ("tas", "pr"),
            "include_self": True,
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",  # rice
        },
        "exp304": {
            "presaved_processed_data": "exp204_processed_data.nc",
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11b.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",  # soy
        },

        "exp200": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11a.csv",
            "subexperiments": ("exp201", "exp202", "exp203", "exp204"),
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "calories",
        },

        "exp201": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11a.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },

        "exp202": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11a.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",  # maize
        },
        "exp203": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11a.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "var_list": ("tas", "pr"),
            "include_self": True,
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",  # rice
        },
        "exp204": {
            "presaved_processed_data": None,
            "gtap_filename": "2024-01-04_GTAPdata_MUSD_v11a.csv",
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (2014, 2030),
            "baseline_years": (2015, 2024),  # inclusive
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "extremes",
            "include_self": True,
            "var_list": ("tas", "pr"),
            "response_year_range": (2025, 2025),  # inclusive
            "window_len": 1,
            "response_tail": ("above", "below_above"),
            "response_threshold": (95, 5),

            "trade_data_year": 2017,
            "growing_season_only": True,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",  # soy
        },

        #  ---------------------------------------------------------------
        # YIELDS - experiments 1000+
        "exp2001": {
            "presaved_processed_data": None,
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (1995, 2017),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },
        "exp2002": {
            "presaved_processed_data": None,
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",
        },

        "exp2003": {
            "presaved_processed_data": None,
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",
        },

        "exp2004": {
            "presaved_processed_data": None,
            "gcm": "cesm2",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",
        },

        "exp1001": {
            "presaved_processed_data": None,
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "wht",
        },

        "exp1002": {
            "presaved_processed_data": None,
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "gro",
        },

        "exp1003": {
            "presaved_processed_data": None,
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "pdr",
        },

        "exp1004": {
            "presaved_processed_data": None,
            "gcm": "mpi",

            "n_members": 100,
            "data_years": (1995, 2020),
            "baseline_years": (1995, 2005),
            "avg_frequency": "month",
            "rng_seed": 44,

            "response_type": "anomalies",
            "include_self": True,
            "var_list": ("tas",),
            "response_year_range": (2017, 2017),
            "window_len": 1,

            "trade_data_year": 2017,
            "exclude_regions": ("hkg", "xtw"),
            "product": "osd",
        },


    }

    exp_dict = experiments[experiment_name]
    exp_dict['exp_name'] = experiment_name

    return exp_dict
