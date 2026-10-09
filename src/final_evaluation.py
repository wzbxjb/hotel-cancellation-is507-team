"""Execute the frozen retrospective final test; never tune on its outcomes."""
from pathlib import Path
import hashlib
import json
import platform
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (log_loss, roc_auc_score, average_precision_score,
    brier_score_loss, accuracy_score, precision_score, recall_score, confusion_matrix)
from .utils import ROOT, FEATURES, verify_source, derive_dates, read_partition


def metrics(y, p):
    y, p = np.asarray(y), np.asarray(p)
    h = (p >= .5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, h, labels=[0, 1]).ravel()
    return dict(n=len(y), prevalence=float(y.mean()), log_loss=float(log_loss(y,p,labels=[0,1])),
        roc_auc=float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None,
        average_precision=float(average_precision_score(y,p)), brier=float(brier_score_loss(y,p)),
        accuracy=float(accuracy_score(y,h)), precision=float(precision_score(y,h,zero_division=0)),
        recall=float(recall_score(y,h,zero_division=0)),
        tn=int(tn), fp=int(fp), fn=int(fn), tp=int(tp))


def run():
    protocol = ROOT/'docs/FINAL_EVALUATION_PROTOCOL.md'
    assert protocol.exists(), 'Freeze the protocol before opening test outcomes.'
    protocol_sha = hashlib.sha256(protocol.read_bytes()).hexdigest()
    record = ROOT/'tables/final_test_results.json'
    if record.exists():
        old = json.loads(record.read_text())
        assert old['protocol_sha256']==protocol_sha, 'Protocol changed after test inspection.'
    verify_source(ROOT/'data/raw/hotels.csv')
    raw = pd.read_csv(ROOT/'data/raw/hotels.csv',keep_default_na=False,low_memory=False)
    d = raw.copy()
    d['children'] = pd.to_numeric(d.children.replace({'NA':np.nan,'NULL':np.nan,'':np.nan}))
    d = derive_dates(d)
    d.insert(0,'row_id',np.arange(len(d)))
    held = d[d.booking_date.ge('2017-01-01')]
    window = held[held.booking_date.lt('2017-06-01')]
    mature = (window.planned_departure.lt('2017-09-01') &
              window.status_date.lt('2017-09-01') & window.status_date.ge(window.booking_date))
    test = window.loc[mature].copy()
    tr, va = read_partition('train'), read_partition('validation')
    assert set(test.row_id).isdisjoint(set(tr.row_id)|set(va.row_id))
    assert test.booking_date.min() > va.booking_date.max()
    assert test.is_canceled.eq(test.reservation_status.isin(['Canceled','No-Show']).astype(int)).all()
    model_path = ROOT/'data/processed/logistic_primary.joblib'
    model = joblib.load(model_path)
    p = model.predict_proba(test[FEATURES])[:,1]
    prior = float(tr.is_canceled.mean())
    baseline = np.full(len(test),prior)
    rows = [dict(model='Dummy prior',**metrics(test.is_canceled,baseline)),
            dict(model='Logistic primary',**metrics(test.is_canceled,p))]
    pd.DataFrame(rows).to_csv(ROOT/'tables/final_test_metrics.csv',index=False)
    pred = test[['row_id','booking_date','hotel','lead_time','is_canceled']].copy()
    pred['p_primary']=p; pred['p_dummy']=baseline
    pred.to_csv(ROOT/'data/processed/final_test_predictions.csv',index=False)
    k = int(np.ceil(.1*len(test)))
    top = pred.sort_values(['p_primary','row_id'],ascending=[False,True]).head(k)
    ranking = dict(capacity_fraction=.1,k=k,positive_count=int(top.is_canceled.sum()),
        precision_at_k=float(top.is_canceled.mean()),recall_at_k=float(top.is_canceled.sum()/test.is_canceled.sum()))
    subgroup = []
    for h,g in pred.groupby('hotel'):
        subgroup.append(dict(hotel=h,**metrics(g.is_canceled,g.p_primary)))
    pd.DataFrame(subgroup).to_csv(ROOT/'tables/final_test_subgroups.csv',index=False)
    semantics = test.groupby(['reservation_status','is_canceled']).size().reset_index(name='n')
    semantics.to_csv(ROOT/'tables/final_test_target_semantics.csv',index=False)
    test_hash = set(pd.util.hash_pandas_object(raw.loc[test.index],index=False).astype(str))
    overlap_train = len(test_hash & set(tr.exact_duplicate_group.astype(str)))
    overlap_validation = len(test_hash & set(va.exact_duplicate_group.astype(str)))
    result = dict(protocol_sha256=protocol_sha,model_sha256=hashlib.sha256(model_path.read_bytes()).hexdigest(),
        heldout_total=len(held),later_booking_proxy_unused=len(held)-len(window),window_candidates=len(window),
        maturity_excluded=int((~mature).sum()),eligible_test_rows=len(test),training_prior=prior,
        booking_min=str(test.booking_date.min().date()),booking_max=str(test.booking_date.max().date()),
        status_max=str(test.status_date.max().date()),departure_max=str(test.planned_departure.max().date()),
        full_row_hash_overlap_train=overlap_train,full_row_hash_overlap_validation=overlap_validation,
        duplicate_redundant_test=int(pd.util.hash_pandas_object(raw.loc[test.index],index=False).duplicated().sum()),
        metrics=rows,top10=ranking,subgroups=subgroup,
        relative_logloss_reduction=1-rows[1]['log_loss']/rows[0]['log_loss'],
        environment=dict(python=platform.python_version(),pandas=pd.__version__,sklearn=sklearn.__version__),
        interpretation='Later-period retrospective selected-cohort test; not certified creation-time prediction.')
    if record.exists():
        # Stable empirical outputs must match when rerun; paths/time are not included.
        assert result==old, 'Reproduction changed the frozen final-test result.'
    record.write_text(json.dumps(result,indent=2))
    (ROOT/'data/processed/HOLDOUT_POLICY.md').write_text('# Frozen final-test policy\n\nThe inherited development notebooks reject holdout reads/scoring. src.final_evaluation is the declared final-test entry point under docs/FINAL_EVALUATION_PROTOCOL.md. January-May 2017 eligibility requires status and planned departure before September 1. 3,696 later proxy-date rows remain unused; 328 window candidates are excluded. This is procedural control, not encryption.\n')
    print(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    run()
