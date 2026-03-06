from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Region, Team, CollectionSchedule
from reports.models import WasteReport
from django.utils import timezone

User = get_user_model()

class SchedulingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create Admin
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='password123',
            phone='+254711111111',
            role='admin'
        )
        
        # Create Collector
        self.collector = User.objects.create_user(
            email='collector@example.com',
            password='password123',
            phone='+254722222222',
            role='collector'
        )

        # Create Report
        self.report = WasteReport.objects.create(
            user=self.admin,
            waste_type='plastic',
            description='Dump',
            latitude=0.0,
            longitude=0.0
        )

        self.region_url = reverse('region-list-create')
        self.team_url = reverse('team-list-create')
        self.schedule_url = reverse('schedule-list-create')

    def test_create_region_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'Nairobi', 'county': 'Nairobi'}
        response = self.client.post(self.region_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Region.objects.count(), 1)

    def test_create_region_non_admin(self):
        self.client.force_authenticate(user=self.collector)
        data = {'name': 'Mombasa', 'county': 'Mombasa'}
        response = self.client.post(self.region_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_team_admin(self):
        self.client.force_authenticate(user=self.admin)
        region = Region.objects.create(name='Nairobi')
        data = {
            'name': 'Team Alpha',
            'lead': self.collector.id,
            'members': [self.collector.id],
            'region': region.id
        }
        response = self.client.post(self.team_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_create_schedule_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'report': self.report.id,
            'scheduled_date': timezone.now() + timezone.timedelta(days=1),
            'collector': self.collector.id,
            'notes': 'Urgent collection'
        }
        response = self.client.post(self.schedule_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CollectionSchedule.objects.count(), 1)

    def test_list_schedule_collector(self):
        # Create a schedule manually
        CollectionSchedule.objects.create(
            report=self.report,
            scheduled_date=timezone.now(),
            collector=self.collector
        )
        
        self.client.force_authenticate(user=self.collector)
        response = self.client.get(self.schedule_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_schedule_conflict(self):
        self.client.force_authenticate(user=self.admin)
        start = timezone.now() + timezone.timedelta(days=2)
        end = start + timezone.timedelta(hours=2)
        
        # Create first schedule
        CollectionSchedule.objects.create(
            report=self.report,
            scheduled_date=start,
            end_date=end,
            collector=self.collector
        )
        
        # Try to create second overlapping schedule for same collector
        report2 = WasteReport.objects.create(
            user=self.admin,
            waste_type='organic',
            description='Dump 2',
            latitude=1.0,
            longitude=1.0
        )
        
        data = {
            'report': report2.id,
            'scheduled_date': start + timezone.timedelta(hours=1),
            'end_date': end + timezone.timedelta(hours=1),
            'collector': self.collector.id
        }
        response = self.client.post(self.schedule_url, data)
        # Should fail with 400 because of validation error in save()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Conflict detected", str(response.data))

