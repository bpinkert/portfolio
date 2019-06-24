from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard, admin_dashboard
# import notifications.urls

urlpatterns = [
	url(r'^dashboard/', dashboard, name='dashboard'),
	url(r'^admin_dashboard/', admin_dashboard, name='admin_dashboard'),
]