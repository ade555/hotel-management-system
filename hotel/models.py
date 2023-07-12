from django.db import models
from django.conf import settings

from .room_types import ROOM_TYPES

class RoomType(models.Model):
    room_type = models.CharField(max_length=15, choices=ROOM_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.room_type


class RoomProperties(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number_of_beds = models.IntegerField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name_plural = "Room properties"

class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    properties = models.ManyToManyField('RoomProperties')

class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return self.room_type.room_type
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def get_room_type(self):
        room_types = dict(ROOM_TYPES)
        room_properties = self.room.properties.first() if self.room.properties.exists() else None
        if room_properties:
            return room_types.get(room_properties.room_type.room_type)
        else:
            return None
