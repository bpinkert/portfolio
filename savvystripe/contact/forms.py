from django import forms
from django.http import HttpResponse, request 
from django.shortcuts import render, render_to_response
from .models import whois 
import subprocess

class contactForm(forms.Form):
	name = forms.CharField(required=True, max_length=100, help_text="100 characters max")
	email = forms.EmailField(required=True)
	comment = forms.CharField(required=True, widget=forms.Textarea)

# class domainForm(forms.Form):
# 	placeholder
class WhoisForm(forms.Form):     
	domainname = forms.CharField(max_length=100)      

