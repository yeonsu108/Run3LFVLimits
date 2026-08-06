# LFVLimits

We base the toolbox on FCNC analysis limit toolbox.

Toolbox to derive upper limits for Run3 (2022, 2022EE, 2023, 2023BPix, and 2024) LFV TOP analysis
# Installation
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
scramv1 b clean; scramv1 b # always make a clean build

cd $CMSSW_BASE/src
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester
git checkout v3.0.0-pre1
scram b

cd -
mkdir UserCode
cd UserCode
git clone https://github.com/yeonsu108/Run3LFVLimits
cd $CMSSW_BASE/src
scram b -j 4

cd UserCode/Run3LFVLimits
git clone https://github.com/yeonsu108/plotIt.git
cd plotIt/external
source build-external.sh
cd ..
make -j6
```
# Stay up to date
You can check that the above recipe is up to date by following the links
https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/
and
https://cms-analysis.github.io/CombineHarvester/

# Run the limits
One line instruction:
`source run_everything_allYear.sh tag`

The `run_everything_allYear.sh` creates `datacards_20[16pre, 16post, 17, 18]_tag`, run limits, print limits, and run impacts.

**The input histogram path must be defined in** `run_everything_oneYear.sh`. You can use this to run a single year.


In detail:
Write the datacards and rootfiles suitable for combine (be careful that cross sections and sum of event weights are taken from `xsec.yml` and that for signal cross section is different than the one used in `plotIt`!)

`python prepareShapesAndCards.py -p /path/to/your/rootfiles`

Run combine to extract the limits

`python run_all_limits.py`

Plot the limits and print the values extrapolated to branching ratios

`python plotLimitsPerCategory.py`

All these python scripts are easily configurable, check what you can do with the `--help` option

To see how to do postfit plots, nuisance pulls, impacts, etc, have a look at the file: `run_everything_oneYear.sh`

You can also print limits in form of latex table with `printLimitLatexTable.py`

# To pay attention to

The signal cross section you use in 'xsec.yml' has to be propagated to `plotLimitsPerCategory.py` and to `printLimitLatexTable.py`. Note that `plotLimitsPerCategory.py` also needs the real, physical, expected signal cross section (for coupling one) to derive the limit on branching ratio.

# Script documentation

Script by script explanation (some might be slightly outdated or need minor modifications to adapt to different data taking year)

`convertPostfitShapesForPlotIt.py` makes the output of `combine` suitable for plotIt when deriving post-fit plots

`plotLimitsPerCategory.py` stores limit values inside a json file and makes the plot with limits on signal cross section per jet category and with all jet categories combined

`prepareShapesAndCards.py` based on the TH1 obtained from `gather_th1_for_limits.py`, writes datacards and rootfiles to feed combine (taking care of systematics, rescaling to lumi\*Xsec/Nevent, etc). This code also writes several bash script to derive the limits with combine, perform the pre-approval checks (pulls and impact of systematics), post-fit shapes, ...

`printLimitLatexTable.py` print a latex pre-formatted table with limits taken from the json file produced by `plotLimitsPerCategory.py`

`run_all_impacts.py`, `run_all_limits.py`, `run_all_postfits.py` scripts used to automatize the full chain. It launches the various combine commands in the bash scripts written by `prepareShapesAndCards.py`

`run_withoutPrepCard.sh` same then `run_everything_for2016/7/8.sh` but without the datacard writing part

`setTDRStyle.C` used to be compliant with CMS style guidelines (used in `plotLimitsPerCategory.py`)

All the `xsec.yml` contain the cross section and number of generated events used by `prepareShapesAndCards.py` to apply proper normalization before limit setting

`update_an.sh` script used to automatize the update of the AN after generating new limits (writes the latex table with limits in the AN, change the limits and psotfit plots, etc). It has to be updated to whatever format will be decided for AN combining 2017 and 2018.


# Run 2 combination
One line:
`source run_everything_forRun3.sh tag`

In detail:
`run_everything_forRun3.sh` read datacards defined as `-p22/-p22EE/-p23/-p23BPix/-p24` and generate output folder with merged datacards. Then run limit, pull, impact in the directory

