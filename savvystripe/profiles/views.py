from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import sessions
import json
from django.template import Context
from .models import userStripe
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def home(request):
	# cartitems = request.session['cart_items']
	context = {}
	template = 'home.html'
	return render(request, template, context)

def about(request):
	context = {}
	template = 'about.html'
	return render(request, template, context)

@login_required
def userProfile(request):
	# cartitems = request.session['cart_items']
	user = request.user
	customer_id = request.user.userstripe.stripe_id
	c = stripe.Charge.list(customer=customer_id)
	d = json.loads(str(c))
	data_list = d['data']
	context = {'user':user, 'data_list': data_list}
	template = 'profile.html'
	return render(request, template, context)