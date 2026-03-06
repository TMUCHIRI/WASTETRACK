# reports/serializers.py
from rest_framework import serializers
from .models import WasteReport

class WasteReportSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = WasteReport
        fields = [
            'id', 'user', 'waste_type', 'description', 'image',
            'latitude', 'longitude', 'urgency',
            'status', 'created_at', 'estimated_fullness', 'region',
            'admin_feedback', 'collector_feedback', 'collector_image',
            'collector', 'points_adjusted'
        ]

        read_only_fields = ['status', 'created_at', 'user']

    # Remove custom create method as perform_create in view handles user assignment via serializer.save(user=...)
    # which injects it into validated_data