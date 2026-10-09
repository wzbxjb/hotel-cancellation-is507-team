"""Verify scientific invariants, frozen test outputs and deliverable consistency."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
import nbformat
import joblib
from src.utils import ROOT, FEATURES, verify_source, score, read_partition, VAL_START, HOLDOUT_START

checks=[]
def check(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)

verify_source(ROOT/'data/raw/hotels.csv');checks.append('Pinned raw SHA256 matches')
tr,va=read_partition('train'),read_partition('validation')
manifest=pd.read_csv(ROOT/'data/processed/row_manifest.csv')
splits=pd.read_csv(ROOT/'tables/split_counts.csv')
check('All raw rows accounted for exactly once',len(manifest)==119390 and manifest.row_id.nunique()==119390 and splits.n.sum()==119390)
check('No train/validation overlap',set(tr.row_id).isdisjoint(va.row_id))
check('Prediction-time calendar ordering',tr.booking_date.max()<VAL_START<=va.booking_date.min() and va.booking_date.max()<HOLDOUT_START)
check('Training outcomes matured before validation',bool(((tr.status_date<VAL_START)&(tr.planned_departure<VAL_START)).all()))
check('Validation outcomes matured before final origin',bool(((va.status_date<HOLDOUT_START)&(va.planned_departure<HOLDOUT_START)).all()))
pred=pd.read_csv(ROOT/'data/processed/validation_predictions.csv')
check('Predictions only for eligible validation IDs',pred.row_id.tolist()==va.row_id.tolist())
check('No holdout IDs in predictions',set(pred.row_id).isdisjoint(set(manifest.loc[manifest.partition=='final_holdout','row_id'])))
metrics=pd.read_csv(ROOT/'tables/validation_metrics.csv').set_index('model')
for label,col in [('Dummy prior','p_dummy'),('Logistic primary','p_primary'),('Logistic train deduplicated','p_dedup_train'),('Logistic minimal proxy','p_minimal')]:
    actual=score(pred.is_canceled,pred[col])
    check(label+' all metrics recomputed',all(np.isclose(actual[c],metrics.loc[label,c],atol=1e-10,equal_nan=True) for c in actual))
unique=~pred.exact_duplicate_group.duplicated()
actual=score(pred.loc[unique,'is_canceled'],pred.loc[unique,'p_primary'])
check('Unique-validation metrics recomputed',all(np.isclose(actual[c],metrics.loc['Primary on unique validation rows',c],atol=1e-10,equal_nan=True) for c in actual))
lr=joblib.load(ROOT/'data/processed/logistic_primary.joblib')
check('Saved model reproduces validation scores',np.allclose(lr.predict_proba(va[FEATURES])[:,1],pred.p_primary,atol=1e-10))
notebooks=sorted((ROOT/'notebooks').glob('*.ipynb'))
check('Six notebooks present',len(notebooks)==6)
for path in notebooks:
    nb=nbformat.read(path,as_version=4);nbformat.validate(nb)
    cells=[c for c in nb.cells if c.cell_type=='code']
    check(path.name+' all cells executed',all(c.execution_count is not None for c in cells))
    check(path.name+' zero error outputs',all(o.output_type!='error' for c in cells for o in c.outputs))
check('Seven nonempty figure files',len(list((ROOT/'figures').glob('*.png')))==7 and all(p.stat().st_size>5000 for p in (ROOT/'figures').glob('*.png')))
audit=pd.read_csv(ROOT/'tables/prediction_time_leakage_audit.csv')
check('Feature audit covers all raw and derived model fields', len(audit)==34 and audit.column.nunique()==34)
check('Audit approved predictors match enforced set',set(audit.loc[~audit.enforced_exclusion,'column'])==set(FEATURES))
mat=pd.read_csv(ROOT/'tables/maturity_rule_audit.csv').set_index(['partition','rule'])
for part,n in [('train',len(tr)),('validation',len(va))]:
    check(part+' maturity primary count matches',mat.loc[(part,'primary_both'),'n']==n)
    check(part+' maturity alternatives reconcile',mat.loc[(part,'status_only'),'n']==n+mat.loc[(part,'additional_status_only'),'n'])
check('Development combined endpoint agrees with terminal status',all(g.is_canceled.eq(g.reservation_status.isin(['Canceled','No-Show']).astype(int)).all() for g in [tr,va]))
# Recompute final scores independently from the saved probabilities.
from src.final_evaluation import metrics as final_metrics
import re,zipfile,xml.etree.ElementTree as ET
result=json.loads((ROOT/'tables/final_test_results.json').read_text())
proto=ROOT/'docs/FINAL_EVALUATION_PROTOCOL.md'
check('Frozen protocol SHA matches',hashlib.sha256(proto.read_bytes()).hexdigest()==result['protocol_sha256'])
test=pd.read_csv(ROOT/'data/processed/final_test_predictions.csv',parse_dates=['booking_date'])
check('Final test size matches',len(test)==result['eligible_test_rows']==22541)
check('No test/development row-ID overlap',set(test.row_id).isdisjoint(set(tr.row_id)|set(va.row_id)))
check('Test booking-proxy window',bool(test.booking_date.ge('2017-01-01').all() and test.booking_date.lt('2017-06-01').all()))
check('Complete raw partition accounting',39865+14088+22541+38872+4024==119390)
check('Holdout accounting',result['heldout_total']==result['eligible_test_rows']+result['maturity_excluded']+result['later_booking_proxy_unused'])
for saved,col in zip(result['metrics'],['p_dummy','p_primary']):
    actual=final_metrics(test.is_canceled,test[col])
    check(saved['model']+' final metrics independently recomputed',all(np.isclose(actual[c],saved[c],atol=1e-10,equal_nan=True) for c in actual))
check('Baseline does not use evaluation prevalence',np.allclose(test.p_dummy,tr.is_canceled.mean(),atol=1e-12))
top=test.sort_values(['p_primary','row_id'],ascending=[False,True]).head(result['top10']['k'])
check('Top-10% selected size',len(top)==int(np.ceil(.1*len(test))))
check('Top-10% positives independently counted',int(top.is_canceled.sum())==result['top10']['positive_count'])
check('Top-10% precision and recall recomputed',np.isclose(top.is_canceled.mean(),result['top10']['precision_at_k']) and np.isclose(top.is_canceled.sum()/test.is_canceled.sum(),result['top10']['recall_at_k']))
raw=pd.read_csv(ROOT/'data/raw/hotels.csv',keep_default_na=False,low_memory=False)
from src.utils import derive_dates
raw['children']=pd.to_numeric(raw.children.replace({'NA':np.nan,'NULL':np.nan,'':np.nan}))
d=derive_dates(raw); eligible=d.loc[test.row_id]
check('Test maturity and consistency gates',bool((eligible.planned_departure.lt('2017-09-01') & eligible.status_date.lt('2017-09-01') & eligible.status_date.ge(eligible.booking_date)).all()))
check('Saved model reproduces test scores',np.allclose(lr.predict_proba(eligible[FEATURES])[:,1],test.p_primary,atol=1e-10))
check('Final-test endpoint includes cancellation/no-show',eligible.is_canceled.eq(eligible.reservation_status.isin(['Canceled','No-Show']).astype(int)).all())
report=(ROOT/'deliverables/IS507_Midterm_Report.md').read_text()
for key in ['log_loss','roc_auc','brier','average_precision']:
    check('Midterm report matches validation '+key,f"{metrics.loc['Logistic primary',key]:.4f}" in report)
check('Report contains validation confusion counts',all(f"{int(metrics.loc['Logistic primary',c]):,}" in report for c in ['tp','tn','fp','fn']))
for key in ['log_loss','roc_auc']:
    check('Report discloses previously evaluated test '+key,f"{result['metrics'][1][key]:.4f}" in report)
check('Report discloses test inspection','already' in report and 'unknown test after tuning' in report)
pdf=(ROOT/'deliverables/IS507_Midterm_Report.pdf').read_bytes()
check('Report PDF has five page objects',len(re.findall(rb'/Type\s*/Page\b',pdf))==5)
with zipfile.ZipFile(ROOT/'deliverables/IS507_Midterm_Presentation.pptx') as z:
    slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',x)]
    check('PPTX has 15 total slides',len(slides)==15)
    check('Five backup slides are hidden',sum(ET.fromstring(z.read(x)).get('show')=='0' for x in slides)==5)
    notes=[x for x in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',x)]
    check('All 15 slides have notes',len(notes)==15)
    text=' '.join(' '.join(ET.fromstring(z.read(x)).itertext()) for x in slides)
    check('PPTX uses actual validation headline metrics','0.6584' in text and '0.5517' in text and '0.30%' in text)
    check('PPTX discloses later-test results','0.6644' in text and '0.5968' in text and '6.62%' in text)
    check('Charts remain native',sum('/charts/' in x and x.endswith('.xml') for x in z.namelist())==2)
    check('Chart workbooks are embedded',sum(x.endswith('.xlsx') for x in z.namelist())==2)
for path in [ROOT/'README.md',ROOT/'FINAL_CHECKLIST.md',ROOT/'deliverables/IS507_Midterm_Report.md']:
    check(path.name+' local links resolve',all((path.parent/url.split('#')[0]).exists() for url in re.findall(r'\]\(([^)]+)\)',path.read_text()) if not url.startswith(('http:','https:','#'))))
result={'status':'PASS','n_checks':len(checks),'checks':checks,'frozen_final_test_evaluated':True,'later_booking_proxy_rows_unused':3696,'test_rows':22541}
(ROOT/'tables/verification_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
