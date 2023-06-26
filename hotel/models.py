from django.db import models
from django.conf import settings
# from django.urls import reverse_lazy

from .room_types import ROOM_TYPES

class RoomType(models.Model):
    room_type = models.CharField(max_length=15, choices=ROOM_TYPES)

    def __str__(self):
        return self.room_type


class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number_of_beds = models.IntegerField()
    description = models.TextField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Room {self.room_number} \nType: {self.room_type}"

class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return self.room_type
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()