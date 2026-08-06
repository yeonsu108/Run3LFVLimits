datacardFolder=$1
year=$2
#python prepareShapesAndCards.py -o $datacardFolder -xsecfile plotIt/configs/TOP-22-011/files.yml -dataYear $year -p /data1/users/minerva1993/work/lfv_production/LFVRun2/DNN/DNN_out_0424_genuineTau/${year}_postprocess_2/ #misID
python3 prepareShapesAndCards.py -o $datacardFolder -xsecfile plotIt/configs/TOP-22-011/files.yml -dataYear $year -p /data1/users/minerva1993/work/lfv_production/LFVRun2/DNN/DNN_out_0705/${year}_postprocess_2/
#python prepareShapesAndCards.py -o $datacardFolder -xsecfile plotIt/configs/TOP-22-011/files.yml -dataYear $year -p /data1/users/minerva1993/work/lfv_production/LFVRun2/DNN/DNN_out_0716/${year}_postprocess_2/
#python prepareShapesAndCards.py -o $datacardFolder -xsecfile plotIt/configs/TOP-22-011/files.yml -dataYear $year -p /data1/users/minerva1993/work/lfv_production/LFVRun2/nanoaodframe/v9_0714_1010_uforeweight_jesflav_v6_FF/${year}_postprocess_2/
python3 run_all_limits.py $datacardFolder
python3 plotLimitsPerCategory.py -limitfolder $datacardFolder
python3 printLimitLatexTable.py $datacardFolder > out_${datacardFolder}.tex
python3 run_all_impacts.py $datacardFolder
python3 plot_syst.py $datacardFolder
python3 run_all_gatherFailedFits.py $datacardFolder
python3 run_all_postfits.py $datacardFolder

#python printPostfitLatexTable.py $datacardFolder
#python get_postfit_scale.py $datacardFolder
