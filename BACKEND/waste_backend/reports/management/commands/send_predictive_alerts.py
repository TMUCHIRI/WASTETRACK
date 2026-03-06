# reports/management/commands/send_predictive_alerts.py
from django.core.management.base import BaseCommand
from reports.models import WasteReport
from reports.prediction import predict_fullness_date
from auth_app.at_service import send_sms
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Analyzes report history and sends predictive alerts to users'

    def handle(self, *args, **options):
        # We group by location to predict for each bin
        # In a real app, we'd have a 'Bin' model
        locations = WasteReport.objects.values('latitude', 'longitude').distinct()
        
        for loc in locations:
            lat, lng = loc['latitude'], loc['longitude']
            prediction = predict_fullness_date(lat, lng)
            
            if prediction:
                days_until_full = (prediction - timezone.now()).days
                
                if 0 <= days_until_full <= 2:
                    # Find the latest reporter for this bin to alert them
                    latest_report = WasteReport.objects.filter(
                        latitude=lat, longitude=lng
                    ).order_by('-created_at').first()
                    
                    if latest_report and latest_report.user.phone:
                        message = f"WasteTrack Alert: Based on patterns, your bin likely full in {days_until_full} days. Please update or report if full!"
                        self.stdout.write(f"Alerting {latest_report.user.phone}: {message}")
                        send_sms(latest_report.user.phone, message)
