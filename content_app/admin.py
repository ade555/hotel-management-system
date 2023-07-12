from django.contrib import admin
from project_core.admin import custom_admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email']
    list_filter = ['created_at']
custom_admin.register(ContactMessage, ContactAdmin)

# Register your models here.
