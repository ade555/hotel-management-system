from django.urls import path
from .views import ProfileView, UpdateProfileView
app_name = 'users'
urlpatterns = [
    path('', ProfileView.as_view(), name='ProfileView'),
    path('update/', UpdateProfileView.as_view(), name='UpdateProfileView'),
]
