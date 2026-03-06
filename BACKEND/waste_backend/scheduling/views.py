from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Region, Team, CollectionSchedule
from .serializers import RegionSerializer, TeamSerializer, CollectionScheduleSerializer
from reports.permissions import IsAdmin, IsCollector
from django.db.models import Q

class RegionListCreateView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class CollectionScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = CollectionScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CollectionSchedule.objects.all()
        elif user.role == 'collector':
            # Collector's individual assignment or team assignment
            return CollectionSchedule.objects.filter(
                Q(collector=user) | Q(team__members=user)
            ).distinct()
        return CollectionSchedule.objects.none()

    def perform_create(self, serializer):
        # Only admins can create schedules for now as per Story 3.1/3.2 logic
        if self.request.user.role != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only admins can create schedules.")
        serializer.save()

class CollectionScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CollectionSchedule.objects.all()
    serializer_class = CollectionScheduleSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
