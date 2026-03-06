from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+254[17]\d{8}$',
            message="Phone number must be in the format: '+2547xxxxxxxx' or '+2541xxxxxxxx'"
        )],
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    
    # Use phone or email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]

    ROLE_CHOICES = [
        ('collector', 'Collector'),
        ('admin', 'Admin'),
        ('citizen', 'Citizen'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    points = models.IntegerField(default=0)



class FCMDevice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fcm_devices')
    registration_token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.registration_token[:20]}"
