postfix=0803
datacardFolder=fullRun2Comb_${postfix}
python3 prepareRun2Combine.py -o $datacardFolder \
    -p16pre  datacards_top_lfv_multiClass_Oct19_2023_2016pre \
    -p16post datacards_top_lfv_multiClass_Oct19_2023_2016post \
    -p17     datacards_top_lfv_multiClass_Oct19_2023_2017 \
    -p18     datacards_top_lfv_multiClass_Oct19_2023_2018
python3 run_all_limits.py $datacardFolder
python3 plotLimitsPerCategory.py -limitfolder $datacardFolder
python3 printLimitLatexTable.py $datacardFolder > out_${datacardFolder}.tex
python3 run_all_impacts.py $datacardFolder
python3 run_all_gatherFailedFits.py $datacardFolder
python3 run_all_postfits.py $datacardFolder
python3 plotLimitsInterpolation.py -limitfolder $datacardFolder
python3 run_all_gof.py $datacardFolder

python3 printPostfitLatexTable.py $datacardFolder
