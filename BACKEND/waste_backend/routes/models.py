from django.db import models
from django.conf import settings
from reports.models import WasteReport

class OptimizedRoute(models.Model):
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='optimized_routes')
    created_at = models.DateTimeField(auto_now_add=True)
    # Storing ordered list of reports and their details
    route_data = models.JSONField(help_text="Ordered list of reports and coordinates")
    total_distance = models.FloatField(default=0.0, help_text="Total distance in km")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Route for {self.collector.email} - {self.created_at.date()}"
