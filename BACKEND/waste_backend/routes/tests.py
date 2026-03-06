from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from reports.models import WasteReport
from .models import OptimizedRoute

User = get_user_model()

class RouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.collector = User.objects.create_user(
            email='collector@example.com',
            password='password123',
            phone='+254722222222',
            role='collector'
        )
        
        # Create reports assigned to this collector
        self.report_low = WasteReport.objects.create(
            user=self.collector,
            waste_type='plastic',
            description='Low Urgency',
            latitude=-1.0,
            longitude=36.0,
            urgency='low',
            collector=self.collector,
            status='assigned'
        )
        self.report_high = WasteReport.objects.create(
            user=self.collector,
            waste_type='organic',
            description='High Urgency',
            latitude=-1.1,
            longitude=36.1,
            urgency='high',
            collector=self.collector,
            status='assigned'
        )
        
        self.generate_url = reverse('route-generate')
        self.list_url = reverse('route-list')

    def test_generate_route_collector(self):
        self.client.force_authenticate(user=self.collector)
        # Starting from Nairobi roughly
        data = {'latitude': -1.28, 'longitude': 36.82}
        response = self.client.post(self.generate_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OptimizedRoute.objects.count(), 1)
        
        route_data = response.data['route_data']
        # High urgency should be first because of our algorithm
        self.assertEqual(route_data[0]['id'], self.report_high.id)
        self.assertEqual(route_data[1]['id'], self.report_low.id)

    def test_generate_route_no_reports(self):
        # Create another collector with no assignments
        other_collector = User.objects.create_user(
            email='other@example.com',
            password='password123',
            phone='+254733333333',
            role='collector'
        )
        self.client.force_authenticate(user=other_collector)
        data = {'latitude': -1.0, 'longitude': 36.0}
        response = self.client.post(self.generate_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
