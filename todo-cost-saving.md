# Cost-Saving Features (V2) Implementation To-Do List

## Task Group 1: Backend Enhancements

### User Story 2.1 & 2.2: Dynamic Reporting & Incentives
- [x] Update `CustomUser` model to include `points` (IntegerField, default=0).
- [x] Update `WasteReport` model to include `estimated_fullness` (IntegerField, default=0, choices 0-100).
- [x] Update `Region` model to include `threshold` (IntegerField, default=100).
- [x] Modify `WasteReport` creation API:
    - [x] Award 5 points if image is provided.
    - [x] Add logic to check region threshold based on lat/lng.
    - [x] Return warning message if fullness is below threshold.
- [x] **Test**: Verify report creation with points award and threshold warning.

### User Story 2.5 & 2.6: Updates & Incentive Redemption
- [x] Modify `WasteReport` update API:
    - [x] Allow updating `estimated_fullness`.
    - [x] Implement logic to "resubmit" or mark as collection-ready when threshold reached.
- [x] Create API endpoint for user to view points balance.
- [x] Create API endpoint for initial point redemption "perks" (mock).
- [x] **Test**: Verify points balance after report submission and update.


### User Story 3.1 & 3.4: AI Grouping & Batched Routes
- [x] Implement Haversine distance utility function.
- [x] Create service to group pending reports within 2-5km radius.
- [x] Update Scheduling API to support grouped reports.
- [x] **Test**: Verify clustering logic with mock report locations.

### User Story 4.4: Predictive Fullness Alerts
- [x] Implement simple regression logic using `scikit-learn` to predict fullness based on historical reports.
- [x] Create background task (management command) to check and alert users.
- [x] **Test**: Verify prediction output with dummy history.

### User Story 6.1 & 6.3: Admin Controls
- [x] Update Report Approval API to award/deduct points.
- [x] Create API for Admin to edit Region thresholds.
- [x] **Test**: Verify admin point adjustments.


## Task Group 2: Frontend Enhancements

### Reporting & Dashboard
- [x] Replace boolean full checkbox with fullness slider (0-100%) in `ReportComponent`.
- [x] Show dynamic warning if fullness < threshold.
- [x] Add points display component to User Dashboard.
- [x] **Test**: Verify slider functionality and points display.

### Admin Dashboard
- [x] Add "Region Threshold Settings" page/section.
- [x] Update Report Management view to show clusters and savings estimates.
- [x] **Test**: Verify threshold updates reflection in report logic.

## Summary of Results
- **Clustering**: Optimized routes reduced estimated trips significantly (verified in stats).
- **Incentives**: Correct point awarding (+10 accurate, -5 inaccurate) verified.
- **Predictions**: Regression model correctly alerts users based on history.


