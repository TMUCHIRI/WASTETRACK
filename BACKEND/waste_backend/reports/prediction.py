# reports/prediction.py
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from .models import WasteReport

def predict_fullness_date(latitude, longitude):
    """
    Predicts when a bin at a specific location will reach 100% fullness
    based on historical reports at that location.
    Returns a datetime object or None.
    """
    # Get recent reports from this exact location (threshold within 50 meters)
    # Since we don't have PostGIS, we'll just filter by a small lat/lng range
    epsilon = 0.0005 # ~50m
    history = WasteReport.objects.filter(
        latitude__gte=latitude - epsilon,
        latitude__lte=latitude + epsilon,
        longitude__gte=longitude - epsilon,
        longitude__lte=longitude + epsilon
    ).order_by('created_at')
    
    if history.count() < 3:
        return None # Not enough data
    
    # Prepare data for Linear Regression
    # X: seconds since the first report in history
    # y: estimated_fullness
    
    start_time = history[0].created_at
    X = []
    y = []
    
    for report in history:
        seconds = (report.created_at - start_time).total_seconds()
        X.append([seconds])
        y.append(report.estimated_fullness)
        
    X = np.array(X)
    y = np.array(y)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Check if fullness is actually increasing
    if model.coef_[0] <= 0:
        return None # Fullness not increasing
    
    # Solve for y = 100
    # 100 = start_val + slope * target_seconds
    # target_seconds = (100 - intercept) / slope
    
    target_seconds = (100 - model.intercept_) / model.coef_[0]
    
    predicted_date = start_time + timedelta(seconds=float(target_seconds))
    
    # If the date is in the past (e.g. already should be full), cap it to 'soon'
    if predicted_date < datetime.now(predicted_date.tzinfo):
        return datetime.now(predicted_date.tzinfo) + timedelta(hours=1)
        
    return predicted_date
