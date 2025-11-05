from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from vehicles.models import Vehicle


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def clean(self):
        """Validate booking dates"""
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date must be after start date.")
            
            # Check for overlapping bookings for the same vehicle
            overlapping = Booking.objects.filter(
                vehicle=self.vehicle,
                status__in=['pending', 'confirmed'],
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            ).exclude(pk=self.pk if self.pk else None)
            
            if overlapping.exists():
                raise ValidationError(
                    "This vehicle is already booked for the selected dates."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle} ({self.start_date} to {self.end_date})"
