from django.urls import path, include
from .views import HomePage, ContactView, AboutPage, TouristPage
app_name = 'content_app'
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutPage.as_view(), name='about'),
    path('tourist-spots/', TouristPage.as_view(), name='tourist-spots'),
]
