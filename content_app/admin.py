from django.contrib import admin
from project_core.admin import custom_admin
from .models import ContactMessage, TouristSpot

# register models to super admin with custom behaviour
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email']
    list_filter = ['created_at']

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ['tourist_spot_name', 'link']


# regoster models to custom admin with custom behaviour
custom_admin.register(ContactMessage, ContactAdmin)
custom_admin.register(TouristSpot, TouristSpotAdmin)
