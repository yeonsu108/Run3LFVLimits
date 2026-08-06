import json, sys, os, argparse
from math import sqrt
from array import array
from ROOT import *
import numpy as np
import math
from collections import OrderedDict
gROOT.SetBatch()
gROOT.ProcessLine(".x setTDRStyle.C")

parser = argparse.ArgumentParser(description='Store limits inside a json file and plot them if required (one bin per category).')
parser.add_argument('-limitfolder', dest='limitfolder', default='./datacards', type=str, help='Folder where ct and ut combine output folders are stored')
parser.add_argument('--unblind', dest='unblind', action='store_true', default=True, help='Display or not the observed limit.')
parser.add_argument('--lumi', dest='lumi', type=str, default='138', help='Luminosity to display on the plot.')
parser.add_argument('--pas', dest='pas', type=bool, default=True, help='To present Preliminary label')

options = parser.parse_args()
print options.limitfolder

postfix = ''

#signal_Xsec = {'st_lfv_cs': 6.4, 'st_lfv_cv': 41.0, 'st_lfv_ct': 225.2, 'st_lfv_us': 61.83, 'st_lfv_uv': 297.6, 'st_lfv_ut': 1401}
signal_Xsec = {'st_lfv_cs':7.863,'st_lfv_ct':266.815,'st_lfv_cv':48.967,'st_lfv_uv':376.644,'st_lfv_ut':1751.6,'st_lfv_us':79.226}
signal_lorentz_dict = OrderedDict()
#signal_lorentz_dict = {'s': kRed+1, 'v': kGreen+2, 't': kBlue+1}
signal_lorentz_dict['s'] = kRed+1
signal_lorentz_dict['v'] = kGreen+2
signal_lorentz_dict['t'] = kBlue+1
#signal_lorentz_dict = {'t': kBlue+1}

def calcWilson(limits):
    wilson = np.sqrt(limits)
    return wilson

def calcBr(op, limits):
    if op == "cs" or op == "us":
        out = 2 * limits * (172.5**5) * 10**(-6) / (1.32 * 6144 * (math.pi**3))
    elif op == "cv" or op == "uv":
        out = 4 * limits * (172.5**5) * 10**(-6) / (1.32 * 1536 * (math.pi**3))
    elif op == "ct" or op == "ut":
        out = 2 * limits * (172.5**5) * 10**(-6) / (1.32 * 128*(math.pi**3))
    return out

x_coup_exp = {}; y_coup_exp = {}
x_coup_obs = {}; y_coup_obs = {}
x_coup_one_up = {}; x_coup_one_dn = {}
y_coup_one_up = {}; y_coup_one_dn = {}
x_br_exp = {}; y_br_exp = {}
x_br_obs = {}; y_br_obs = {}
x_br_one_up = {}; x_br_one_dn = {}
y_br_one_up = {}; y_br_one_dn = {}

ut_exp = {}; ut_obs = {}; ut_one_up = {}; ut_one_dn = {}
ct_exp = {}; ct_obs = {}; ct_one_up = {}; ct_one_dn = {}

for signal_lorentz in signal_lorentz_dict:
    ut_limits = json.loads(open(os.path.join(options.limitfolder, 'st_lfv_u' + signal_lorentz + '_limits.json')).read())
    ct_limits = json.loads(open(os.path.join(options.limitfolder, 'st_lfv_c' + signal_lorentz + '_limits.json')).read())

    x_coup_exp[signal_lorentz], y_coup_exp[signal_lorentz] = array( 'd' ), array( 'd' )
    x_coup_obs[signal_lorentz], y_coup_obs[signal_lorentz] = array( 'd' ), array( 'd' )
    x_coup_one_up[signal_lorentz], x_coup_one_dn[signal_lorentz] = array( 'd' ), array( 'd' )
    y_coup_one_up[signal_lorentz], y_coup_one_dn[signal_lorentz] = array( 'd' ), array( 'd' )
    x_br_exp[signal_lorentz], y_br_exp[signal_lorentz] = array( 'd' ), array( 'd' )
    x_br_obs[signal_lorentz], y_br_obs[signal_lorentz] = array( 'd' ), array( 'd' )
    x_br_one_up[signal_lorentz], x_br_one_dn[signal_lorentz] = array( 'd' ), array( 'd' )
    y_br_one_up[signal_lorentz], y_br_one_dn[signal_lorentz] = array( 'd' ), array( 'd' )

    ut_exp[signal_lorentz] = ut_limits[""]['expected']
    ut_obs[signal_lorentz] = ut_limits[""]['observed']
    ut_one_up[signal_lorentz] = ut_limits[""]['one_sigma'][1]
    ut_one_dn[signal_lorentz] = ut_limits[""]['one_sigma'][0]

    ct_exp[signal_lorentz] = ct_limits[""]['expected']
    ct_obs[signal_lorentz] = ct_limits[""]['observed']
    ct_one_up[signal_lorentz] = ct_limits[""]['one_sigma'][1]
    ct_one_dn[signal_lorentz] = ct_limits[""]['one_sigma'][0]

