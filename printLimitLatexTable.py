import json, sys, os
import numpy as np
import math

limitfolder = sys.argv[1]
year = ""
#for y_ in ["2016pre", "2016post", "2017", "2018", "Run2"]:
for y_ in ["2022","2022EE","2023","2023BPix","2024","Run3"]:
    if y_ in limitfolder: year = y_
    if year == "Run3": year = "3"


# for limit rescaling if the signal Xsec inseted in combine was not 1 pb
#signal_Xsec = {'st_lfv_cs': 10.09, 'st_lfv_cv': 58.3, 'st_lfv_ct': 307.4, 'st_lfv_us': 86.49, 'st_lfv_uv': 414.5, 'st_lfv_ut': 1925}
# For SMEFTsim cross sections, but TT are always 2.69, 21.5, 129 for s, v, t
#signal_Xsec = {'st_lfv_cs': 6.4, 'st_lfv_cv': 41.0, 'st_lfv_ct': 225.2, 'st_lfv_us': 61.83, 'st_lfv_uv': 297.6, 'st_lfv_ut': 1401}
signal_Xsec = {'st_lfv_cs':7.863,'st_lfv_ct':266.815,'st_lfv_cv':48.967,'st_lfv_uv':376.644,'st_lfv_ut':1751.6,'st_lfv_us':79.226}

def calcXsec(signal, limits):
    xsec = list(np.around(np.array(limits) * signal_Xsec[signal], decimals=3))
    if len(xsec) == 1: result = str(xsec[0])
    else: result = str(xsec)
    return result

def calcWilson(limits):
    wilson = list(np.around(np.sqrt(limits), decimals=3))
    if len(wilson) == 1: result = str(wilson[0])
    else: result = str(wilson)
    return result


def calcBr(op, limits):
    out = []
    if op == "cs" or op == "us":
        out = 2 * np.array(limits) * (172.5**5) * 10**(-6) / (1.32 * 6144 * (math.pi**3))
    elif op == "cv" or op == "uv":
        out = 4 * np.array(limits) * (172.5**5) * 10**(-6) / (1.32 * 1536 * (math.pi**3))
    elif op == "ct" or op == "ut":
        out = 2 * np.array(limits) * (172.5**5) * 10**(-6) / (1.32 * 128*(math.pi**3))
    out = list(np.around(out, decimals=3))
    if len(out) == 1: result = str(out[0])
    else: result = str(out)
    return result

################
for_table = []
for signal in ['st_lfv_cs', 'st_lfv_cv', 'st_lfv_ct', 'st_lfv_us', 'st_lfv_uv', 'st_lfv_ut']:
  op = signal.split("_")[2]
  limits = json.loads(open(os.path.join(limitfolder, signal+'_limits.json')).read())
  limits = limits[""]
  #print(signal , op)
  nom = " & ".join([calcXsec(signal, [limits['observed']]) + ' (' + calcXsec(signal, [limits['expected']]) + ')', calcWilson([limits['observed']]) + ' (' + calcWilson([limits['expected']]) + ')',  calcBr(op, [limits['observed']]) + ' (' + calcBr(op, [limits['expected']]) + ')'])
  #print("nom : ", nom)
  for_table.append(nom)
  unc = " & ".join(['{\small ' + calcXsec(signal, limits['one_sigma']) + '}',\
                    '{\small ' + calcWilson(limits['one_sigma']) + '}',\
                    '{\small ' + calcBr(op, limits['one_sigma']) + '}'])
  #print("unc : ", unc)
  for_table.append(unc)

#print(len(for_table),for_table)


lfv_table = """
\\begin{{table}}[h!]
    \\centering
    \\renewcommand{{\\arraystretch}}{{1.4}}
    \\topcaption{{Table for Run {year} upper limits of LFV cross section ($\\sigma$), Wilson coefficient ($C_{{\\cPqt\\cPq\\mu\\tau}}$), and branching fraction for different types of interactions. Central probabilty intervals containing 68\\% of the expected upper limits are given in square brackets.}}
    \\resizebox{{1.\\hsize}}{{!}}{{
    \\begin{{tabular}}{{ccccc}}
        Interaction & Type & Obs. (exp.) $\\sigma$ (\\unit{{fb}}) & Obs. (exp.) $C_{{\\cPqt\\cPq\\mu\\tau}}\\slash\\Lambda^{{2}}$ ($\TeV^{{-2}}$) & Obs. (exp.) $\\mathcal{{B}}(\\tTomutauq) (10^{{-6}})$ \\\\ \\hline
        \\multirow{{6}}{{*}}{{$\\cPqt\\cPqu\\mu\\tau$}}
            & \\multirow{{2}}{{*}}{{Scalar}} & {lim6} \\\\ & & {lim7} \\\\
            & \\multirow{{2}}{{*}}{{Vector}} & {lim8} \\\\ & & {lim9} \\\\
            & \\multirow{{2}}{{*}}{{Tensor}} & {lim10} \\\\ & & {lim11} \\\\\\cline{{1-5}}
        \\multirow{{6}}{{*}}{{$\\cPqt\\cPqc\\mu\\tau$}}
            & \\multirow{{2}}{{*}}{{Scalar}} & {lim0} \\\\ & & {lim1} \\\\
            & \\multirow{{2}}{{*}}{{Vector}} & {lim2} \\\\ & & {lim3} \\\\
            & \\multirow{{2}}{{*}}{{Tensor}} & {lim4} \\\\ & & {lim5} \\\\
    \\end{{tabular}}
    }}
    \\label{{tab:{year}limit}}
\\end{{table}}
""".format(
lim0=for_table[0],
lim1=for_table[1],
lim2=for_table[2],
lim3=for_table[3],
lim4=for_table[4],
lim5=for_table[5],
lim6=for_table[6],
lim7=for_table[7],
lim8=for_table[8],
lim9=for_table[9],
lim10=for_table[10],
lim11=for_table[11],
year = year)
print(lfv_table)

