from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import SortedWasteLog, EducationalTip
from reports.models import WasteReport

User = get_user_model()

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='password123',
            phone='+254711111111',
            role='admin'
        )
        self.collector = User.objects.create_user(
            email='collector@example.com',
            password='password123',
            phone='+254722222222',
            role='collector'
        )
        self.report = WasteReport.objects.create(
            user=self.admin,
            waste_type='plastic',
            description='Test',
            latitude=0.0,
            longitude=0.0
        )
        
        self.log_url = reverse('waste-log-list-create')
        self.export_url = reverse('waste-log-export')
        self.tip_url = reverse('educational-tip-list')

    def test_log_waste(self):
        self.client.force_authenticate(user=self.collector)
        data = {
            'waste_type': 'plastic',
            'weight': 10.5,
            'report': self.report.id
        }
        response = self.client.post(self.log_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SortedWasteLog.objects.count(), 1)

    def test_export_csv_admin(self):
        SortedWasteLog.objects.create(
            waste_type='plastic',
            weight=5.0,
            logged_by=self.collector
        )
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.export_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment', response['Content-Disposition'])

    def test_export_csv_non_admin(self):
        self.client.force_authenticate(user=self.collector)
        response = self.client.get(self.export_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_educational_tips_public(self):
        EducationalTip.objects.create(title='Recycle Plastic', content='How to recycle...')
        response = self.client.get(self.tip_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