def coupl(ut_limit, ct_limit, pos, arrX, arrY, to_print):
    if pow(pos, 2) <= ut_limit:
        coupling = sqrt(ct_limit * (1 - pow(pos, 2)/ut_limit))
        arrX.append(pos)
        arrY.append(coupling)
        if to_print: print pos, ' : coupling -> ', coupling

def br(op, ut_limit, ct_limit, pos, arrX, arrY, to_print):
    if pow(pos, 2) <= ut_limit:
        coupling = sqrt(ct_limit * (1 - pow(pos, 2)/ut_limit))
        br_x = calcBr(op, pow(pos, 2))
        br_y = calcBr(op, pow(coupling, 2))
        #arrX.append(np.around(br_x, decimals=5))
        #arrY.append(np.around(br_y, decimals=5))
        arrX.append(br_x)
        arrY.append(br_y)
        #if to_print: print pos, ' : br -> ', 10**-6 * br_x, 10**-6 * br_y
        if to_print: print pos, op, ' : br -> ', br_x, br_y


for i in range(200000):
    x_pos = 0.0001 * i
    #x_pos = 0.000005 * i

    to_print = False
    #if (x_pos * 400).is_integer(): to_print = True

    for signal_lorentz in signal_lorentz_dict:
        coupl(ut_exp[signal_lorentz], ct_exp[signal_lorentz], x_pos, x_coup_exp[signal_lorentz], y_coup_exp[signal_lorentz], to_print)

        br('u'+signal_lorentz, ut_exp[signal_lorentz], ct_exp[signal_lorentz], x_pos, x_br_exp[signal_lorentz], y_br_exp[signal_lorentz], to_print)


#Unc band requires high gran.
for i in range(200000):
    x_pos = 0.000005 * i

    to_print = False
    #if (x_pos * 400).is_integer(): to_print = True

    for signal_lorentz in signal_lorentz_dict:
        coupl(ut_obs[signal_lorentz], ct_obs[signal_lorentz], x_pos, x_coup_obs[signal_lorentz], y_coup_obs[signal_lorentz], to_print)
        coupl(ut_one_up[signal_lorentz], ct_one_up[signal_lorentz], x_pos, x_coup_one_up[signal_lorentz], y_coup_one_up[signal_lorentz], to_print)
        coupl(ut_one_dn[signal_lorentz], ct_one_dn[signal_lorentz], x_pos, x_coup_one_dn[signal_lorentz], y_coup_one_dn[signal_lorentz], to_print)

        br('u'+signal_lorentz, ut_obs[signal_lorentz], ct_obs[signal_lorentz], x_pos, x_br_obs[signal_lorentz], y_br_obs[signal_lorentz], to_print)
        br('u'+signal_lorentz, ut_one_up[signal_lorentz], ct_one_up[signal_lorentz], x_pos, x_br_one_up[signal_lorentz], y_br_one_up[signal_lorentz], to_print)
        br('u'+signal_lorentz, ut_one_dn[signal_lorentz], ct_one_dn[signal_lorentz], x_pos, x_br_one_dn[signal_lorentz], y_br_one_dn[signal_lorentz], to_print)


margin_left = 0.16
margin_right = 0.04
margin_top = 0.065
margin_bottom = 0.135

##########################################
#           Wilson coefficient           #
##########################################
g_coup_exp = {}; g_coup_obs = {}
g_coup_one_band = {};

# Create Canvas
c1 = TCanvas("c1", "interpolate", 450, 450)
c1.SetLeftMargin(margin_left)
c1.SetRightMargin(margin_right)
c1.SetTopMargin(margin_top)
c1.SetBottomMargin(margin_bottom)

p1 = c1.DrawFrame(0, 0.002, 0.3, 1.4)

