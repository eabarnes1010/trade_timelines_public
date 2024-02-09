"""Metrics

Functions
---------
get_metrics
"""
import numpy as np
import scipy.stats as stats

__author__ = "Elizabeth A. Barnes"
__date__ = "04 July 2023"


def stress_correlation(x, y):
    r = stats.spearmanr(x, y, nan_policy="omit").correlation
    if np.isnan(r):
        r = 0.0
    return r


def correlation_localimports(traded_stress, reporter_code, partner_code_list):
    ip = np.where(partner_code_list == reporter_code)[0]
    x = traded_stress[:, ip]

    ip = np.where(partner_code_list != reporter_code)[0]
    y = np.nansum(traded_stress[:, ip], axis=-1)

    return stress_correlation(x, y)


def correlation_toptwo(dollars, partners_stress):
    j = [list(dollars).index(i) for i in sorted(dollars, reverse=True)][:2]
    return stress_correlation(partners_stress[:, j[0]], partners_stress[:, j[1]])


def stress_fraction_ratios(total_stress, rep_stress, perc=75, frac=0.1):
    stress_fracratio_perc = np.nanpercentile(rep_stress, perc) / np.nanpercentile(
        total_stress, perc
    )
    if np.isnan(stress_fracratio_perc) or np.isinf(stress_fracratio_perc):
        stress_fracratio_perc = 0.0

    try:
        stress_fracratio = np.count_nonzero(rep_stress >= frac) / np.count_nonzero(
            total_stress >= frac
        )
    except:
        stress_fracratio = 0.0

    return stress_fracratio, stress_fracratio_perc


def variance_fraction(traded_stress, irep, reporter_code, partner_code_list):
    y = np.nansum(traded_stress[irep, :, :] * 100, axis=-1)

    i_self = np.where(partner_code_list == reporter_code)[0]
    y_noself = traded_stress[irep, :, :] * 100
    y_noself = np.delete(y_noself, i_self, axis=-1)
    y_noself = np.nansum(y_noself, axis=-1)

    # return np.sum(y_noself) / np.sum(y), np.var(y_noself) / np.var(y)
    return np.mean(y_noself / y), np.var(y_noself) / np.var(y)


# ORIGINAL VERSION OF CODE
# def variance_fraction(traded_stress, irep, reporter_code, partner_code_list):
#     y = np.nansum(traded_stress[irep, :, :] * 100, axis=-1)

#     x = traded_stress[irep, :, :] * 100
#     x_noself = traded_stress[irep, :, :] * 100
#     i_self = np.where(partner_code_list == reporter_code)[0]
#     x_noself = np.delete(x_noself, i_self, axis=-1)
#     x = x_noself

#     y_noself = traded_stress[irep, :, :] * 100
#     y_noself = np.delete(y_noself, i_self, axis=-1)
#     y_noself = np.nansum(y_noself, axis=-1)

#     # run computations
#     var_sum = 0
#     cov_sum = 0
#     for i in range(x.shape[-1]):
#         if np.isnan(np.var(x[:, i])):
#             continue
#         var_sum += np.var(x[:, i])

#         for j in range(i):
#             if np.isnan(np.var(x[:, j])):
#                 continue
#             cov_sum += np.cov(x[:, i], x[:, j])[0, 1]

#     # check that the variances add up correctly and are within 1% of each other
#     assert np.abs(np.var(y_noself) - (var_sum + 2 * cov_sum)) / np.var(y_noself) < 0.01

#     frac_noself = (var_sum + 2 * cov_sum) / np.var(y)

#     return frac_noself
