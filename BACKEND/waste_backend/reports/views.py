from django.shortcuts import render
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Count
from django.utils import timezone
from .models import WasteReport
from .serializers import WasteReportSerializer
from .utils import send_sms_alert
from scheduling.models import CollectionSchedule
import logging

logger = logging.getLogger(__name__)

class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = WasteReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return WasteReport.objects.all().order_by('-created_at')
        return WasteReport.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        
        # Award 5 points if image is provided
        if report.image:
            user = self.request.user
            user.points += 5
            user.save()

        # Find nearest region and associate
        from .utils import find_nearest_region
        region = find_nearest_region(report.latitude, report.longitude)
        if region:
            report.region = region
            # Award bonus points if threshold is reached on creation
            if report.estimated_fullness >= region.threshold:
                user = self.request.user
                user.points += 10
                user.save()
                report.threshold_bonus_awarded = True
            report.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        report = WasteReport.objects.get(id=serializer.data['id'])
        response_data = serializer.data
        
        # Add threshold warning
        if report.region and report.estimated_fullness < report.region.threshold and report.urgency != 'high':
            response_data['warning'] = f"Collection may be delayed until fullness reaches {report.region.threshold}%."
            response_data['threshold_not_met'] = True
            
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class UserPointsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'points': request.user.points
        })

class ReportListView(generics.ListAPIView):
    serializer_class = WasteReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return WasteReport.objects.all().order_by('-created_at')
        return WasteReport.objects.filter(user=self.request.user).order_by('-created_at')
    
from .permissions import IsCollector

class CollectorReportListView(generics.ListAPIView):
    serializer_class = WasteReportSerializer
    permission_classes = [IsCollector]

    def get_queryset(self):
        user = self.request.user
        return WasteReport.objects.filter(status='assigned', collector=user)

