from django.shortcuts import render
from django.views.generic import ListView, View
from django.http import HttpResponse
from .room_types import ROOM_TYPES
from .models import Room, RoomImage, Booking, RoomType
from .forms import BookingForm
from hotel.utility_functions.room_availability import check_room_availability
from django.urls import reverse_lazy

# def RoomListView(request):
#     room = Room.objects.all()[0]
#     room_types = dict(ROOM_TYPES)
#     room_values = room_types.values()
#     room_list = []

#     for room_type in room_types:
#         room = room_types.get(room_type)
#         room_url = reverse_lazy('RoomDetailView', kwargs={'type': room_type})
#         room_list.append((room, room_url))
#     context = {
#         "room_list": room_list,
#     }
#     return render(request, 'room_list_view.html', context)

class RoomListView(ListView):
    model = RoomType
    context_object_name = 'rooms'
    template_name = "hotel/room_list.html"
    def get_queryset(self):
        return super().get_queryset().prefetch_related('roomimage_set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_list = []
        for room_type in self.object_list:
            room_type_name = room_type.room_type
            room_url = reverse_lazy('RoomDetailView', kwargs={'room_type': room_type_name})
            room_list.append((room_type, room_url))
        context['room_list'] = room_list
        return context

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
        """
        TO-DO: Only show "category does not exist when the category in the url is not a room category in the hhotel"
        """

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

class BookingListView(ListView):
    model = Booking

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

def custom_404(request, exception):
    return render(request, '404.html', status=404)
