"""Reproduce development and the frozen retrospective final test."""
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
subprocess.run([sys.executable,str(ROOT/'download_data.py')],check=True)
from src.analysis import audit,eda,preprocessing,modeling,errors
from src.final_evaluation import run as final_evaluation
from src.final_figures import run as final_figures
for stage in [audit,eda,preprocessing,modeling,errors,final_evaluation,final_figures]:
    print('Running',stage.__name__,flush=True)
    stage()
print('Analysis reproduced. Run run_notebooks.py to refresh all six saved notebooks.')
