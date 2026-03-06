from rest_framework import generics, permissions
from .models import SortedWasteLog, EducationalTip
from .serializers import SortedWasteLogSerializer, EducationalTipSerializer
from reports.permissions import IsAdmin, IsCollector
import csv
from django.http import HttpResponse

class SortedWasteLogListCreateView(generics.ListCreateAPIView):
    queryset = SortedWasteLog.objects.all()
    serializer_class = SortedWasteLogSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()] # Both admin and collector can log
        return [IsAdmin()] # Only admin can list all for now (or collector can list their own - but let's keep it admin for analytics)

    def perform_create(self, serializer):
        serializer.save(logged_by=self.request.user)

class EducationalTipListView(generics.ListAPIView):
    queryset = EducationalTip.objects.all()
    serializer_class = EducationalTipSerializer
    permission_classes = [permissions.AllowAny]

class EducationalTipAdminView(generics.ListCreateAPIView):
    queryset = EducationalTip.objects.all()
    serializer_class = EducationalTipSerializer
    permission_classes = [IsAdmin]

class ExportWasteLogCSVView(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="waste_logs.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Waste Type', 'Weight (kg)', 'Report ID', 'Logged By', 'Date'])
        
        logs = SortedWasteLog.objects.all()
        for log in logs:
            writer.writerow([
                log.id, log.waste_type, log.weight, 
                log.report.id if log.report else 'N/A',
                log.logged_by.email, log.logged_at
            ])
            
        return response
from django.db.models import Sum
from rest_framework.response import Response

class SortingStatsView(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        total_weight = SortedWasteLog.objects.aggregate(Sum('weight'))['weight__sum'] or 0
        by_type = SortedWasteLog.objects.values('waste_type').annotate(total_weight=Sum('weight'))
        
        return Response({
            'total_weight_kg': total_weight,
            'by_type_weight': {item['waste_type']: item['total_weight'] for item in by_type}
        })
