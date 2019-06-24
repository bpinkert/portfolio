from django import forms
from django.db import models
from .models import Item, Service


class CheckoutForm(forms.Form):
    product_name = forms.CharField()
    quantity = forms.IntegerField()
    item_id = forms.IntegerField()
    item_value = forms.IntegerField()