from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user)
        
        from_date = self.request.query_params.get('from', None)
        if from_date:
            try:
                queryset = queryset.filter(start_date__gte=from_date)
            except ValueError:
                pass
        
        to_date = self.request.query_params.get('to', None)
        if to_date:
            try:
                queryset = queryset.filter(end_date__lte=to_date)
            except ValueError:
                pass
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        days = (end_date - start_date).days + 1
        estimated_cost = days * 50
        deposit_amount = estimated_cost * 0.20
        
        serializer.save(
            user=self.request.user,
            status='pending',
            deposit_amount=deposit_amount,
            deposit_paid=False
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, dict) and 'results' in response.data:
            return response
        if isinstance(response.data, list):
            response.data = {
                'count': len(response.data),
                'results': response.data
            }
        return response
