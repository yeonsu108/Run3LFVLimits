import os, sys
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.kde import KDEUnivariate
import ROOT
from ROOT import *


def smoothing(hin, hnom):

    htmp = hin.Clone()
    htmp.SetDirectory(0)
    htmp.Divide(hnom)

    x_vals = np.arange(htmp.GetNbinsX())
    y_vals = np.zeros(htmp.GetNbinsX())

    for i in range(htmp.GetNbinsX()):
        y_vals[i] = htmp.GetBinContent(i+1)

    #local linear regression (locally weighted polynomial regression)
    lowess = sm.nonparametric.lowess
    smoothed_vals = np.zeros(y_vals.shape)
    smoothed_vals = lowess(y_vals, x_vals, frac=1./3, return_sorted=False)

    #print y_vals
    ##averaging smoothign
    #for i in range(htmp.GetNbinsX()):
    #  if i == 0: y_vals[i] = htmp.GetBinContent(i+1)
    #  elif i > 0 and i < htmp.GetNbinsX() - 1: y_vals[i] = (htmp.GetBinContent(i) + htmp.GetBinContent(i+1) + htmp.GetBinContent(i+2))/3
    #  elif i == htmp.GetNbinsX() - 1: y_vals[i] = (htmp.GetBinContent(i) + htmp.GetBinContent(i+1))/2

    #def kde_statsmodels_u(x, x_grid, bandwidth=0.2, **kwargs):
    #    """Univariate Kernel Density Estimation with Statsmodels"""
    #    kde = KDEUnivariate(x)
    #    kde.fit(bw=bandwidth, **kwargs)
    #    return kde.evaluate(x_grid)

    #print y_vals
    #smoothed_vals = kde_statsmodels_u(y_vals, x_vals, bandwidth=1.0)
    #print "smooth:", smoothed_vals


    for x_position in x_vals:
        hin.SetBinContent(int(x_position+1), max(0, smoothed_vals[x_position]*hnom.GetBinContent(int(x_position+1))))
        #hin.SetBinContent(x_position+1, max(0, y_vals[x_position]*hnom.GetBinContent(x_position+1)))
        #hin.SetBinContent(x_position+1, max(0, smoothed_vals[x_position]*hnom.GetBinContent(x_position+1)))

    return hin


def symmetrize(var, var_opp, nom):

    for xbin in range(var.GetNbinsX()):
        if xbin == 0: continue #test: skip first bin
        if nom.GetBinContent(xbin+1) == 0: ratio = 1.
        else:
            ratio = var.GetBinContent(xbin+1) / nom.GetBinContent(xbin+1)
            ratio_opp = var_opp.GetBinContent(xbin+1) / nom.GetBinContent(xbin+1)

            #symmetrize only if one-sided smooth1
            #if (ratio - 1.) * (ratio_opp - 1.) <= 0: continue

            #symmetrize only if stat error is larger than variation, symm4
            #if (var.GetBinContent(xbin+1) - nom.GetBinContent(xbin+1)) > var.GetBinError(xbin+1) and \
            #    (var_opp.GetBinContent(xbin+1) - nom.GetBinContent(xbin+1)) > var_opp.GetBinError(xbin+1):
            #    continue

            #if var.GetBinError(xbin+1) / var.GetBinContent(xbin+1) < 0.1 and \
            #    var_opp.GetBinError(xbin+1) / var_opp.GetBinContent(xbin+1) < 0.1:
            #    continue

            ratio_var = 1.

            if var_opp.GetBinContent(xbin+1) > 0: ratio_var = var.GetBinContent(xbin+1) / var_opp.GetBinContent(xbin+1)

            # max diff to 20%
            #nom_m_var = abs(nom.GetBinContent(xbin+1)-var.GetBinContent(xbin+1))
            #if nom_m_var / nom.GetBinContent(xbin+1) > 0.2:
            #    nom_m_var = 0.2 * nom.GetBinContent(xbin+1)
            #nom_m_var_opp = abs(nom.GetBinContent(xbin+1)-var_opp.GetBinContent(xbin+1))
            #if nom_m_var_opp / nom.GetBinContent(xbin+1) > 0.2:
            #    nom_m_var_opp = 0.2 * nom.GetBinContent(xbin+1)
            #diff = nom_m_var + nom_m_var_opp

            diff = abs(nom.GetBinContent(xbin+1)-var.GetBinContent(xbin+1)) + abs(nom.GetBinContent(xbin+1)-var_opp.GetBinContent(xbin+1))

            if ratio_var > 1.:
                var.SetBinContent(xbin+1, nom.GetBinContent(xbin+1) + diff/2.)
                if ratio > 1.2: var.SetBinContent(xbin+1, 1.2 * nom.GetBinContent(xbin+1))
            else:
                var.SetBinContent(xbin+1, nom.GetBinContent(xbin+1) - diff/2.)
                if ratio < 0.8: var.SetBinContent(xbin+1, 0.8 * nom.GetBinContent(xbin+1))
                if nom.GetBinContent(xbin+1) - diff/2. < 0.: var.SetBinContent(xbin+1, 0)

    return var

