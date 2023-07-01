from django.urls import path
from .views import ProfileView, UpdateProfileView

urlpatterns = [
    path('', ProfileView.as_view(), name='ProfileView'),
    path('update/', UpdateProfileView.as_view(), name='UpdateProfileView'),
]
