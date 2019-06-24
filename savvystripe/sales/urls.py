from django.conf.urls import *
from sales import views

urlpatterns = [
    url(r'^charge/$', views.charge, name="charge"),
]