from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required
def dashboard(request):
	template = 'dashboard.html'
	return render(request, template)

@login_required
def admin_dashboard(request):
	template = 'admin-dashboard.html'
	return render(request, template)