from django.urls import path
from .views import RoomListView, RoomDetailView, BookedRoomsView, CancelBookingView


app_name = 'hotel'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name = 'RoomListView'),
    path('rooms/<str:room_type>/', RoomDetailView.as_view(), name = 'RoomDetailView'),
    path('booked_rooms', BookedRoomsView.as_view(), name='BookedRoomsView'),
    path('booking/cancel/<int:pk>/', CancelBookingView.as_view(), name='CancelBookingView'),
]