# Create TGraph
for signal_lorentz in signal_lorentz_dict:
    g_coup_exp[signal_lorentz] = TGraph(len(x_coup_exp[signal_lorentz]), x_coup_exp[signal_lorentz], y_coup_exp[signal_lorentz])
    g_coup_obs[signal_lorentz] = TGraph(len(x_coup_obs[signal_lorentz]), x_coup_obs[signal_lorentz], y_coup_obs[signal_lorentz])
    print 'ut obs Wilson ',  x_coup_obs[signal_lorentz][-1], 'ct obs kappa', y_coup_obs[signal_lorentz][0]
    print 'ut exp Wilson ',  x_coup_exp[signal_lorentz][-1], 'ct exp kappa', y_coup_exp[signal_lorentz][0]
    print 'ut exp +1sig Wilson ',  x_coup_one_up[signal_lorentz][-1], 'ct exp kappa', y_coup_one_up[signal_lorentz][0]
    print 'ut exp -1sig Wilson ',  x_coup_one_dn[signal_lorentz][-1], 'ct exp kappa', y_coup_one_dn[signal_lorentz][0]

    g_coup_one_band[signal_lorentz] = TGraph(len(x_coup_one_up[signal_lorentz])+len(x_coup_one_dn[signal_lorentz]))
    for i in range(len(x_coup_one_up[signal_lorentz])):
        g_coup_one_band[signal_lorentz].SetPoint(i, x_coup_one_up[signal_lorentz][i], y_coup_one_up[signal_lorentz][i]);
        if len(x_coup_one_up[signal_lorentz]) + i < len(x_coup_one_up[signal_lorentz])+len(x_coup_one_dn[signal_lorentz]):
            g_coup_one_band[signal_lorentz].SetPoint(len(x_coup_one_up[signal_lorentz]) + i , x_coup_one_dn[signal_lorentz][len(x_coup_one_dn[signal_lorentz])-i-1], y_coup_one_dn[signal_lorentz][len(x_coup_one_dn[signal_lorentz])-i-1]);


    # Change style
    g_coup_exp[signal_lorentz].SetLineColor(signal_lorentz_dict[signal_lorentz])
    g_coup_exp[signal_lorentz].SetLineWidth(3)
    g_coup_exp[signal_lorentz].SetLineStyle(2)
    g_coup_obs[signal_lorentz].SetLineColor(signal_lorentz_dict[signal_lorentz])
    g_coup_obs[signal_lorentz].SetLineWidth(3)
    if not options.unblind:
        g_coup_obs[signal_lorentz].SetLineColorAlpha(kRed, 0.0);
    g_coup_one_band[signal_lorentz].SetFillColorAlpha(signal_lorentz_dict[signal_lorentz], 0.3)
    g_coup_one_band[signal_lorentz].SetLineWidth(0)


# Axis style
xAxis = p1.GetXaxis()
xAxis.SetTitle("C_{tu#mu#tau}/#Lambda^{2} (TeV^{-2})")
xAxis.SetLabelSize(20)
xAxis.SetLabelFont(43)
xAxis.SetLabelOffset(0.007)
xAxis.SetTitleFont(43)
xAxis.SetTitleOffset(1.0)
xAxis.SetTitleSize(22)
xAxis.SetTickLength(0.03)
yAxis = p1.GetYaxis()
yAxis.SetTitle("C_{tc#mu#tau}/#Lambda^{2} (TeV^{-2})")
yAxis.SetLabelSize(20)
yAxis.SetLabelFont(43)
yAxis.SetLabelOffset(0.012)
yAxis.SetTitleFont(43)
yAxis.SetTitleOffset(1.4)
yAxis.SetTitleSize(22)
yAxis.SetTickLength(0.03)


# Some text
progress = 'Preliminary'
latexLabel = TLatex()
latexLabel.SetNDC()
#Lumi
latexLabel.SetTextFont(62) # helvetica
latexLabel.SetTextSize(0.8 * margin_top)
latexLabel.SetTextAlign(33)
latexLabel.DrawLatex(1 - margin_right, 1 - 0.05 * margin_top, '%s fb^{-1} (13 TeV)'%(options.lumi))
#CMS
latexLabel.SetTextFont(62) # helvetica bold face
latexLabel.SetTextSize(0.9 * margin_top)
latexLabel.SetTextAlign(11)
latexLabel.DrawLatex(1.248 * margin_left, 0.865, "CMS")
#legend
latexLabel.SetTextFont(62)
latexLabel.SetTextSize(0.6 * c1.GetTopMargin())
#latexLabel.DrawLatex(0.57, 0.88, "CLFV    Exp #pm 1#sigma   Obs")
latexLabel.DrawLatex(0.57, 0.88, "CLFV   68% exp.   Obs.")
latexLabel.SetTextFont(42)
latexLabel.DrawLatex(0.57, 0.84, "Scalar")
latexLabel.DrawLatex(0.57, 0.80, "Vector")
latexLabel.DrawLatex(0.57, 0.76, "Tensor")
latexLabel.DrawLatex(0.57, 0.715, "95% CL upper limits")

