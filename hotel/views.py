from django.shortcuts import render
from django.views.generic import ListView, View
from django.http import HttpResponse
from .room_types import ROOM_TYPES
from .models import Room, RoomImage, Booking
from .forms import BookingForm
from hotel.utility_functions.room_availability import check_room_availability

class RoomListView(ListView):
    model = Room
    context_object_name = 'rooms'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_images = RoomImage.objects.all()
        context['room_images'] = room_images
        return context
    def get_queryset(self):
        return Room.objects.prefetch_related('properties')

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        room_type = self.kwargs.get('room_type', None)
        form = BookingForm()
        room_list = Room.objects.filter(properties__room_type__room_type=room_type)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(ROOM_TYPES).get(room.properties.all().first().room_type.room_type, None)

            print(room_category)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'hotel/room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        room_type = self.kwargs.get('room_type', None)
        room_list = Room.objects.filter(properties__room_type__room_type=room_type)
        form = BookingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_room_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
