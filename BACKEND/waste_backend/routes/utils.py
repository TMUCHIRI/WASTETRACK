from reports.models import WasteReport
from reports.utils import calculate_haversine_distance

def generate_smart_route(collector, start_lat, start_lng):
    """
    Generate an optimized route for a collector using a greedy approach.
    Prioritizes High Urgency reports, then distance.
    """
    # Get all reports assigned to this collector that are not yet collected
    reports = list(WasteReport.objects.filter(collector=collector, status='assigned'))
    
    if not reports:
        return [], 0.0

    optimized_reports = []
    current_lat = start_lat
    current_lng = start_lng
    total_distance = 0.0

    while reports:
        # Filter for high urgency if any
        high_urgency = [r for r in reports if r.urgency == 'high']
        targets = high_urgency if high_urgency else reports
        
        # Find the closest report in the target list
        closest_report = min(
            targets,
            key=lambda r: calculate_haversine_distance(current_lat, current_lng, r.latitude, r.longitude)
        )
        
        dist = calculate_haversine_distance(current_lat, current_lng, closest_report.latitude, closest_report.longitude)
        total_distance += dist
        
        # Add to optimized list
        optimized_reports.append({
            'id': closest_report.id,
            'waste_type': closest_report.waste_type,
            'latitude': closest_report.latitude,
            'longitude': closest_report.longitude,
            'urgency': closest_report.urgency,
            'distance_from_previous': dist
        })
        
        # Update current position
        current_lat = closest_report.latitude
        current_lng = closest_report.longitude
        
        # Remove from remaining reports
        reports.remove(closest_report)

    return optimized_reports, total_distance