if options.pas:
    latexLabel.SetTextFont(52) # helvetica italics
    latexLabel.SetTextSize(0.5 * c1.GetTopMargin())
    latexLabel.DrawLatex(1.21 * margin_left, 0.833, progress)

latexLabel.Clear()


# Legend
legend = TLegend(0.7, 0.75, 0.94, 0.87)
legend.SetNColumns(2)
legend.SetColumnSeparation(0.05)
legend.SetMargin(1.0)
legend.SetTextFont(42)
legend.SetTextColor(kWhite)
legend.SetFillStyle(0)
legend.SetLineColor(kWhite)

for signal_lorentz in signal_lorentz_dict:

    g_coup_one_band[signal_lorentz].Draw("f same")
    g_coup_obs[signal_lorentz].Draw("c same")
    g_coup_exp[signal_lorentz].Draw("c same")

    g_coup_one_band[signal_lorentz].SetLineColorAlpha(signal_lorentz_dict[signal_lorentz], 1.0)
    g_coup_one_band[signal_lorentz].SetLineStyle(2)
    g_coup_one_band[signal_lorentz].SetLineWidth(2)
    legend.AddEntry(g_coup_one_band[signal_lorentz], '.', 'lf')
    legend.AddEntry(g_coup_obs[signal_lorentz], '.', 'l')

gPad.RedrawAxis();
legend.Draw('same')
c1.cd()
if options.pas:
    c1.Print(options.limitfolder + "/interpolated_coupling"+postfix+"_pas.pdf")
    c1.Print(options.limitfolder + "/interpolated_coupling"+postfix+"_pas.png")
else:
    c1.Print(options.limitfolder + "/interpolated_coupling"+postfix+".pdf")
    c1.Print(options.limitfolder + "/interpolated_coupling"+postfix+".png")

##########################################
#           branching fraction           #
##########################################
g_br_exp = {}; g_br_obs = {}
g_br_one_band = {};

c2 = TCanvas("c2", "interpolate", 450, 450)
c2.SetLeftMargin(margin_left)
c2.SetRightMargin(margin_right)
c2.SetTopMargin(margin_top)
c2.SetBottomMargin(margin_bottom)

p2 = c2.DrawFrame(0, 0.001, 0.27, 4.7)
#TGaxis.SetMaxDigits(2)
#TGaxis.SetExponentOffset(-0.03, -0.04, "x");
#TGaxis.SetExponentOffset(-0.07, 0.0, "y");

# Create TGraph
for signal_lorentz in signal_lorentz_dict:
    g_br_exp[signal_lorentz] = TGraph(len(x_br_exp[signal_lorentz]), x_br_exp[signal_lorentz], y_br_exp[signal_lorentz])
    g_br_obs[signal_lorentz] = TGraph(len(x_br_obs[signal_lorentz]), x_br_obs[signal_lorentz], y_br_obs[signal_lorentz])

    g_br_one_band[signal_lorentz] = TGraph(len(x_br_one_up[signal_lorentz])+len(x_br_one_dn[signal_lorentz]))
    for i in range(len(x_br_one_up[signal_lorentz])):
        g_br_one_band[signal_lorentz].SetPoint(i, x_br_one_up[signal_lorentz][i], y_br_one_up[signal_lorentz][i]);
        if len(x_br_one_up[signal_lorentz]) + i < len(x_br_one_up[signal_lorentz])+len(x_br_one_dn[signal_lorentz]):
            g_br_one_band[signal_lorentz].SetPoint(len(x_br_one_up[signal_lorentz]) + i , x_br_one_dn[signal_lorentz][len(x_br_one_dn[signal_lorentz])-i-1], y_br_one_dn[signal_lorentz][len(x_br_one_dn[signal_lorentz])-i-1]);


    # Change style
    g_br_exp[signal_lorentz].SetLineColor(signal_lorentz_dict[signal_lorentz])
    g_br_exp[signal_lorentz].SetLineWidth(3)
    g_br_exp[signal_lorentz].SetLineStyle(2)
    g_br_obs[signal_lorentz].SetLineColor(signal_lorentz_dict[signal_lorentz])
    g_br_obs[signal_lorentz].SetLineWidth(3)
    if not options.unblind:
        g_br_obs[signal_lorentz].SetLineColorAlpha(kRed, 0.0);
    g_br_one_band[signal_lorentz].SetFillColorAlpha(signal_lorentz_dict[signal_lorentz], 0.3)
    g_br_one_band[signal_lorentz].SetLineWidth(0)


