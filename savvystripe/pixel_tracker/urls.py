from django.conf.urls import  url
from .views import tracking_pixel


urlpatterns = [
    url(r'^(?P<tracking_pixel>.*?).png', tracking_pixel, name="tracking_pixel"),
]
