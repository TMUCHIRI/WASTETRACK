from django.db import models
from django.conf import settings
from reports.models import WasteReport

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    county = models.CharField(max_length=100, blank=True) # Optional: Kenyan County
    threshold = models.IntegerField(default=100) # Fullness percentage to trigger collection
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='led_teams',
        limit_choices_to={'role': 'collector'}
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='teams',
        limit_choices_to={'role': 'collector'}
    )
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class CollectionSchedule(models.Model):
    report = models.OneToOneField(WasteReport, on_delete=models.CASCADE, related_name='schedule')
    scheduled_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'collector'}
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['scheduled_date']

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.db.models import Q
        
        if self.scheduled_date and self.end_date:
            if self.end_date <= self.scheduled_date:
                raise ValidationError("End date must be after scheduled date.")
            
            # Check for overlaps
            query = Q()
            if self.collector:
                query |= Q(collector=self.collector)
            if self.team:
                query |= Q(team=self.team)
                
            if query:
                overlaps = CollectionSchedule.objects.filter(
                    query,
                    scheduled_date__lt=self.end_date,
                    end_date__gt=self.scheduled_date
                ).exclude(pk=self.pk)
                
                if overlaps.exists():
                    raise ValidationError("Conflict detected: This collector/team is already scheduled during this time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Schedule for {self.report.id} on {self.scheduled_date}"
