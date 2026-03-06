# reports/models.py
from django.conf import settings
from django.utils import timezone
from django.db import models

class WasteReport(models.Model):
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

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned to Collector'),
        ('collected', 'Collected'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected/Inaccurate'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/')
    
    # Replace PointField with simple floats
    latitude = models.FloatField()
    longitude = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    urgency = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    estimated_fullness = models.IntegerField(default=0) # 0-100%
    threshold_bonus_awarded = models.BooleanField(default=False)
    admin_feedback = models.TextField(blank=True, null=True)
    collector_feedback = models.TextField(blank=True, null=True)
    collector_image = models.ImageField(upload_to='collection_photos/', blank=True, null=True)
    points_adjusted = models.BooleanField(default=False)  # True after admin awards/deducts based on collector feedback
    region = models.ForeignKey('scheduling.Region', on_delete=models.SET_NULL, null=True, blank=True)

    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports',
        limit_choices_to={'role': 'collector'}
    )

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
        ]
        ordering = ['-created_at']