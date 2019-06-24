from django import forms
from django.conf import settings
import stripe


class cardForm(forms.Form):
	number = forms.CharField(required=True, max_length=20, help_text="20 characters max")
	exp_month =
	exp_year =
	cvc =
	email = forms.EmailField(required=True)
	