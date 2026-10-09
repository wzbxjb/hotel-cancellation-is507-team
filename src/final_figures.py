"""Scientific diagnostic plots from frozen, saved test predictions."""
import numpy as np
import pandas as pd
import os
from .utils import ROOT
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.calibration import calibration_curve
from .utils import ROOT

def run():
    d=pd.read_csv(ROOT/'data/processed/final_test_predictions.csv')
    y,p=d.is_canceled,d.p_primary
    fpr,tpr,_=roc_curve(y,p)
    pd.DataFrame({'fpr':fpr,'tpr':tpr}).to_csv(ROOT/'tables/final_test_roc.csv',index=False)
    b=pd.qcut(p,10,duplicates='drop')
    cal=pd.DataFrame({'bin':b,'y':y,'p':p}).groupby('bin',observed=True).agg(n=('y','size'),observed=('y','mean'),predicted=('p','mean')).reset_index()
    cal.to_csv(ROOT/'tables/final_test_calibration.csv',index=False)
    fig,ax=plt.subplots(1,2,figsize=(10,3.4),constrained_layout=True)
    ax[0].plot(fpr,tpr,color='#246A73',label='Logistic: AUC 0.6644')
    ax[0].plot([0,1],[0,1],'--',color='#999999',label='Constant baseline')
    ax[0].set(xlabel='False positive rate',ylabel='True positive rate',title='Later-period test discrimination',xlim=(0,1),ylim=(0,1))
    ax[0].legend(fontsize=8)
    ax[1].plot(cal.predicted,cal.observed,'o-',color='#246A73',label='Quantile bins')
    ax[1].plot([0,1],[0,1],'--',color='#999999',label='Perfect agreement')
    ax[1].set(xlabel='Mean predicted probability',ylabel='Observed noncompletion fraction',title='Test reliability (no recalibration)',xlim=(0,.8),ylim=(0,.8))
    ax[1].legend(fontsize=8)
    fig.savefig(ROOT/'figures/07_final_test_diagnostics.png',dpi=200)
    plt.close(fig)

if __name__=='__main__': run()
