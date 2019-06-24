from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import submit_ticket, my_tickets, TicketDetailView
# from .models import Item, Service


urlpatterns=[
    url(r'^my-tickets/', my_tickets, name='my-tickets' ),
    url(r'^ticket/(?P<pk>\d+)/$', TicketDetailView.as_view(), name='ticket'),
    url(r'^submit-ticket/', submit_ticket, name='submit-ticket' ),
    url(r'^comments/', include('django_comments.urls')),
]