from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import WasteReport

User = get_user_model()

class WasteReportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            phone='+254700000000',
            role='resident'
        )
        self.client.force_authenticate(user=self.user)
        self.list_create_url = '/api/reports/' # Based on root url include 'api/reports/' and app url ''

    def test_create_report(self):
        # Create a dummy valid image
        from io import BytesIO
        from PIL import Image
        
        file = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'JPEG')
        file.name = 'test_image.jpg'
        file.seek(0)
        
        image_file = SimpleUploadedFile("test_image.jpg", file.read(), content_type="image/jpeg")
        
        data = {
            'waste_type': 'plastic',
            'description': 'Plastic bottles dump',
            'latitude': -1.2921,
            'longitude': 36.8219,
            'urgency': 'medium',
            'image': image_file
        }
        
        response = self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(WasteReport.objects.count(), 1)
        report = WasteReport.objects.first()
        self.assertEqual(report.waste_type, 'plastic')
        self.assertEqual(report.latitude, -1.2921)

    def test_list_reports(self):
        # Create a report manually
        WasteReport.objects.create(
            user=self.user,
            waste_type='organic',
            description='Organic waste',
            latitude=0.0,
            longitude=0.0,
            image='reports/test.jpg' 
        )
        
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['waste_type'], 'organic')

    def test_create_report_invalid_data(self):
        data = {
            'waste_type': 'plastic',
            # Mission lat/long
        }
        response = self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
