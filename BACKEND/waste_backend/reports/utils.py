# reports/utils.py
import math
import requests
from django.conf import settings

def send_sms_alert(report):
    # Mock SMS sending
    print(f"MOCK SMS SENT TO {report.user.phone}: Waste collected at {report.latitude}, {report.longitude}. Thank you!")

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    R = 6371 # Radius of earth in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(dlambda / 2)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_google_maps_distance(origin_lat, origin_lng, dest_lat, dest_lng):
    """
    Placeholder for Google Maps Distance Matrix API call.
    Useful for 'real road distance' instead of 'as the crow flies'.
    """
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    if not api_key:
        return calculate_haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
    
    # In production:
    # url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_lat},{origin_lng}&destinations={dest_lat},{dest_lng}&key={api_key}"
    # response = requests.get(url).json()
    # return response['rows'][0]['elements'][0]['distance']['value'] / 1000 # returns km
    return calculate_haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)

def find_nearest_region(lat, lng):
    from scheduling.models import Region
    regions = Region.objects.all()
    if not regions.exists():
        return None
    
    nearest_region = None
    min_distance = float('inf')
    
    for region in regions:
        if region.latitude is not None and region.longitude is not None:
            dist = calculate_haversine_distance(lat, lng, region.latitude, region.longitude)
            if dist < min_distance:
                min_distance = dist
                nearest_region = region
    
    return nearest_region

def cluster_reports(reports_queryset, radius_km=5.0):
    """
    Groups reports by proximity using DBSCAN.
    Radius is in kilometers.
    """
    import numpy as np
    from sklearn.cluster import DBSCAN
    
    if not reports_queryset:
        return []

        
    # Prepare coordinates (latitude, longitude)
    coords = np.array([[r.latitude, r.longitude] for r in reports_queryset])
    
    # DBSCAN with haversine metric requires coordinates in radians
    kms_per_radian = 6371.0
    epsilon = radius_km / kms_per_radian
    
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')
    db.fit(np.radians(coords))
    
    clusters = {}
    for idx, label in enumerate(db.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(reports_queryset[idx])
        
    return list(clusters.values())
