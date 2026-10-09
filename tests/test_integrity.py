"""Tests focus on scientific failure modes, not cosmetic output."""
import unittest
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from src import utils

class IntegrityTests(unittest.TestCase):
    def test_source_verifier_rejects_changed_bytes(self):
        self.assertTrue(hasattr(utils, 'verify_source'), 'source verifier absent')
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'changed.csv'
            p.write_text('same name, different bytes')
            with self.assertRaises(ValueError):
                utils.verify_source(p)

    def test_booking_date_leap_day(self):
        d = pd.DataFrame({'arrival_date_year':[2016], 'arrival_date_month':['March'], 'arrival_date_day_of_month':[1], 'lead_time':[1], 'stays_in_week_nights':[2], 'stays_in_weekend_nights':[0], 'reservation_status_date':['2016-03-03']})
        self.assertTrue(hasattr(utils, 'derive_dates'), 'date function absent')
        self.assertEqual(str(utils.derive_dates(d).booking_date.iloc[0].date()), '2016-02-29')

    def test_temporal_boundaries_and_mature_labels(self):
        d = pd.DataFrame({'booking_date':pd.to_datetime(['2015-06-30','2015-07-01','2016-06-30','2016-07-01','2016-12-31','2017-01-01']), 'planned_departure':pd.to_datetime(['2015-08-01','2015-08-01','2016-07-02','2016-08-01','2017-01-02','2017-02-01']), 'status_date':pd.to_datetime(['2015-08-01','2015-08-01','2016-06-30','2016-08-01','2016-12-31','2017-02-01'])})
        self.assertTrue(hasattr(utils, 'assign_partition'), 'partition function absent')
        p = utils.assign_partition(d)
        self.assertEqual(p.tolist(), ['left_boundary','train','train_unmatured','validation','validation_unmatured','final_holdout'])

    def test_holdout_scoring_is_rejected(self):
        self.assertTrue(hasattr(utils, 'score'), 'guarded metrics absent')
        with self.assertRaises(ValueError):
            utils.score([0,1], [.1,.9], partition='final_holdout')

    def test_unknown_category_and_train_only_imputation(self):
        self.assertTrue(hasattr(utils, 'build_pipeline'), 'pipeline absent')
        train = pd.DataFrame({'lead_time':[0.,10.,np.nan,20.], 'hotel':['A','A','B','B']})
        model = utils.build_pipeline(['lead_time'], ['hotel'])
        model.fit(train, [0,0,1,1])
        pred = model.predict_proba(pd.DataFrame({'lead_time':[1000.,np.nan], 'hotel':['C','C']}))
        self.assertTrue(np.isfinite(pred).all())
        self.assertEqual(model.named_steps['preprocess'].named_transformers_['numeric'].named_steps['impute'].statistics_[0], 10.)

class FeaturePolicyTests(unittest.TestCase):
    def test_unapproved_predictors_rejected(self):
        for col in ['previous_cancellations', 'previous_bookings_not_canceled',
                    'is_repeated_guest', 'customer_type', 'country', 'agent',
                    'company', 'planned_departure', 'booking_date', 'row_id']:
            with self.subTest(column=col), self.assertRaises(ValueError):
                utils.build_pipeline([col], ['hotel'])

    def test_holdout_status_not_needed_for_partition(self):
        d = pd.DataFrame({'booking_date':pd.to_datetime(['2017-01-01']),
                          'planned_departure':[pd.NaT], 'status_date':[pd.NaT]})
        self.assertEqual(utils.assign_partition(d).iloc[0], 'final_holdout')

    def test_cutoff_day_and_inconsistent_dates(self):
        d = pd.DataFrame({'booking_date':pd.to_datetime(['2016-06-01']*3),
            'planned_departure':pd.to_datetime(['2016-07-01','2016-06-20','2016-06-20']),
            'status_date':pd.to_datetime(['2016-06-10','2016-07-01','2016-05-31'])})
        self.assertEqual(utils.assign_partition(d).tolist(),
                         ['train_unmatured','train_unmatured','train_date_inconsistent'])

if __name__ == '__main__': unittest.main()
