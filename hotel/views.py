from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DeleteView
from django.http import HttpResponse, Http404
from django.contrib import messages
from .room_types import ROOM_TYPES
from .models import Room, RoomType, Booking
from .forms import BookingForm
from hotel.utility_functions.room_availability import check_room_availability
from django.urls import reverse_lazy
from datetime import timezone

class RoomListView(ListView):
    model = RoomType
    context_object_name = 'rooms'
    template_name = "hotel/room_list.html"
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('roomimage_set')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(room_type__icontains=search_query)
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_list = []
        for room_type in self.object_list:
            room_type_name = room_type.room_type
            room_url = reverse_lazy('hotel:RoomDetailView', kwargs={'room_type': room_type_name})
            room_list.append((room_type, room_url))
        context['room_list'] = room_list
        return context

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
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
            raise Http404('Category does not exist')

    def post(self, request, *args, **kwargs):
        room_type = self.kwargs.get('room_type', None)
        room_list = Room.objects.filter(properties__room_type__room_type=room_type)
        form = BookingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            check_out = data['check_out'].replace(tzinfo=timezone.utc)

            if check_out < data['check_in']:
                form.add_error('check_out', 'Cannot check out earlier than the check-in time')
                return render(request, 'hotel/room_detail_view.html', {'form': form})


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
            messages.success(request, f'You have successfully booked a {room_type} room')
            return redirect('hotel:BookingListView')
        else:
            messages.error(request, f'All {room_type} rooms have been booked. Please try another one.')
            return redirect('hotel:RoomListView')

class BookingListView(ListView):
    model = Booking

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class CancelBookingView(DeleteView):
    model = Booking
    success_url = reverse_lazy('hotel:BookingListView')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
