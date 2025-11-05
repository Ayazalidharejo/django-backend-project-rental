from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Vehicle
        fields = ('id', 'owner', 'owner_username', 'make', 'model', 'year', 'plate', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def validate_year(self, value):
        # Check if year makes sense
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Year must be between 1900 and {current_year + 1}"
            )
        return value

    def validate_plate(self, value):
        # Normalize plate number to uppercase
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("License plate cannot be empty")
        return value.strip().upper()

