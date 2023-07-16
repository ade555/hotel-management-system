from django.contrib import admin

# create a new custom admin panel for the website admin
class CustomAdmin(admin.AdminSite):
    site_header = 'Hotel Miramar SG Admin'
    site_title = 'Hotel Miramar SG Admin Panel'

custom_admin = CustomAdmin(name='custom-admin')