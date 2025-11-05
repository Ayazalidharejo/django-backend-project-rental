from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    # Vehicle CRUD operations - only user's own vehicles
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter to show only current user's vehicles
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Auto-assign owner when creating
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        vehicle = self.get_object()
        self.perform_destroy(vehicle)
        return Response(
            {'message': 'Vehicle deleted successfully'},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        vehicle = self.get_object()
        serializer = self.get_serializer(vehicle, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Vehicle updated successfully',
            'data': serializer.data
        })
