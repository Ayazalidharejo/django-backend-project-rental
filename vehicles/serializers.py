from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Vehicle
        fields = ('id', 'owner', 'owner_username', 'make', 'model', 'year', 'plate', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def validate_plate(self, value):
        return value.upper().strip()

