from django.db import models
from django.conf import settings
from reports.models import WasteReport

class SortedWasteLog(models.Model):
    WASTE_TYPES = [
        ('plastic', 'Plastic'),
        ('organic', 'Organic'),
        ('paper', 'Paper/Cardboard'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('ewaste', 'E-Waste'),
        ('hazardous', 'Hazardous'),
        ('general', 'General'),
    ]

    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    weight = models.FloatField(help_text="Weight in Kilograms")
    report = models.ForeignKey(WasteReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='sort_logs')
    logged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.weight}kg logged by {self.logged_by.email}"

class EducationalTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='tips/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
