from django.contrib import admin
from project_core.admin import custom_admin
from .models import Room, Booking, RoomImage, RoomType, RoomProperties

custom_admin.register(RoomImage)
custom_admin.register(RoomType)

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

@admin.register(RoomProperties)
class RoomPropertiesAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'number_of_beds', 'capacity', 'price_per_night']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['get_room_type', 'get_number_of_beds', 'get_capacity', 'get_price_per_night', 'display_check_in', 'display_check_out']
    list_filter = ['room__properties__room_type', 'check_in', 'check_out']

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


    # Display only the check in and check out dates in the admin panel i.e. exclude the time
    def display_check_in(self, obj):
        return obj.check_in.date()

    def display_check_out(self, obj):
        return obj.check_out.date()

    display_check_in.short_description = 'Check-in Date'
    display_check_out.short_description = 'Check-out Date'


custom_admin.register(RoomProperties, RoomPropertiesAdmin)
custom_admin.register(Room, RoomAdmin)
custom_admin.register(Booking, BookingAdmin)
