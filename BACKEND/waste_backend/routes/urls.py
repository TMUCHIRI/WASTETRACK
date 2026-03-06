from django.urls import path
from .views import RouteListView, RouteGenerateView, RouteDetailView

urlpatterns = [
    path('', RouteListView.as_view(), name='route-list'),
    path('generate/', RouteGenerateView.as_view(), name='route-generate'),
    path('<int:pk>/', RouteDetailView.as_view(), name='route-detail'),
]
