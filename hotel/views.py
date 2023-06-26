from django.shortcuts import render
from django.views.generic import ListView
from .models import Room, RoomImage

class RoomListView(ListView):
    model = Room
    context_object_name = 'rooms'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_images = RoomImage.objects.all()
        context['room_images'] = room_images
        return context





# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)
