from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OptimizedRoute
from .serializers import OptimizedRouteSerializer
from .utils import generate_smart_route
from reports.permissions import IsCollector, IsAdmin

class RouteListView(generics.ListAPIView):
    serializer_class = OptimizedRouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return OptimizedRoute.objects.all()
        return OptimizedRoute.objects.filter(collector=user)

class RouteGenerateView(APIView):
    permission_classes = [IsCollector]
    
    def post(self, request):
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        
        if lat is None or lng is None:
            return Response({'error': 'Latitude and Longitude are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            route_data, total_dist = generate_smart_route(request.user, float(lat), float(lng))
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not route_data:
            return Response({'message': 'No assigned reports found to route.'}, status=status.HTTP_404_NOT_FOUND)
            
        route = OptimizedRoute.objects.create(
            collector=request.user,
            route_data=route_data,
            total_distance=total_dist
        )
        
        return Response(OptimizedRouteSerializer(route).data, status=status.HTTP_201_CREATED)

class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OptimizedRoute.objects.all()
    serializer_class = OptimizedRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return OptimizedRoute.objects.all()
        return OptimizedRoute.objects.filter(collector=user)
