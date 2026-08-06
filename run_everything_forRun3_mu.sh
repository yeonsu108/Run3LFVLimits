dnnpath=~/github/anti_NanoAODRun3/DNN/DNN_0715_v9.1_syst0804/muon/
datacardPrefix=datacards_0715_v9.1_syst_mu
#python3 prepareShapesAndCards.py -p ${dnnpath}/v12_2022_postprocess_2/ -o ${datacardPrefix}_2022 -xsecfile files_mu.yml -dataYear 2022
#python3 prepareShapesAndCards.py -p ${dnnpath}/v12_2022EE_postprocess_2/ -o ${datacardPrefix}_2022EE -xsecfile files_mu.yml -dataYear 2022EE
#python3 prepareShapesAndCards.py -p ${dnnpath}/v12_2023_postprocess_2/ -o ${datacardPrefix}_2023 -xsecfile files_mu.yml -dataYear 2023
#python3 prepareShapesAndCards.py -p ${dnnpath}/v12_2023BPix_postprocess_2/ -o ${datacardPrefix}_2023BPix -xsecfile files_mu.yml -dataYear 2023BPix
#python3 prepareShapesAndCards.py -p ${dnnpath}/v15_2024_postprocess_2/ -o ${datacardPrefix}_2024 -xsecfile files24_mu.yml -dataYear 2024
#
#python3 run_all_limits.py ${datacardPrefix}_2022
#python3 plotLimitsPerCategory.py -limitfolder ${datacardPrefix}_2022
#python3 printLimitLatexTable.py ${datacardPrefix}_2022 > out_${datacardPrefix}_2022.tex
#python3 run_all_impacts.py ${datacardPrefix}_2022
#
#python3 run_all_limits.py ${datacardPrefix}_2022EE
#python3 plotLimitsPerCategory.py -limitfolder ${datacardPrefix}_2022EE
#python3 printLimitLatexTable.py ${datacardPrefix}_2022EE > out_${datacardPrefix}_2022EE.tex
#python3 run_all_impacts.py ${datacardPrefix}_2022EE
#
#python3 run_all_limits.py ${datacardPrefix}_2023
#python3 plotLimitsPerCategory.py -limitfolder ${datacardPrefix}_2023
#python3 printLimitLatexTable.py ${datacardPrefix}_2023 > out_${datacardPrefix}_2023.tex
#python3 run_all_impacts.py ${datacardPrefix}_2023
#
#python3 run_all_limits.py ${datacardPrefix}_2023BPix
#python3 plotLimitsPerCategory.py -limitfolder ${datacardPrefix}_2023BPix
#python3 printLimitLatexTable.py ${datacardPrefix}_2023BPix > out_${datacardPrefix}_2023BPix.tex
#python3 run_all_impacts.py ${datacardPrefix}_2023BPix
#
#python3 run_all_limits.py ${datacardPrefix}_2024
#python3 plotLimitsPerCategory.py -limitfolder ${datacardPrefix}_2024
#python3 printLimitLatexTable.py ${datacardPrefix}_2024 > out_${datacardPrefix}_2024.tex
#python3 run_all_impacts.py ${datacardPrefix}_2024


datacardFolder=${datacardPrefix}_fullRun3
python3 prepareRun3Combine.py -o $datacardFolder \
    -p22     ${datacardPrefix}_2022\
    -p22EE   ${datacardPrefix}_2022EE \
    -p23     ${datacardPrefix}_2023 \
    -p23BPix ${datacardPrefix}_2023BPix \
    -p24     ${datacardPrefix}_2024 
python3 run_all_limits.py $datacardFolder
python3 plotLimitsPerCategory.py -limitfolder $datacardFolder
python3 printLimitLatexTable.py $datacardFolder > out_${datacardFolder}.tex
python3 run_all_impacts.py $datacardFolder
#python3 run_all_gatherFailedFits.py $datacardFolder
#python3 run_all_postfits.py $datacardFolder
#python3 plotLimitsInterpolation.py -limitfolder $datacardFolder
#python3 run_all_gof.py $datacardFolder
#
#python3 printPostfitLatexTable.py $datacardFolder
