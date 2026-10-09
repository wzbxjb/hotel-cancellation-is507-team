"""Shared, deterministic analysis utilities. No function evaluates final holdout."""
from pathlib import Path
import calendar
import hashlib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (roc_auc_score, average_precision_score, accuracy_score,
    balanced_accuracy_score, precision_score, recall_score, f1_score,
    brier_score_loss, log_loss, confusion_matrix)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = '7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06'

def verify_source(path):
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != SOURCE_SHA256:
        raise ValueError(f'Source checksum mismatch: {actual}; stop before writing outputs.')
    return actual

SEED = 507
TRAIN_START = pd.Timestamp('2015-07-01')
VAL_START = pd.Timestamp('2016-07-01')
HOLDOUT_START = pd.Timestamp('2017-01-01')
NUMERIC = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights',
           'adults', 'children', 'babies', 'arrival_month_sin', 'arrival_month_cos']
CATEGORICAL = ['hotel', 'meal', 'market_segment', 'distribution_channel', 'reserved_room_type']
FEATURES = NUMERIC + CATEGORICAL
FORBIDDEN = {'is_canceled','reservation_status','reservation_status_date','status_date',
             'assigned_room_type','booking_changes','days_in_waiting_list','adr',
             'deposit_type','required_car_parking_spaces','total_of_special_requests',
             'previous_cancellations','previous_bookings_not_canceled','is_repeated_guest',
             'customer_type','country','agent','company','booking_date','arrival_date',
             'planned_departure','row_id','partition','exact_duplicate_group',
             'arrival_date_year','arrival_date_month','arrival_date_week_number','arrival_date_day_of_month'}

def derive_dates(raw):
    d = raw.copy()
    months = {m:i for i,m in enumerate(calendar.month_name) if m}
    month = d.arrival_date_month.map(months)
    d['arrival_date'] = pd.to_datetime(dict(year=d.arrival_date_year, month=month,
                                          day=d.arrival_date_day_of_month), errors='raise')
    d['booking_date'] = d.arrival_date - pd.to_timedelta(d.lead_time, unit='D')
    d['planned_departure'] = d.arrival_date + pd.to_timedelta(d.stays_in_week_nights + d.stays_in_weekend_nights, unit='D')
    d['status_date'] = pd.to_datetime(d.reservation_status_date, errors='raise')
    d['arrival_month_sin'] = np.sin(2*np.pi*month/12)
    d['arrival_month_cos'] = np.cos(2*np.pi*month/12)
    return d

def assign_partition(d):
    """Calendar assignment plus conservative outcome-maturation embargo.

    Does not consult holdout labels or status dates. Dates are only proxies.
    Recorded terminal-status date and snapshot-derived departure must BOTH precede fitting/evaluation
    origin. Eligibility does not branch on cancellation label, but can select on outcome timing.
    This extra departure restriction is a cohort choice, not necessary label latency
    for an already canceled booking. Same-day dates are conservatively excluded.
    """
    p = pd.Series('left_boundary', index=d.index, dtype='str')
    p.loc[d.booking_date >= HOLDOUT_START] = 'final_holdout'
    for name, start, end in [('train',TRAIN_START,VAL_START),('validation',VAL_START,HOLDOUT_START)]:
        mask = d.booking_date.ge(start) & d.booking_date.lt(end)
        p.loc[mask] = name
        mature = d.loc[mask,'planned_departure'].lt(end) & d.loc[mask,'status_date'].lt(end)
        p.loc[mature.index[~mature]] = name + '_unmatured'
        inconsistent = d.loc[mask,'status_date'].lt(d.loc[mask,'booking_date'])
        p.loc[inconsistent.index[inconsistent]] = name + '_date_inconsistent'
    return p

def build_pipeline(numeric=None, categorical=None):
    numeric = NUMERIC if numeric is None else numeric
    categorical = CATEGORICAL if categorical is None else categorical
    if FORBIDDEN.intersection(numeric + categorical) or not set(numeric + categorical) <= set(FEATURES):
        raise ValueError('Predictor not approved by the retrospective feature policy')
    preprocess = ColumnTransformer([
        ('numeric', Pipeline([('impute',SimpleImputer(strategy='median',add_indicator=True)),
                              ('scale',StandardScaler())]), numeric),
        ('categorical', Pipeline([('impute',SimpleImputer(strategy='constant',fill_value='Unknown')),
                                  ('encode',OneHotEncoder(handle_unknown='ignore'))]), categorical)
    ])
    return Pipeline([('preprocess',preprocess), ('model',LogisticRegression(C=1.,solver='lbfgs',max_iter=3000,random_state=SEED))])

def score(y, p, threshold=.5, partition='validation'):
    if partition not in {'train','validation','sensitivity_validation'}:
        raise ValueError('Final holdout evaluation is locked for Midterm')
    y, p = np.asarray(y), np.asarray(p)
    h = (p >= threshold).astype(int)
    tn,fp,fn,tp = confusion_matrix(y,h,labels=[0,1]).ravel()
    both = len(np.unique(y)) == 2
    return dict(n=len(y), prevalence=float(np.mean(y)), threshold=threshold,
        roc_auc=roc_auc_score(y,p) if both else np.nan,
        average_precision=average_precision_score(y,p) if np.any(y) else np.nan,
        accuracy=accuracy_score(y,h), balanced_accuracy=balanced_accuracy_score(y,h) if both else np.nan,
        precision=precision_score(y,h,zero_division=0), recall=recall_score(y,h,zero_division=0),
        f1=f1_score(y,h,zero_division=0), specificity=tn/(tn+fp) if tn+fp else np.nan,
        brier=brier_score_loss(y,p), log_loss=log_loss(y,p,labels=[0,1]),
        tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp))

def table(df, filename):
    df.to_csv(ROOT/'tables'/filename,index=False)
    return df

def read_partition(name):
    if name not in {'train','validation'}:
        raise ValueError('Use of locked holdout is forbidden in Midterm notebooks')
    return pd.read_csv(ROOT/'data'/'processed'/f'{name}.csv', parse_dates=['arrival_date','booking_date','planned_departure','status_date'])
