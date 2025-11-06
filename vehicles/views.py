from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
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