class UpdateReportStatusView(views.APIView):
    permission_classes = [IsCollector]

    def patch(self, request, pk):
        try:
            report = WasteReport.objects.get(pk=pk)
        except WasteReport.DoesNotExist:
            return Response({'error': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        if report.collector != request.user:
            raise PermissionDenied("Not your report.")

        new_status = request.data.get('status')
        if new_status not in ['collected', 'verified']:
            raise ValidationError("Invalid status.")

        report.status = new_status

        feedback = request.data.get('collector_feedback')
        if feedback:
            report.collector_feedback = feedback

        if 'collector_image' in request.FILES:
            report.collector_image = request.FILES['collector_image']

        report.save()

        if new_status == 'collected':
            send_sms_alert(report)
            if hasattr(report, 'schedule'):
                report.schedule.end_date = timezone.now()
                report.schedule.save()

        return Response(WasteReportSerializer(report).data, status=status.HTTP_200_OK)

from .permissions import IsAdmin

class AdminStatsView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total = WasteReport.objects.count()
        pending = WasteReport.objects.filter(status='pending').count()
        collected = WasteReport.objects.filter(status='collected').count()
        verified = WasteReport.objects.filter(status='verified').count()
        by_type = WasteReport.objects.values('waste_type').annotate(count=Count('id'))
        
        from .utils import cluster_reports
        eligible = WasteReport.objects.filter(status='pending', estimated_fullness__gte=80)
        clusters = cluster_reports(eligible, radius_km=3.0)
        trips_saved = max(0, eligible.count() - len(clusters))
        fuel_savings = trips_saved * 2.5 
        
        return Response({
            'total': total,
            'pending': pending,
            'collected': collected,
            'verified': verified,
            'by_type': {item['waste_type']: item['count'] for item in by_type},
            'savings': {
                'trips_saved': trips_saved,
                'estimated_fuel_saved_liters': fuel_savings,
                'accuracy_rate': (verified / collected * 100) if collected > 0 else 0
            }
        })

class AssignReportView(generics.UpdateAPIView):
    queryset = WasteReport.objects.all()
    serializer_class = WasteReportSerializer
    permission_classes = [IsAdmin]

    def patch(self, request, *args, **kwargs):
        report = self.get_object()
        collector_id = request.data.get('collector')
        if collector_id:
            report.collector_id = collector_id
            report.status = 'assigned'
            report.save()

            CollectionSchedule.objects.update_or_create(
                report=report,
                defaults={
                    'collector_id': collector_id,
                    'scheduled_date': timezone.now()
                }
            )
        return Response(WasteReportSerializer(report).data)

class AdminRegionThresholdView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from scheduling.models import Region
        regions = Region.objects.all()
        from django.forms.models import model_to_dict
        return Response([model_to_dict(r) for r in regions])

    def post(self, request):
        from scheduling.models import Region
        name = request.data.get('name')
        threshold = request.data.get('threshold', 100)
        county = request.data.get('county', '')
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        
        region, created = Region.objects.update_or_create(
            name=name,
            defaults={
                'threshold': threshold,
                'county': county,
                'latitude': lat,
                'longitude': lng
            }
        )
        return Response({'success': True, 'region': region.id})

class ReportUpdateView(generics.RetrieveUpdateAPIView):
    queryset = WasteReport.objects.all()
    serializer_class = WasteReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        report = self.get_object()
        user_role = getattr(self.request.user, 'role', 'unknown')
        if report.user != self.request.user and user_role != 'admin':
            raise PermissionDenied("Not your report.")
        
        old_fullness = report.estimated_fullness
        old_status = report.status
        
        new_report = serializer.save()

        # Resubmission logic: Reset status to pending if it was rejected
        if old_status == 'rejected' and user_role != 'admin':
            WasteReport.objects.filter(id=new_report.id).update(status='pending', admin_feedback=None)
            new_report.status = 'pending'
            new_report.admin_feedback = None

        # Award 10 points if threshold is reached and bonus wasn't awarded yet
        if (new_report.region and not new_report.threshold_bonus_awarded and 
            new_report.estimated_fullness >= new_report.region.threshold):
            user = new_report.user
            user.points += 10
            user.save()
            new_report.threshold_bonus_awarded = True
            new_report.save()
        self.bonus_awarded = (new_report.threshold_bonus_awarded and old_fullness < new_report.region.threshold)

    def update(self, request, *args, **kwargs):
        self.bonus_awarded = False
        response = super().update(request, *args, **kwargs)
        if self.bonus_awarded:
            response.data['bonus_awarded'] = True
            response.data['message'] = "Congratulations! You earned 10 bonus points for reporting a full bin."
        return response

class PointRedeemView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        perk = request.data.get('perk')
        cost = 50 
        if request.user.points >= cost:
            request.user.points -= cost
            request.user.points = max(0, request.user.points)
            request.user.save()
            return Response({'success': True, 'message': f'Redeemed {perk} for {cost} points.'})
        return Response({'success': False, 'message': 'Insufficient points.'}, status=status.HTTP_400_BAD_REQUEST)

class AdminVerifyReportView(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        report = WasteReport.objects.get(pk=pk)
        is_accurate = request.data.get('is_accurate', True)
        feedback = request.data.get('feedback', '')
        
        if is_accurate:
            report.status = 'verified'
            report.save()
            user = report.user
            user.points += 10
            user.save()
            return Response({'success': True, 'message': 'Report verified. 10 points awarded.'})
        else:
            report.status = 'rejected'
            report.admin_feedback = feedback
            report.save()
            user = report.user
            user.points -= 5
            user.points = max(0, user.points)
            user.save()
            return Response({'success': True, 'message': 'Report marked inaccurate. 5 points deducted.'})

class AdminReportClustersView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from .utils import cluster_reports
        eligible_reports = []
        all_pending = WasteReport.objects.filter(status='pending')
        
        for report in all_pending:
            threshold = 100
            if report.region:
                threshold = report.region.threshold
            if report.estimated_fullness >= threshold or report.urgency == 'high':
                eligible_reports.append(report)
        
        if not eligible_reports:
            return Response([])

        clusters = cluster_reports(eligible_reports, radius_km=3.0)
        results = []
        for i, cluster in enumerate(clusters):
            cluster_data = {
                'cluster_id': i,
                'count': len(cluster),
                'reports': WasteReportSerializer(cluster, many=True).data,
                'center': {
                    'latitude': sum(r.latitude for r in cluster) / len(cluster),
                    'longitude': sum(r.longitude for r in cluster) / len(cluster)
                }
            }
            results.append(cluster_data)
        return Response(results)


class AdminAdjustPointsView(views.APIView):
    """Admin endpoint to award/deduct points from a citizen based on collector feedback."""
    permission_classes = [IsAdmin]

    def post(self, request):
        from auth_app.models import CustomUser
        user_id = request.data.get('user_id')
        delta = request.data.get('delta', 0)
        reason = request.data.get('reason', '')
        report_id = request.data.get('report_id')  # optional – mark points_adjusted

        try:
            delta = int(delta)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid delta value.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            citizen = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Guard: if a report_id was given, check it hasn't already been adjusted
        report = None
        if report_id:
            try:
                report = WasteReport.objects.get(pk=report_id)
                if report.points_adjusted:
                    return Response(
                        {'error': 'Points for this report have already been adjusted.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except WasteReport.DoesNotExist:
                pass  # report_id is optional; proceed without it

        citizen.points = max(0, citizen.points + delta)
        citizen.save()

        # Mark the report so the UI disables the buttons
        if report:
            report.points_adjusted = True
            report.save(update_fields=['points_adjusted'])

        action = 'awarded' if delta > 0 else 'deducted'
        return Response({
            'success': True,
            'message': f'{abs(delta)} points {action} for {citizen.email}. {reason}',
            'new_points': citizen.points
        })

