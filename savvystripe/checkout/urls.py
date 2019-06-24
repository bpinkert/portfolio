from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import views as checkout_views
from .models import Item, Service


urlpatterns=[
    url(r'^add-to-cart/$', checkout_views.add_to_cart, name='add-to-cart' ),
    url(r'^add-subscription/$', checkout_views.add_subscription, name='add-subscription'),
    url(r'^before-checkout/$', checkout_views.before_checkout, name='before-checkout'),
    url(r'^cart/$', checkout_views.get_cart, name='cart'),
    url(r'^cart-subscribe/$', checkout_views.cart_subscribe, name='cart-subscribe'),
    url(r'^cart-total/$', checkout_views.get_cart_total, name='cart-total'),
    url(r'^checkout/$', checkout_views.checkout, name='checkout'),
    url(r'^checkout-thanks/$', checkout_views.checkoutThanks, name='checkoutThanks'),
    url(r'^remove-from-cart/$', checkout_views.remove_from_cart, name='remove-from-cart'),
    url(r'^remove-subscription/$', checkout_views.remove_subscription, name='remove-subscription'),
    url(r'^unsubscribe/$', checkout_views.unsubscribe, name='ubsubscribe'),
    url(r'^subscribe/$', checkout_views.subscribe, name='subscribe'),
    url(r'^subscribe-card/$', checkout_views.subscribe_savecard, name='subscribe-card'),
]