import os, sys
from subprocess import call

print ("Usage: python run_all_postfits.py datacard_folder (optional: 1617/1718/161718)")

current_dir = os.getcwd()
datacard_path = sys.argv[1]

try:
    if any(i in sys.argv[2] for i in ['1617','1718','161718']): years = sys.argv[2]
except: years = ''

signal_folders = [folder for folder in os.listdir(datacard_path) if os.path.isdir(os.path.join(datacard_path, folder))]
if not signal_folders:
    print ("Found no signal directory inside %s"%datacard_path)
for signal_folder in signal_folders:
    os.chdir(os.path.join(datacard_path, signal_folder))
    postfit_scripts = [postfit_script for postfit_script in os.listdir(".") if postfit_script.endswith('_run_postfit.sh')]
    if len(years) > 1:
        postfit_scripts = [x for x in postfit_scripts if '_'+years+'_' in x]
        limit_scripts = [limit_script for limit_script in os.listdir(".") if limit_script.endswith('_run_limits.sh')]
        limit_scripts = [x for x in limit_scripts if '_'+years+'_' in x]
        for limit_script in limit_scripts:
            print ("Executing %s"%limit_script)
            call(['bash', limit_script])
    if not postfit_scripts:
        print ("Found no limit script in directory %s"%os.path.join(datacard_path, signal_folder))
    for postfit_script in postfit_scripts:
        print ("Executing %s"%postfit_script)
        call(['bash', postfit_script])
    os.chdir(current_dir)
