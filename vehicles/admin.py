from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate', 'make', 'model', 'year', 'owner', 'created_at')
    list_filter = ('make', 'year', 'created_at')
    search_fields = ('plate', 'make', 'model', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
