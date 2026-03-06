from django.urls import path
from .views import (
    SortedWasteLogListCreateView,
    EducationalTipListView,
    EducationalTipAdminView,
    ExportWasteLogCSVView,
    SortingStatsView
)

urlpatterns = [
    path('logs/', SortedWasteLogListCreateView.as_view(), name='waste-log-list-create'),
    path('logs/export/', ExportWasteLogCSVView.as_view(), name='waste-log-export'),
    path('stats/', SortingStatsView.as_view(), name='sorting-stats'),
    path('tips/', EducationalTipListView.as_view(), name='educational-tip-list'),
    path('tips/admin/', EducationalTipAdminView.as_view(), name='educational-tip-admin'),
]
