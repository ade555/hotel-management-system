from hotel.models import Booking

# function to check if a room choosen by the user is available for booking
def check_room_availability(room, check_in, check_out):
    available_rooms_list = []
    booked_rooms_list = Booking.objects.filter(room=room)
    for booking in booked_rooms_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            available_rooms_list.append(True)
        else:
            available_rooms_list.append(False)
    return all(available_rooms_list)
