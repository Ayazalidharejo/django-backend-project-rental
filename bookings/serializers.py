from rest_framework import serializers
from .models import Booking
from datetime import date


class BookingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'user_username', 'vehicle', 'vehicle_details',
            'start_date', 'end_date', 'status', 'deposit_amount',
            'deposit_paid', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'status', 'deposit_amount', 'deposit_paid', 'created_at', 'updated_at')

    def get_vehicle_details(self, obj):
        return {
            'id': obj.vehicle.id,
            'make': obj.vehicle.make,
            'model': obj.vehicle.model,
            'year': obj.vehicle.year,
            'plate': obj.vehicle.plate,
        }

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        vehicle = attrs.get('vehicle')

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({"end_date": "End date must be after start date."})

            if vehicle:
                overlapping = Booking.objects.filter(
                    vehicle=vehicle,
                    status__in=['pending', 'confirmed'],
                    start_date__lte=end_date,
                    end_date__gte=start_date
                ).exclude(pk=self.instance.pk if self.instance else None)

                if overlapping.exists():
                    raise serializers.ValidationError(
                        "This vehicle is already booked for the selected dates."
                    )

        return attrs


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('vehicle', 'start_date', 'end_date')

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        vehicle = attrs.get('vehicle')

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({"end_date": "End date must be after start date."})

            if vehicle:
                overlapping = Booking.objects.filter(
                    vehicle=vehicle,
                    status__in=['pending', 'confirmed'],
                    start_date__lte=end_date,
                    end_date__gte=start_date
                )

                if overlapping.exists():
                    raise serializers.ValidationError(
                        "This vehicle is already booked for the selected dates."
                    )

        return attrs

