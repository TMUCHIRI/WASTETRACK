from rest_framework import serializers
from .models import OptimizedRoute

class OptimizedRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizedRoute
        fields = '__all__'
        read_only_fields = ['collector', 'created_at', 'route_data', 'total_distance']
