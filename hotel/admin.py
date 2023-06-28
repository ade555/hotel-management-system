from django.contrib import admin
from .models import Room, Booking, RoomImage, RoomType, RoomProperties

admin.site.register(RoomImage)
admin.site.register(RoomType)
admin.site.register(RoomProperties)



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'get_room_type', 'get_number_of_beds', 'get_capacity', 'get_price_per_night']
    ordering = ['room_number']
    list_display_links = ['room_number']
    list_filter = ['properties__room_type', 'properties__number_of_beds', 'properties__capacity', 'properties__price_per_night']
    search_fields = ['room_number']

    def get_room_property(self, obj, property_name):
        room_properties = obj.properties.first()
        if room_properties:
            return getattr(room_properties, property_name)
        return None

    def get_room_type(self, obj):
        return self.get_room_property(obj, 'room_type')
    get_room_type.short_description = 'Room Type'

    def get_number_of_beds(self, obj):
        return self.get_room_property(obj, 'number_of_beds')
    get_number_of_beds.short_description = 'Number of Beds'

    def get_capacity(self, obj):
        return self.get_room_property(obj, 'capacity')
    get_capacity.short_description = 'Room Capacity'

    def get_price_per_night(self, obj):
        return self.get_room_property(obj, 'price_per_night')
    get_price_per_night.short_description = 'Room Price per night'



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['get_room_type', 'get_number_of_beds', 'get_capacity', 'get_price_per_night']
    list_filter = ['room__properties__room_type',]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('room__properties')
        return queryset

    def get_booked_room_property(self, obj, property_name):
        booked_room = obj.room
        if booked_room:
            room_properties = booked_room.properties.first()
            if room_properties:
                return getattr(room_properties, property_name)
        return None

    def get_room_type(self, obj):
        return self.get_booked_room_property(obj, 'room_type')
    get_room_type.short_description = 'Room Type'

    def get_number_of_beds(self, obj):
        return self.get_booked_room_property(obj, 'number_of_beds')
    get_number_of_beds.short_description = 'Number of Beds'

    def get_capacity(self, obj):
        return self.get_booked_room_property(obj, 'capacity')
    get_capacity.short_description = 'Room Capacity'

    def get_price_per_night(self, obj):
        return self.get_booked_room_property(obj, 'price_per_night')
    get_price_per_night.short_description = 'Room Price per night'