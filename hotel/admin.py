from django.contrib import admin
from .models import Room, Booking, RoomImage, RoomType

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(RoomImage)
admin.site.register(RoomType)
