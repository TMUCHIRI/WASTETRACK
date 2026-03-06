from django.urls import path
from .views import (
    RegionListCreateView, 
    TeamListCreateView, 
    CollectionScheduleListCreateView,
    CollectionScheduleDetailView
)

urlpatterns = [
    path('regions/', RegionListCreateView.as_view(), name='region-list-create'),
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('schedules/', CollectionScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', CollectionScheduleDetailView.as_view(), name='schedule-detail'),
]
