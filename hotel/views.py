from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DeleteView
from django.http import Http404
from django.contrib import messages
from .room_types import ROOM_TYPES
from .models import Room, RoomType, Booking, RoomImage
from .forms import BookingForm
from hotel.utility_functions.room_availability import check_room_availability
from django.urls import reverse_lazy
from datetime import timezone, datetime

class RoomListView(ListView):
    model = RoomType
    context_object_name = 'rooms'
    template_name = "hotel/room_list.html"

     # create queryset based user's search input
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('roomimage_set', 'roomproperties_set')

        #get search query from user input
        search_query = self.request.GET.get('search')

        if search_query:
            # filter queryset by the search key word and return closely matched results
            queryset = queryset.filter(
                Q(room_type__icontains=search_query)  # Match room type
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search')
        room_list = []
        for room_type in self.object_list:
            room_type_name = room_type.room_type
            room_url = reverse_lazy('hotel:RoomDetailView', kwargs={'room_type': room_type_name})
            room_list.append((room_type, room_url))
        context['room_list'] = room_list
        context['search'] = search_query
        return context

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        # get the room type from the url
        room_type = self.kwargs.get('room_type', None)
        form = BookingForm()

        # get the list of rooms available in the room type
        room_list = Room.objects.filter(properties__room_type__room_type=room_type)

        # get the associated properties of the room type and return it
        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(ROOM_TYPES).get(room.properties.all().first().room_type.room_type, None)
            room_type_obj = RoomType.objects.get(room_type=room_type)  # Get RoomType object
            room_images = RoomImage.objects.filter(room_type=room_type_obj)

            context = {
                'room_category': room_category,
                'form': form,
                'room_images':room_images,
                'room_type_obj':room_type_obj,
            }
            return render(request, 'hotel/room_detail_view.html', context)
        else:
            # return a 404 message if there are no rooms in that category
            raise Http404('Category does not exist')
    
    # Post request to handle the event where the user decides to book a room
    def post(self, request, *args, **kwargs):
        # get the room type from the url
        room_type = self.kwargs.get('room_type', None)

        # get all the rooms for that specific room type
        room_list = Room.objects.filter(properties__room_type__room_type=room_type)

        form = BookingForm(request.POST)


        if form.is_valid():
            # get data from the form
            data = form.cleaned_data

            check_out = data['check_out'].replace(tzinfo=timezone.utc)
            current_day = datetime.now(timezone.utc)

            # validate if user is booking the room with correct dates and time
            if check_out < data['check_in'] or data['check_in'] < current_day:
                form.add_error('check_out', 'Cannot check out earlier than the check-in time')
                form.add_error('check_in', 'Cannot check in at a previous date')
                return render(request, 'hotel/room_detail_view.html', {'form': form})


        # check for the number of rooms available in the room type the user chooses at the specified time
        available_rooms = []
        for room in room_list:
            if check_room_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        
        # book the first available room for the user
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
            return redirect('hotel:BookedRoomsView')
        # return an error message if there is no available room in the chosen room type at that period
        else:
            messages.error(request, f'All {room_type} rooms have been booked at this period. Please try another one or book at a different time.')
            return redirect('hotel:RoomListView')


# views for rooms booked by a user
class BookedRoomsView(ListView):
    model = Booking
    template_name = 'hotel/booked_rooms.html'

    def get_queryset(self):
        # return all the booked rooms if the current user is an admin, otherwise, return only the room booked by the current user
        if self.request.user.is_staff:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=self.request.user)
        
    # override the default context for class-based views to return booked rooms
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booked_rooms = self.get_queryset()
        room_prices = []
        room_images = []
        room_descriptions = []
        booking_status=[]
        current_date = datetime.now(timezone.utc)
        
        for booked_room in booked_rooms:
            room_properties = booked_room.room.properties.first()
            if room_properties:
                room_prices.append(room_properties.price_per_night)
                room_image = RoomImage.objects.filter(room_type=room_properties.room_type).first()
                if room_image:
                    room_images.append(room_image.image.url)
                else:
                    room_images.append(None)

                # get the room description of each room type
                room_descriptions.append(room_properties.room_type.description)

                # check if user is trying to checking out at a previous date 
                booking_status.append(booked_room.check_out >= current_date)
            else:
                room_prices.append(None)
                room_images.append(None)
                room_descriptions.append(None)
                booking_status.append(False)

        # return the booked rooms and their properties
        context['booked_rooms'] = zip(booked_rooms, room_prices, room_images, room_descriptions, booking_status)
        return context

# View for users to cancel their hotel bookings
class CancelBookingView(DeleteView):
    model = Booking
    success_url = reverse_lazy('hotel:BookedRoomsView')


# custom 404 error page view
def custom_404(request, exception):
    return render(request, '404.html', status=404)
