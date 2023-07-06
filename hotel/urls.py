from django.urls import path
from .views import RoomListView, RoomDetailView, BookingListView, CancelBookingView


app_name = 'hotel'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name = 'RoomListView'),
    path('rooms/<str:room_type>/', RoomDetailView.as_view(), name = 'RoomDetailView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('booking/cancel/<int:pk>/', CancelBookingView.as_view(), name='CancelBookingView'),
]