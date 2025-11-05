from rest_framework import serializers
from django.utils import timezone
from .models import Booking
from .validators import validate_booking_dates
from vehicles.serializers import VehicleSerializer


class BookingSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'user_username', 'vehicle', 'vehicle_details',
            'start_date', 'end_date', 'status', 'deposit_amount',
            'deposit_paid', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'status', 'created_at', 'updated_at')

    def validate_start_date(self, value):
        # Don't allow past dates
        if value < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        # Don't allow past dates
        if value < timezone.now().date():
            raise serializers.ValidationError("End date cannot be in the past.")
        return value

    def validate(self, attrs):
        # Check for booking conflicts and date validity
        start_date = attrs.get('start_date') or (self.instance.start_date if self.instance else None)
        end_date = attrs.get('end_date') or (self.instance.end_date if self.instance else None)
        vehicle = attrs.get('vehicle') or (self.instance.vehicle if self.instance else None)
        booking_id = self.instance.pk if self.instance else None

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })
            
            if vehicle:
                try:
                    validate_booking_dates(start_date, end_date, vehicle, booking_id)
                except Exception as e:
                    raise serializers.ValidationError(str(e))
        
        return attrs


class BookingCreateSerializer(serializers.ModelSerializer):
    # Used when creating new bookings - calculates deposit automatically
    class Meta:
        model = Booking
        fields = ('vehicle', 'start_date', 'end_date', 'deposit_amount')
        read_only_fields = ('deposit_amount',)

    def validate_start_date(self, value):
        # Can't book in the past
        if value < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        # Can't book in the past
        if value < timezone.now().date():
            raise serializers.ValidationError("End date cannot be in the past.")
        return value

    def validate(self, attrs):
        # Validate dates and calculate deposit
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        vehicle = attrs.get('vehicle')
        booking_id = self.instance.pk if self.instance else None

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })
            
            if vehicle:
                try:
                    validate_booking_dates(start_date, end_date, vehicle, booking_id)
                except Exception as e:
                    raise serializers.ValidationError(str(e))
                
                # Auto-calculate deposit: 20% of total rental cost
                days = (end_date - start_date).days + 1
                daily_rate = 50.00  # Base rate per day
                attrs['deposit_amount'] = (days * daily_rate) * 0.20
        
        return attrs

