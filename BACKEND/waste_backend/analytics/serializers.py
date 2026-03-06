from rest_framework import serializers
from .models import SortedWasteLog, EducationalTip

class SortedWasteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedWasteLog
        fields = '__all__'
        read_only_fields = ['logged_by', 'logged_at']

class EducationalTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalTip
        fields = '__all__'
