from rest_framework import serializers
from .models import Region, Team, CollectionSchedule
from reports.serializers import WasteReportSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    lead_details = UserSimpleSerializer(source='lead', read_only=True)
    member_details = UserSimpleSerializer(source='members', many=True, read_only=True)
    region_details = RegionSerializer(source='region', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'lead', 'lead_details', 'members', 'member_details', 'region', 'region_details']

class CollectionScheduleSerializer(serializers.ModelSerializer):
    report_details = WasteReportSerializer(source='report', read_only=True)
    team_details = TeamSerializer(source='team', read_only=True)
    collector_details = UserSimpleSerializer(source='collector', read_only=True)

    class Meta:
        model = CollectionSchedule
        fields = [
            'id', 'report', 'report_details', 'scheduled_date', 'end_date',
            'team', 'team_details', 'collector', 'collector_details', 'notes'
        ]

    def validate(self, data):
        # Create a temporary instance to call the model's clean method
        # This allows us to reuse the overlap detection logic
        instance = CollectionSchedule(**data)
        if self.instance:
            instance.pk = self.instance.pk
            
        from django.core.exceptions import ValidationError as DjangoValidationError
        try:
            instance.clean()
        except DjangoValidationError as e:
            # Convert Django's ValidationError to DRF's ValidationError
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else str(e))
        return data

