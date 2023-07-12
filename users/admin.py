from django.contrib import admin
from project_core.admin import custom_admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', "last_name", 'email', 'profile_picture', 'is_active', "last_login"]
    list_display = ['first_name', 'last_name', 'email']

custom_admin.register(User, UserAdmin)
