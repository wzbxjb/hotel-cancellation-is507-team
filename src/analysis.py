"""Five reproducible analysis stages, shared by CLI and notebooks."""
import hashlib
import json
import platform
import warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
from sklearn.dummy import DummyClassifier
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve
from sklearn.exceptions import ConvergenceWarning
from .utils import *

plt.rcParams.update({'figure.dpi':130,'savefig.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
RAW = ROOT/'data/raw/hotels.csv'
SOURCE = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv'

def savefig(name):
    plt.tight_layout()
    plt.savefig(ROOT/'figures'/name,bbox_inches='tight')
    plt.close()

def audit():
    verify_source(RAW)
    # Preserve original token semantics before converting selected missing values.
    raw = pd.read_csv(RAW,keep_default_na=False, low_memory=False, dtype={'children':str,'agent':str,'company':str,'country':str})
    expected = {'City Hotel':79330,'Resort Hotel':40060}
    assert raw.shape == (119390,32), raw.shape
    assert raw.hotel.value_counts().to_dict() == expected
    assert set(raw.is_canceled.unique()) == {0,1}  # schema only; no holdout target summary
    miss=[]
    for c in raw:
        counts=raw[c].astype(str).value_counts()
        miss.append(dict(column=c,dtype=str(raw[c].dtype),literal_NULL=int(counts.get('NULL',0)),literal_NA=int(counts.get('NA',0)),empty=int(counts.get('',0)),n_unique=raw[c].nunique()))
    table(pd.DataFrame(miss),'raw_missing_tokens.csv')
    d=raw.copy()
    for c in ['agent','company']:
        d[c]=d[c].replace({'NULL':'Not_applicable','NA':'Unknown','':'Unknown'}).astype(str)
    for c in ['children']:
        d[c]=pd.to_numeric(d[c].replace({'NULL':np.nan,'NA':np.nan,'':np.nan}),errors='raise')
    d['country']=d.country.replace({'NULL':'Unknown','NA':'Unknown','':'Unknown'})
    d=derive_dates(d)
    d.insert(0,'row_id',np.arange(len(d)))
    d['partition']=assign_partition(d)
    # Audit alternative maturity gates on development candidates only; no model selection.
    maturity=[]; date_checks=[]
    for name,start,end in [('train',TRAIN_START,VAL_START),('validation',VAL_START,HOLDOUT_START)]:
        g=d.loc[d.booking_date.ge(start)&d.booking_date.lt(end)].copy()
        consistent=g.status_date.ge(g.booking_date)
        status=g.status_date.lt(end); departure=g.planned_departure.lt(end)
        for label,mask in [('primary_both',consistent&status&departure),
                           ('status_only',consistent&status),
                           ('additional_status_only',consistent&status&~departure),
                           ('departure_only_not_status',consistent&departure&~status),
                           ('neither_before_cutoff',consistent&~departure&~status),
                           ('date_inconsistent',~consistent)]:
            z=g.loc[mask]
            maturity.append(dict(partition=name,rule=label,n=len(z),
                non_completion_rate=z.is_canceled.mean(),median_lead_time=z.lead_time.median(),
                canceled=int(z.reservation_status.eq('Canceled').sum()),
                no_show=int(z.reservation_status.eq('No-Show').sum()),
                check_out=int(z.reservation_status.eq('Check-Out').sum())))
        for status_name,z in g.groupby('reservation_status'):
            date_checks.append(dict(partition=name,status=status_name,n=len(z),
                status_before_booking=int(z.status_date.lt(z.booking_date).sum()),
                status_before_arrival=int(z.status_date.lt(z.arrival_date).sum()),
                status_equals_departure=int(z.status_date.eq(z.planned_departure).sum()),
                status_after_departure=int(z.status_date.gt(z.planned_departure).sum())))
    table(pd.DataFrame(maturity),'maturity_rule_audit.csv')
    table(pd.DataFrame(date_checks),'development_date_audit.csv')
    # Duplicate hashes are only computed within development partitions; no test-label access.
    split=[]
    for name,g in d.groupby('partition',sort=True):
        split.append(dict(partition=name,n=len(g),booking_min=str(g.booking_date.min().date()),booking_max=str(g.booking_date.max().date())))
    table(pd.DataFrame(split),'split_counts.csv')
    for name in ['train','validation']:
        g=d[d.partition.eq(name)].copy()
        g['exact_duplicate_group']=pd.util.hash_pandas_object(raw.loc[g.index],index=False).astype(str)
        g.to_csv(ROOT/f'data/processed/{name}.csv',index=False)
    # Final holdout is physically separate. Loaded only to store bytes; no predictions/statistics of y.
    hold=d[d.partition.eq('final_holdout')].copy()
    hold.to_csv(ROOT/'data/processed/FINAL_HOLDOUT_LOCKED.csv',index=False)
    d[['row_id','booking_date','arrival_date','partition']].to_csv(ROOT/'data/processed/row_manifest.csv',index=False)
    train=read_partition('train'); val=read_partition('validation')
    dev=pd.concat([train,val],ignore_index=True)
    anomalies={
        'eligible_development_rows':len(dev),
        'zero_total_guests':int((dev[['adults','children','babies']].sum(axis=1,min_count=3)==0).sum()),
        'zero_nights':int((dev.stays_in_week_nights+dev.stays_in_weekend_nights==0).sum()),
        'negative_adr':int((dev.adr<0).sum()),
        'adr_above_1000':int((dev.adr>1000).sum()),
        'adults_above_10':int((dev.adults>10).sum()),
        'status_before_booking':int((dev.status_date<dev.booking_date).sum()),
        'negative_lead_time':int((dev.lead_time<0).sum()),
        'train_exact_redundant_rows':int(train.exact_duplicate_group.duplicated().sum()),
        'validation_exact_redundant_rows':int(val.exact_duplicate_group.duplicated().sum()),
        'exact_hash_overlap_train_validation':len(set(train.exact_duplicate_group)&set(val.exact_duplicate_group)),
        'repeated_guest_rows':int(dev.is_repeated_guest.sum()),
    }
    table(pd.DataFrame(list(anomalies.items()),columns=['check','count']),'development_audit.csv')
    assert dev.is_canceled.eq(dev.reservation_status.isin(['Canceled','No-Show']).astype(int)).all()
    table(dev.groupby(['partition','reservation_status','is_canceled']).size().reset_index(name='n'),'target_semantics_development.csv')
    table(pd.DataFrame([dict(partition=k,column=c,missing_n=int(g[c].isna().sum())) for k,g in [('train',train),('validation',val)] for c in FEATURES]),'model_missingness.csv')
    leakage=[]
    included=set(NUMERIC+CATEGORICAL)
    reasons={
        'is_canceled':'Target, includes no-show in the published encoding; never a predictor.',
        'reservation_status':'Direct outcome proxy.', 'reservation_status_date':'Terminal outcome date; only administrative label availability check.',
        'assigned_room_type':'Operational room assignment can occur after booking.',
        'booking_changes':'Accumulates amendments after booking.',
        'days_in_waiting_list':'Elapsed waiting until confirmation not necessarily known at entry.',
        'adr':'Computed using lodging transactions; not verified as initial quoted price.',
        'deposit_type':'Table 1: calculated from payments before arrival/cancellation; not initial booking policy.',
        'required_car_parking_spaces':'Request may be added later.',
        'total_of_special_requests':'Requests may accumulate later.',
        'previous_cancellations':'Prior bookings may have outcomes observed only after current creation.',
        'previous_bookings_not_canceled':'As-of-creation history cannot be reconstructed.',
        'is_repeated_guest':'Table 1 checks profile creation before booking creation. Conservative exclusion: exact as-of values cannot be independently reconstructed; not proven future information.',
        'country':'Paper warns correct nationality may only be known at check-in; temporal provenance risk first, nationality proxy concern second.',
        'agent':'Categorical anonymized identifier; omitted for parsimony, not ordinal.',
        'company':'Categorical identifier; NULL means not applicable, not missing.',
        'customer_type':'Table 1 defines group/contract linkage. Initial snapshot is unavailable; possible amendment is a project concern, not proven leakage.',
        'arrival_date_year':'Used to reconstruct calendar split; omit secular year from primary predictors.',
        'arrival_date_month':'Replaced with fixed sine/cosine encoding; planned arrival may have changed.',
        'arrival_date_week_number':'Redundant date component; omitted.',
        'arrival_date_day_of_month':'Used for split reconstruction; omitted from predictors.'}
    for c in raw:
        reason=reasons.get(c,'Plausibly available at booking in an operational system, but this dataset stores later snapshots; inclusion is conditional, not certified safe.')
        if c=='hotel': reason='Source hotel identity is stable; only two specific hotels, not replicated hotel types.'
        if c=='lead_time': reason='Definition supports booking_date = arrival_date - lead_time, but original entry timestamp and consistency after date amendments cannot be verified.'
        if c in included:
            category='stable identity' if c=='hotel' else 'conditional snapshot predictor'
        elif c in {'is_canceled','reservation_status','reservation_status_date'}:
            category='outcome or outcome metadata'
        elif c in {'booking_changes','assigned_room_type','days_in_waiting_list','deposit_type','adr'}:
            category='post-entry operational or cumulative measurement'
        elif c in {'agent','company','arrival_date_year','arrival_date_month','arrival_date_week_number','arrival_date_day_of_month'}:
            category='parsimony or redundant representation; not proven leakage'
        else:
            category='temporal provenance uncertainty; conservative exclusion'
        leakage.append(dict(column=c,risk_category=category,primary_use='conditional predictor' if c in included else ('target' if c=='is_canceled' else 'excluded predictor'),reason=reason,source='Antonio et al. (2019), Table 1 and Section 2; project exclusion judgment',enforced_exclusion=c not in included))
    for c in ['arrival_month_sin','arrival_month_cos']:
        category='conditional snapshot predictor'
        leakage.append(dict(column=c,risk_category=category,primary_use='conditional predictor',reason='Deterministic transform of snapshot arrival month; no learned information from validation.',source='Project derivation from arrival month',enforced_exclusion=False))
    table(pd.DataFrame(leakage),'prediction_time_leakage_audit.csv')
    provenance=dict(source_url=SOURCE,sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),bytes=RAW.stat().st_size,rows=len(raw),columns=len(raw.columns),hotel_counts=expected,raw_file_mtime_utc=datetime.fromtimestamp(RAW.stat().st_mtime,timezone.utc).isoformat(),python=platform.python_version(),paper='https://doi.org/10.1016/j.dib.2018.11.126',mirror_validation='Schema, hotel counts and published arrival window verified; no byte-for-byte comparison to publisher ZIP.',holdout_policy='Schema/date partitioning/storage only; no target summary, predictions, fitting or model selection.')
    assert d.arrival_date.min()==pd.Timestamp('2015-07-01')
    assert d.arrival_date.max()==pd.Timestamp('2017-08-31')
    (ROOT/'data/raw/PROVENANCE.json').write_text(json.dumps(provenance,indent=2))
    (ROOT/'data/processed/HOLDOUT_POLICY.md').write_text('# Final holdout locked\n\nBooking-date proxy >= 2017-01-01. Never loaded by modeling notebooks. Raw source necessarily contains the labels; this is a procedural lock, not encryption. Raw schema/token checks and date partition metadata are permitted. No holdout outcome summaries or predictions are produced.\n\nBefore final use: freeze features, C, threshold, eligibility and primary metrics without opening holdout; resolve temporal snapshot limitations; define cohort/label-maturity rules using source coverage rather than outcomes. Then evaluate once and report all results, including failures. The arrival-window end implies incomplete coverage of long-lead bookings; no general booking-cohort claim is valid.\n')
    return pd.DataFrame(split)

def eda():
    d=read_partition('train')
    table(d[NUMERIC+['adr']].describe(percentiles=[.01,.25,.5,.75,.99]).T.reset_index(names='variable'),'train_distributions.csv')
    for col in ['hotel','market_segment','distribution_channel','meal','reserved_room_type']:
        table(d.groupby(col).is_canceled.agg(n='size',canceled='sum',rate='mean').reset_index(),f'eda_{col}.csv')
    month=d.groupby(d.booking_date.dt.to_period('M').astype(str)).is_canceled.agg(n='size',rate='mean').reset_index()
    table(month,'eda_booking_month.csv')
    fig,ax=plt.subplots(1,2,figsize=(11,4))
    ax[0].bar(month.booking_date,month.n,color='#31788e'); ax[0].tick_params(axis='x',rotation=65); ax[0].set(title='Eligible training bookings by booking month',ylabel='Bookings')
    ax[1].plot(month.booking_date,month.rate,marker='o',color='#a64633'); ax[1].tick_params(axis='x',rotation=65); ax[1].set(title='Training outcome rate (cancellation / no-show)',ylabel='Observed fraction',ylim=(0,1))
    savefig('01_training_time.png')
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for y,label in [(0,'Not canceled'),(1,'Canceled / no-show')]:
        ax[0].hist(d.loc[d.is_canceled.eq(y),'lead_time'],bins=np.arange(0,741,20),alpha=.5,density=True,label=label)
    ax[0].set(xlabel='Lead time (days)',ylabel='Density',title='Training lead-time distribution'); ax[0].legend(fontsize=8)
    hotel=d.groupby('hotel').is_canceled.mean()
    ax[1].bar(hotel.index,hotel.values,color=['#31788e','#d89049']); ax[1].set(ylabel='Observed outcome fraction',ylim=(0,1),title='Two individual hotels (training only)')
    savefig('02_training_distributions.png')
    return month

def preprocessing():
    tr,va=read_partition('train'),read_partition('validation')
    assert set(tr.row_id).isdisjoint(va.row_id)
    assert tr.booking_date.max()<VAL_START<=va.booking_date.min()
    assert va.booking_date.max()<HOLDOUT_START
    assert (tr.status_date<VAL_START).all() and (tr.planned_departure<VAL_START).all()
    assert (va.status_date<HOLDOUT_START).all() and (va.planned_departure<HOLDOUT_START).all()
    assert not FORBIDDEN.intersection(FEATURES)
    prep=build_pipeline().named_steps['preprocess']
    Xt=prep.fit_transform(tr[FEATURES]); Xv=prep.transform(va[FEATURES])
    unseen=[]
    for c in CATEGORICAL:
        unseen.append(dict(column=c,n_unseen=int((~va[c].isin(tr[c])).sum()),unseen_levels=';'.join(sorted(set(va[c])-set(tr[c])))))
    table(pd.DataFrame(unseen),'unseen_validation_categories.csv')
    table(pd.DataFrame({'column':NUMERIC,'training_median':prep.named_transformers_['numeric'].named_steps['impute'].statistics_}),'training_imputation.csv')
    result=dict(train_rows=Xt.shape[0],validation_rows=Xv.shape[0],encoded_columns=Xt.shape[1],features=FEATURES,all_partition_assertions_passed=True,fit_scope='eligible train only')
    (ROOT/'tables/preprocessing_checks.json').write_text(json.dumps(result,indent=2))
    return result

def modeling():
    tr,va=read_partition('train'),read_partition('validation')
    y,yv=tr.is_canceled,va.is_canceled
    dummy=DummyClassifier(strategy='prior').fit(tr[FEATURES],y)
    pdummy=dummy.predict_proba(va[FEATURES])[:,1]
    with warnings.catch_warnings():
        warnings.simplefilter('error',ConvergenceWarning)
        lr=build_pipeline().fit(tr[FEATURES],y)
    p=lr.predict_proba(va[FEATURES])[:,1]
    rows=[dict(model='Dummy prior',**score(yv,pdummy)),dict(model='Logistic primary',**score(yv,p))]
    dedup=tr.drop_duplicates('exact_duplicate_group')
    with warnings.catch_warnings():
        warnings.simplefilter('error',ConvergenceWarning)
        lr_unique=build_pipeline().fit(dedup[FEATURES],dedup.is_canceled)
    pu=lr_unique.predict_proba(va[FEATURES])[:,1]
    rows.append(dict(model='Logistic train deduplicated',**score(yv,pu)))
    # Minimal proxy sensitivity removes mutable room, meal, demographic, channel fields.
    # Even lead_time and calendar retain timestamp assumptions; not a leakage-free claim.
    small_num=['lead_time','arrival_month_sin','arrival_month_cos']; small_cat=['hotel']
    small=build_pipeline(small_num,small_cat).fit(tr[small_num+small_cat],y)
    ps=small.predict_proba(va[small_num+small_cat])[:,1]
    rows.append(dict(model='Logistic minimal proxy',**score(yv,ps)))
    unique_mask=~va.exact_duplicate_group.duplicated()
    rows.append(dict(model='Primary on unique validation rows',**score(yv[unique_mask],p[unique_mask])))
    metrics=table(pd.DataFrame(rows),'validation_metrics.csv')
    preds=va[['row_id','booking_date','hotel','market_segment','lead_time','adults','children','babies','stays_in_week_nights','stays_in_weekend_nights','is_repeated_guest','is_canceled','exact_duplicate_group']].copy()
    preds['p_primary']=p;preds['p_dummy']=pdummy;preds['p_dedup_train']=pu;preds['p_minimal']=ps
    preds['predicted']=(p>=.5).astype(int)
    preds['error_type']=np.select([(yv==0)&(p>=.5),(yv==1)&(p<.5),(yv==1)&(p>=.5)],['FP','FN','TP'],default='TN')
    preds.to_csv(ROOT/'data/processed/validation_predictions.csv',index=False)
    joblib.dump(lr,ROOT/'data/processed/logistic_primary.joblib')
    names=lr.named_steps['preprocess'].get_feature_names_out()
    coef=pd.DataFrame({'feature':names,'coefficient':lr.named_steps['model'].coef_[0]})
    table(coef.sort_values('coefficient'),'logistic_coefficients.csv')
    table(pd.DataFrame([dict(model='Logistic primary',iterations=int(lr.named_steps['model'].n_iter_[0]),training_rows=len(tr),encoded_features=len(names),C=1,threshold=.5,intercept=float(lr.named_steps['model'].intercept_[0]))]),'model_specification.csv')
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for name,pp in [('Primary logistic',p),('Dummy prior',pdummy),('Minimal proxy',ps)]:
        fpr,tpr,_=roc_curve(yv,pp); ax[0].plot(fpr,tpr,label=f'{name} (AUC={roc_auc_score(yv,pp):.3f})')
        if name == 'Dummy prior':
            ax[1].axhline(yv.mean(),ls='--',color='gray',label='No-skill prevalence / Dummy AP')
        else:
            prec,rec,_=precision_recall_curve(yv,pp); ax[1].step(rec,prec,where='post',label=name)
    ax[0].plot([0,1],[0,1],ls='--',color='gray');ax[0].set(xlabel='False positive rate',ylabel='True positive rate',title='Validation ROC');ax[0].legend(fontsize=8)
    ax[1].set(xlabel='Recall',ylabel='Precision',title='Validation precision–recall');ax[1].legend(fontsize=8)
    savefig('03_validation_roc_pr.png')
    m=rows[1];cm=np.array([[m['tn'],m['fp']],[m['fn'],m['tp']]])
    fig,ax=plt.subplots(figsize=(5,4));ax.imshow(cm,cmap='Blues')
    for i in range(2):
        for j in range(2):ax.text(j,i,f'{cm[i,j]:,}',ha='center',va='center',color='white' if cm[i,j]>cm.max()/2 else 'black',fontsize=16)
    ax.set(xticks=[0,1],yticks=[0,1],xticklabels=['Completed','Canceled / no-show'],yticklabels=['Completed','Canceled / no-show'],xlabel='Predicted',ylabel='Observed',title='Validation confusion matrix (threshold 0.50)')
    savefig('04_confusion_matrix.png')
    fig,ax=plt.subplots(figsize=(6,4))
    frac,mean=calibration_curve(yv,p,n_bins=10,strategy='quantile')
    ax.plot(mean,frac,'o-',label='Primary logistic');ax.plot([0,1],[0,1],'--',color='gray');ax.set(xlabel='Mean predicted probability',ylabel='Observed outcome fraction',title='Validation calibration (no recalibration)');ax.legend()
    savefig('05_calibration.png')
    bins=pd.qcut(p,10,duplicates='drop')
    calibration=pd.DataFrame({'bin':bins,'y':np.asarray(yv),'p':p}).groupby('bin',observed=True).agg(n=('y','size'),observed=('y','mean'),predicted=('p','mean')).reset_index()
    table(calibration,'calibration_bins.csv')
    return metrics

def errors():
    d=pd.read_csv(ROOT/'data/processed/validation_predictions.csv',parse_dates=['booking_date'])
    d['lead_band']=pd.cut(d.lead_time,[-1,7,30,90,180,np.inf],labels=['0–7','8–30','31–90','91–180','181+']).astype(str)
    d['booking_month']=d.booking_date.dt.to_period('M').astype(str)
    d['family']=np.where((d.children.fillna(0)+d.babies)>0,'With children/babies','No recorded children/babies')
    groups=[]
    for c in ['hotel','market_segment','lead_band','booking_month','is_repeated_guest','family']:
        for name,g in d.groupby(c,dropna=False):
            m=score(g.is_canceled,g.p_primary)
            groups.append(dict(grouping=c,group=name,small_group=len(g)<100,**m))
    sg=table(pd.DataFrame(groups),'subgroup_metrics.csv')
    summary=d.groupby('error_type').agg(n=('row_id','size'),mean_score=('p_primary','mean'),median_lead=('lead_time','median'),mean_adults=('adults','mean')).reset_index()
    table(summary,'error_summary.csv')
    examples=pd.concat([d[d.error_type.eq('FP')].nlargest(10,'p_primary'),d[d.error_type.eq('FN')].nsmallest(10,'p_primary')])
    table(examples,'confident_errors.csv')
    thresholds=[dict(threshold_value=t,**score(d.is_canceled,d.p_primary,threshold=t)) for t in [.2,.3,.4,.5,.6,.7,.8]]
    table(pd.DataFrame(thresholds),'threshold_diagnostics.csv')
    ranks=[]
    for fraction in [.05,.1,.2]:
        k=int(np.ceil(len(d)*fraction)); top=d.sort_values(['p_primary','row_id'],ascending=[False,True]).head(k)
        ranks.append(dict(capacity_fraction=fraction,k=k,precision_at_k=top.is_canceled.mean(),recall_at_k=top.is_canceled.sum()/d.is_canceled.sum(),tie_rule='ascending original row_id'))
    table(pd.DataFrame(ranks),'ranking_capacity.csv')
    # Paired cluster bootstrap preserves same-week bookings, but cannot recover guest/group clusters.
    clusters=d.booking_date.dt.to_period('W').astype(str)
    ix=[np.flatnonzero((clusters==c).to_numpy()) for c in sorted(clusters.unique())]
    rng=np.random.default_rng(SEED); rows=[]
    y=d.is_canceled.to_numpy();p=d.p_primary.to_numpy();p0=d.p_dummy.to_numpy()
    for b in range(400):
        inds=np.concatenate([ix[j] for j in rng.integers(0,len(ix),size=len(ix))])
        if len(np.unique(y[inds]))<2:continue
        rows.append(dict(rep=b,roc_auc=roc_auc_score(y[inds],p[inds]),auc_gain=roc_auc_score(y[inds],p[inds])-roc_auc_score(y[inds],p0[inds]),brier_gain=brier_score_loss(y[inds],p0[inds])-brier_score_loss(y[inds],p[inds])))
    boot=pd.DataFrame(rows)
    ci=[]
    for c in ['roc_auc','auc_gain','brier_gain']:
        ci.append(dict(metric=c,lower_2_5=boot[c].quantile(.025),upper_97_5=boot[c].quantile(.975),replicates=len(boot),week_clusters=len(ix),interpretation='Approximate conditional stability interval; fixed fitted model, exchangeable weeks assumed.'))
    table(pd.DataFrame(ci),'week_cluster_bootstrap.csv')
    table(boot,'bootstrap_replicates.csv')
    # Eligibility anomaly sensitivity uses rules independent of y, retains original fitted model.
    regular=(d[['adults','children','babies']].sum(axis=1,min_count=3)>0)&((d.stays_in_week_nights+d.stays_in_weekend_nights)>0)&(d.adults<=10)
    table(pd.DataFrame([dict(scope='Exclude zero guests, zero nights and >10 adults from validation only',**score(y[regular],p[regular]))]),'anomaly_sensitivity.csv')
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    h=sg[sg.grouping.eq('hotel')]
    ax[0].bar(h.group,100*h.recall,color='#31788e');ax[0].set(ylim=(0,1),ylabel='Recall (%) — zoomed 0–1%',title='Validation recall at threshold 0.50')
    for i,recall in enumerate(h.recall): ax[0].text(i,100*recall+.025,f'{100*recall:.2f}%',ha='center')
    m=sg[sg.grouping.eq('booking_month')]
    ax[1].plot(m.group,m.roc_auc,'o-',label='ROC-AUC');ax[1].plot(m.group,m.prevalence,'s--',label='Outcome rate');ax[1].tick_params(axis='x',rotation=45);ax[1].set(ylim=(0,1),title='Validation temporal stability');ax[1].legend()
    savefig('06_subgroup_temporal.png')
    return sg

if __name__=='__main__':
    for stage in [audit,eda,preprocessing,modeling,errors]:
        print(f'Running {stage.__name__}',flush=True)
        result=stage()
        print(result if isinstance(result,dict) else result.to_string(index=False),flush=True)