# Axis style
xAxis = p2.GetXaxis()
xAxis.SetTitle("B(t#rightarrow #mu#tau u) #times 10^{-6}")
xAxis.SetLabelSize(20)
xAxis.SetLabelFont(43)
xAxis.SetLabelOffset(0.007)
xAxis.SetTitleFont(43)
xAxis.SetTitleOffset(1.0)
xAxis.SetTitleSize(22)
xAxis.SetTickLength(0.03)
yAxis = p2.GetYaxis()
yAxis.SetTitle("B(t#rightarrow #mu#tau c) #times 10^{-6}")
yAxis.SetLabelSize(20)
yAxis.SetLabelFont(43)
yAxis.SetLabelOffset(0.012)
yAxis.SetTitleFont(43)
yAxis.SetTitleOffset(1.4)
yAxis.SetTitleSize(22)
yAxis.SetTickLength(0.03)


# Some text
progress = 'Preliminary'
latexLabel = TLatex()
latexLabel.SetNDC()
#Lumi
latexLabel.SetTextFont(62) # helvetica
latexLabel.SetTextSize(0.8 * margin_top)
latexLabel.SetTextAlign(33)
latexLabel.DrawLatex(1 - margin_right, 1 - 0.05 * margin_top, '%s fb^{-1} (13 TeV)'%(options.lumi))
#CMS
latexLabel.SetTextFont(62) # helvetica bold face
latexLabel.SetTextSize(0.9 * margin_top)
latexLabel.SetTextAlign(11)
latexLabel.DrawLatex(1.248 * margin_left, 0.865, "CMS")
#legend
latexLabel.SetTextFont(62)
latexLabel.SetTextSize(0.6 * c1.GetTopMargin())
#latexLabel.DrawLatex(0.57, 0.88, "CLFV    Exp #pm 1#sigma   Obs")
latexLabel.DrawLatex(0.57, 0.88, "CLFV   68% exp.   Obs.")
latexLabel.SetTextFont(42)
latexLabel.DrawLatex(0.57, 0.84, "Scalar")
latexLabel.DrawLatex(0.57, 0.80, "Vector")
latexLabel.DrawLatex(0.57, 0.76, "Tensor")
latexLabel.DrawLatex(0.57, 0.715, "95% CL upper limits")

if options.pas:
    latexLabel.SetTextFont(52) # helvetica italics
    latexLabel.SetTextSize(0.5 * c1.GetTopMargin())
    latexLabel.DrawLatex(1.21 * margin_left, 0.833, progress)

latexLabel.Clear()


# Legend
legend.Clear()
legend.SetColumnSeparation(0.05)
legend.SetMargin(1.0)
legend.SetTextFont(42)
legend.SetTextColor(kWhite)
legend.SetFillStyle(0)
legend.SetLineColor(kWhite)

for signal_lorentz in signal_lorentz_dict:

    g_br_one_band[signal_lorentz].Draw("f same")
    g_br_obs[signal_lorentz].Draw("c same")
    g_br_exp[signal_lorentz].Draw("c same")

    g_br_one_band[signal_lorentz].SetLineColorAlpha(signal_lorentz_dict[signal_lorentz], 1.0)
    g_br_one_band[signal_lorentz].SetLineStyle(2)
    g_br_one_band[signal_lorentz].SetLineWidth(2)
    legend.AddEntry(g_br_one_band[signal_lorentz], '.', 'lf')
    legend.AddEntry(g_br_obs[signal_lorentz], '.', 'l')

gPad.RedrawAxis();
legend.Draw('same')

if options.pas:
    c2.Print(options.limitfolder + "/interpolated_br"+postfix+"_pas.pdf")
    c2.Print(options.limitfolder + "/interpolated_br"+postfix+"_pas.png")
else:
    c2.Print(options.limitfolder + "/interpolated_br"+postfix+".pdf")
    c2.Print(options.limitfolder + "/interpolated_br"+postfix+".png")
