> Historical development specification from the prior midterm stage. Current submission materials: deliverables/IS507_Midterm_Report.pdf and IS507_Midterm_Presentation.pptx. Current requirements: docs/MIDTERM_REVISION_REQUIREMENTS.md. The later test has already been scored under the preserved frozen protocol.

> Historical September 30 development specification. The original freeze is retained; the October 8 final-test extension is documented in [FINAL_EVALUATION_PROTOCOL](docs/FINAL_EVALUATION_PROTOCOL.md). Old unscored-holdout statements refer to the midterm stage.

# Project specification

**Working title:** Retrospective Ranking and Association Analysis of Hotel Booking Non-Completion

**Research question:** Which observable booking characteristics are associated with non-completion, and how well do they distinguish completed bookings from cancellations or no-shows in the eligible retrospective cohort?

**Outcome:** `is_canceled=1` includes Canceled and No-Show; `is_canceled=0` corresponds to recorded Check-Out. Unit: booking, not guest.

**Revised estimand:** Retrospective discrimination, probability quality and predictive associations within the fixed calendar- and maturity-selected sample. Released snapshots do not establish exact booking-creation-time availability. Neither causal effects nor prospective deployment performance are identified.

**Frozen design:** Existing features, calendar boundaries, combined maturity rule, fixed dummy/logistic models, train-only preprocessing and duplicate sensitivities remain the primary analysis. Status-only maturity is a descriptive cohort sensitivity. Final holdout remains unscored.

**Individual scope (2026-09-30 clarification):** The student takes responsibility for the complete analysis and prepares to explain every stage. No analytical modules are assigned away. This follows the student's account of the instructor's expectations; the supplied syllabus separately retains team submission and an individual analytical-choice component.
