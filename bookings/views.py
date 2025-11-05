from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    All operations are scoped to the authenticated user's bookings only.
    Supports filtering by date range using query parameters.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Use different serializers for create vs retrieve/update"""
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Return only bookings for the current user, with optional filtering"""
        queryset = Booking.objects.filter(user=self.request.user)
        
        # Filter by start date (from parameter)
        from_date = self.request.query_params.get('from', None)
        if from_date:
            try:
                queryset = queryset.filter(start_date__gte=from_date)
            except ValueError:
                pass
        
        # Filter by end date (to parameter)
        to_date = self.request.query_params.get('to', None)
        if to_date:
            try:
                queryset = queryset.filter(end_date__lte=to_date)
            except ValueError:
                pass
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Set the user to the current user when creating a booking"""
        serializer.save(user=self.request.user, status='pending')

    def list(self, request, *args, **kwargs):
        """List all bookings with optional filters"""
        response = super().list(request, *args, **kwargs)
        # If response is already paginated, return as-is
        if isinstance(response.data, dict) and 'results' in response.data:
            return response
        # Otherwise, wrap in consistent format
        if isinstance(response.data, list):
            response.data = {
                'count': len(response.data),
                'results': response.data
            }
        return response
