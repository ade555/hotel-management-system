from django.urls import path, include
from .views import HomePage, ContactView
app_name = 'content_app'
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact')
]
