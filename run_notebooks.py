"""Execute all notebooks in clean kernels using this Python interpreter."""
from pathlib import Path
import os, sys, json, tempfile
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

EXPECTED = ['01_data_audit.ipynb','02_eda.ipynb','03_preprocessing.ipynb','04_baseline_logistic.ipynb','05_error_analysis.ipynb','06_final_evaluation.ipynb']
actual = sorted(p.name for p in (ROOT/'notebooks').glob('*.ipynb'))
if actual != EXPECTED: raise RuntimeError(f'Notebook inventory differs: {actual}')
with tempfile.TemporaryDirectory(prefix='is507-kernel-') as tmp:
    spec=Path(tmp)/'is507';spec.mkdir()
    (spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'IS507','language':'python'}))
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        print('Executing',path.name,flush=True)
        nb=nbformat.read(path,as_version=4)
        km=KernelManager(kernel_name='is507',kernel_spec_manager=KernelSpecManager(kernel_dirs=[tmp]))
        client=NotebookClient(nb,km=km,timeout=600,resources={'metadata':{'path':str(ROOT)}})
        try:
            client.execute()
        finally:
            if km.has_kernel: km.shutdown_kernel(now=True)
        nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
        nbformat.write(nb,path)
    print('All six notebooks executed successfully.',flush=True)
