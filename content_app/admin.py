from django.contrib import admin
from project_core.admin import custom_admin
from .models import ContactMessage, TouristSpot

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email']
    list_filter = ['created_at']
custom_admin.register(ContactMessage, ContactAdmin)

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ['tourist_spot_name', 'link']
custom_admin.register(TouristSpot, TouristSpotAdmin)
