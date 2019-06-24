"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from profiles import views as profile_views
from contact import views as contact_views
from checkout import views as checkout_views
from customers import views as customer_views
from checkout.models import Item, Service
from customers.models import stripeEvent
# import notifications.urls

urlpatterns = [
    url(r'^$', profile_views.home, name='home'),
    url(r'^accounts/', include('allauth.urls'), name='accounts'),
    # url(r'^carton/', include('carton.urls')),
    url(r'^about/$', profile_views.about, name='about'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^billing/$', customer_views.billing_view, name='billing'),
    url(r'^capture/$', checkout_views.capture, name='capture'),
    url(r'^add-to-cart/$', checkout_views.add_to_cart, name='add-to-cart' ),
    url(r'^add-subscription/$', checkout_views.add_subscription, name='add-subscription'),
    url(r'^remove-subscription/$', checkout_views.remove_subscription, name='remove-subscription'),
    # url(r'^cart-subscribe/$', checkout_views.cart_subscribe, name='cart-subscribe'),
    url(r'^unsubscribe/$', checkout_views.unsubscribe, name='ubsubscribe'),
    url(r'^subscribe/$', checkout_views.subscribe, name='subscribe'),
    url(r'^subscribe-card/$', checkout_views.subscribe_savecard, name='subscribe-card'),
    url(r'^remove-from-cart/$', checkout_views.remove_from_cart, name='remove-from-cart'),
    url(r'^before-checkout/$', checkout_views.before_checkout, name='before-checkout'),
    url(r'^cart/$', checkout_views.get_cart, name='cart'),
    url(r'^cart-total/$', checkout_views.get_cart_total, name='cart-total'),
    url(r'^checkout/$', checkout_views.checkout, name='checkout'),
    url(r'^hook/$', customer_views.event_hook, name='hook'),
    url(r'^checkout-thanks/$', checkout_views.checkoutThanks, name='checkoutThanks'),
    url(r'^contact/$', contact_views.contact, name='contact'),
    url(r'^contact/i', contact_views.contact, name='contact_track'),
    url(r'^dashboard/', include('dashboard.urls'), name='dashboard'),
    url(r'^domains/$', contact_views.searchDomains, name='domains'),
    url(r'^domain-results/$', contact_views.resultDomains, name='domain-results'),
    # url(r'^admin_dashboard/$', customer_views.admin_dashboard, name='admin_dashboard'),
    url(r'^events/$', customer_views.EventList, name='events'),
    url(r'^email_history/$', customer_views.email_history_view, name='email_history'),
    url(r'^inbox/notifications/', include("notifications.urls", namespace='notifications')) ,
    url(r'^articles/$', customer_views.KBListView.as_view(), name='articles'),
    url(r'^articles/(?P<pk>\d+)/$', customer_views.KBDetailView.as_view(), name='article'),
    url(r'^invoices/$', customer_views.my_invoices, name='invoices'),
    # url(r'^pixel/', include('pixel_tracker.urls'), name='pixels'),
    #url(r'^tracker/', include('django_pixels.urls', namespace="pixels")),
    url(r'^profile/$', profile_views.userProfile, name='profile'),
    # url(r'^sales/', include("sales.urls", namespace='sales')) ,
    url(r'^services/$', checkout_views.ServiceListView.as_view(), name='services'),
    url(r'^services/(?P<pk>\d+)/$', checkout_views.ServiceDetailView.as_view(), name='service'),
    # ex: /items/5/
    url(r'^my_services/$', customer_views.my_services, name='my_services'),
    url(r'^products/$', checkout_views.ItemListView.as_view(), name='items'),

    url(r'^products/(?P<pk>\d+)/$', checkout_views.ItemDetailView.as_view(), name='item'),
    # ex: /items/5/purchased/
    url(r'^tickets/', include("tickets.urls"), name='tickets') ,
    
]
    

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
