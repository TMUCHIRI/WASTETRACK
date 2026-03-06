from django.urls import path
from .views import (
    AdminStatsView, AssignReportView, CollectorReportListView, 
    ReportListCreateView, UpdateReportStatusView, UserPointsView,
    AdminRegionThresholdView, ReportUpdateView, PointRedeemView,
    AdminReportClustersView, AdminVerifyReportView, AdminAdjustPointsView
)

urlpatterns = [
    path('', ReportListCreateView.as_view(), name='report-list-create'),
    path('<int:pk>/', ReportUpdateView.as_view(), name='report-detail-update'),
    path('points/', UserPointsView.as_view(), name='user-points'),
    path('points/redeem/', PointRedeemView.as_view(), name='point-redeem'),
    path('admin/clusters/', AdminReportClustersView.as_view(), name='admin-clusters'),
    path('<int:pk>/verify/', AdminVerifyReportView.as_view(), name='admin-verify'),



    path('collector/', CollectorReportListView.as_view(), name='collector-reports'),
    path('<int:pk>/status/', UpdateReportStatusView.as_view(), name='update-status'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('<int:pk>/assign/', AssignReportView.as_view(), name='assign-report'),
    path('admin/regions/', AdminRegionThresholdView.as_view(), name='admin-regions'),
    path('admin/adjust-points/', AdminAdjustPointsView.as_view(), name='admin-adjust-points'),
]
