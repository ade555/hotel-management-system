from django.urls import path
from .views import RoomListView, RoomDetailView, BookingListView

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name = 'RoomListView'),
    path('rooms/<str:room_type>/', RoomDetailView.as_view(), name = 'RoomDetailView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
]