from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'start_date', 'end_date', 'status', 'deposit_paid', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'deposit_paid', 'created_at')
    search_fields = ('user__username', 'vehicle__plate', 'vehicle__make', 'vehicle__model')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_date'
