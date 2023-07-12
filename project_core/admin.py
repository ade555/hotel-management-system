from django.contrib import admin

class CustomAdmin(admin.AdminSite):
    site_header = 'Hello'
    login_template = 'admin/login.html'

custom_admin = CustomAdmin(name='custom-admin')