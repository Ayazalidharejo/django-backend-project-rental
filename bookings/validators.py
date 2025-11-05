from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


def validate_booking_dates(start_date, end_date, vehicle, booking_id=None):
    """
    Custom validator to check booking date conflicts.
    
    Args:
        start_date: Start date of the booking
        end_date: End date of the booking
        vehicle: Vehicle instance
        booking_id: Optional booking ID to exclude from conflict check
    
    Raises:
        ValidationError if dates are invalid or conflicts exist
    """
    if end_date < start_date:
        raise ValidationError("End date must be after start date.")
    
    if start_date < timezone.now().date():
        raise ValidationError("Start date cannot be in the past.")
    
    # Check for overlapping bookings
    overlapping = Booking.objects.filter(
        vehicle=vehicle,
        status__in=['pending', 'confirmed'],
        start_date__lte=end_date,
        end_date__gte=start_date
    )
    
    if booking_id:
        overlapping = overlapping.exclude(pk=booking_id)
    
    if overlapping.exists():
        raise ValidationError(
            "This vehicle is already booked for the selected dates. "
            f"Please choose different dates or another vehicle."
        )

