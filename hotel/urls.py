from django.urls import path
from .views import RoomListView, RoomDetailView

urlpatterns = [
    path('', RoomListView.as_view(), name = 'RoomListView'),
    path('book/<room_type>', RoomDetailView.as_view(), name = 'RoomDetailView'),
]