from django.db.models.signals import post_save
from notifications.signals import notify
from customers.models import stripeCustomer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



# @csrf_exempt
# def webhook(request):
#   # Process webhook data in `request.body`
#   	event_json = json.loads(request.body)
#   	evt_id = event_json['id']

#   	ret = stripe.Event.retrieve(evt_id)

#   # Do something with event_json

# 	return HttpResponse(status=200)