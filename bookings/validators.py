from django.core.exceptions import ValidationError
from datetime import date
from .models import Booking


def validate_future_date(value):
    if value < date.today():
        raise ValidationError("Date cannot be in the past.")


def validate_booking_dates(start_date, end_date):
    if end_date < start_date:
        raise ValidationError("End date must be after start date.")
    
    if start_date < date.today():
        raise ValidationError("Start date cannot be in the past.")


def validate_no_overlap(vehicle, start_date, end_date, exclude_booking=None):
    overlapping = Booking.objects.filter(
        vehicle=vehicle,
        status__in=['pending', 'confirmed'],
        start_date__lte=end_date,
        end_date__gte=start_date
    )
    
    if exclude_booking:
        overlapping = overlapping.exclude(pk=exclude_booking.pk)
    
    if overlapping.exists():
        raise ValidationError(
            "This vehicle is already booked for the selected dates."
        )

