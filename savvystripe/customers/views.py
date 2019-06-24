from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core import serializers
import stripe
from profiles.models import userStripe
from .models import stripeEvent, Article, ArticleTag
import json

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

@login_required
def savecard(request):
	publishKey = settings.STRIPE_PUBLISHABLE_KEY
	customer_id = request.user.userstripe.stripe_id
	if request.method == 'POST':
		token = request.POST['stripeToken']
		#print request.POST
		try:
			customer = stripe.Customer.retrieve(customer_id)
			card = customer.sources.create(source=token)
		except stripe.error.CardError as e:
		  	body = e.json_body
		  	err  = body['error']
		  	print "Status is: %s" % e.http_status
		  	print "Type is: %s" % err['type']
		  	print "Code is: %s" % err['code']
		  	# param is '' in this case
		  	print "Param is: %s" % err['param']
		  	print "Message is: %s" % err['message']
			# Card wasn't saved 
			print e
	context = {'publishKey': publishKey}
	template = 'capture.html'
	return render(request, template, context)

@login_required
def subscribeThanks(request):
	return HttpResponse("Placeholder, but thanks for subscribing to our service!")


@login_required
def dashboard(request):
	template = 'dashboard.html'
	return render(request, template)

@login_required
def admin_dashboard(request):
	template = 'admin-dashboard.html'
	return render(request, template)

@login_required
def client_area(request):
	template = 'clients.html'
	return render(request, template)

@login_required
def billing_view(request):
	user = request.user
	customer_id = request.user.userstripe.stripe_id
	c = stripe.Charge.list(customer=customer_id)
	d = json.loads(str(c))
	data_list = d['data']
	context = {'user':user, 'data_list': data_list}
	template = 'billing.html'
	return render(request, template, context)

@login_required
def email_history_view(request):
	template = 'email_history.html'
	return render(request, template)

def knowledgebase_view(request):
	template = 'knowledgebase.html'
	return render(request, template)

@login_required
def my_services(request):
	user = request.user
	customer_id = request.user.userstripe.stripe_id
	s = stripe.Subscription.list(customer=customer_id)
	t = json.loads(str(s))
	if s['data'] != None:
		data_list = s['data'] 
	
	context = {'user':user, 'data_list': data_list}
	template = 'subscriptions.html'
	return render(request, template, context)

@login_required
def my_invoices(request):
	user = request.user
	customer_id = request.user.userstripe.stripe_id
	s = stripe.Invoice.list(customer=customer_id)
	if s['data'] != None:
		data_list = s['data'] 
	
	context = {'user':user, 'data_list': data_list}
	template = 'invoices.html'
	return render(request, template, context)


class KBListView(generic.ListView):
	model = Article  
    
	def get_queryset(self):
        	return Article.objects.all()


class KBDetailView(generic.DetailView):
	model = Article


@login_required
class EventList(generic.ListView):
	model = stripeEvent 
	# customer_id = request.user.userstripe.stripe_id
	# e = stripe.Event.list()
	
	# for event in e.auto_paging_iter():		
	# 	hook_id = event['id']
	# 	created = event['created']
	# 	webhook_message = event['data']
	# 	livemode = event['livemode']
 #  		evt_type = event['type']
 #   		request = event['request']
 #   		pending_webhooks = event['pending_webhooks']
 #   		# api_version = event_json['api_version']
 #   		#print event_json.viewkeys()
	# 	#print webhook_message['object'].viewkeys()
	# 	# customer = webhook_message['object']['customer']
	# 	# email = webhook_message['object']['receipt_email']
	# 	s = stripeEvent.objects.create(evtid=hook_id, created=created,request=request, data=webhook_message,livemode=livemode,pending_webhooks=pending_webhooks, evttype=evt_type)
	def get_queryset(self):
       		return stripeEvent.objects.all()

# @login_required
class EventDetail(generic.DetailView):
	model = stripeEvent



@csrf_exempt
def event_hook(request):
  # Retrieve the request's body and parse it as JSON
  	try:
  		event_json = json.loads(request.body)
  		# Verify the evpent by fetching it from Stripe
   		webhook_message = event_json["data"]
  		print 'HookEvent:\n %s' % webhook_message
   		#obj_generator = serializers.json.Deserializer(request.POST) 		
   		#for stripeEvent in obj_generator:
   		#	stripeEvent.save()
   		#event = stripe.Event.retrieve(event_json["id"])
   		#Do something with event
   		hook_id = event_json['id']
   		# event = stripe.Event.retrieve(hook_id)
   		#s = stripeEvent
		#title = event_json['title']
		apiversion = event_json['api_version']
   		webhook_message = event_json['data']
		livemode = event_json['livemode']
  		evt_type = event_json['type']
   		request = event_json['request']
        # time = event_json['created']
   		pending_webhooks = event_json['pending_webhooks']
   		api_version = event_json['api_version']
   		#print event_json.viewkeys()
		#print webhook_message['object'].viewkeys()
		customer = webhook_message['object']['customer']
		email = webhook_message['object']['receipt_email']
		s = stripeEvent.objects.create(evtid=hook_id,request=request, data=webhook_message,livemode=livemode,pending_webhooks=pending_webhooks, evttype=evt_type)
  	except Exception as e:
  		print 'Exception: %s'% e

   	return HttpResponse(status=200)

