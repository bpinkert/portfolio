from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import sessions
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, request
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from cart.models import ItemManager
import uuid
import stripe
from .models import Item, Service, ItemSale, SubscriptionSale
from customers.views import my_services, billing_view
from .forms import CheckoutForm
from bs4 import BeautifulSoup
from stdimage import StdImageField
import urllib

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.


class ItemListView(generic.ListView):
    model = Item

    def get_queryset(self):
        return Item.objects.all()


class ItemDetailView(generic.DetailView):
    model = Item

    # request['item_id'] = str(Item.pk)


class ServiceListView(generic.ListView):
    model = Service

    def get_queryset(self):
        return Service.objects.all()


class ServiceDetailView(generic.DetailView):
    model = Service


@login_required
def add_to_cart(request):
    cart_items = 0
    request.session['cart_items'] = 0
    if request.method == 'POST':
        quantity = request.POST['quantity']
        item_id = request.POST['item_id']
        item_value = request.POST['item_value']
        request.session['cart_items'] += 1
        request.session['carttype'] = 'item'
        item = Item.objects.get(id=item_id)
        cart = Cart(request)
        cart.add(item, item_value, quantity)

    return redirect(get_cart)


@csrf_exempt
@login_required
def remove_from_cart(request):
    # item_id = request.POST['item_id']
    try:
        item_id = request.GET['item_id']
        item = Item.objects.get(id=item_id)
        cart = Cart(request)
        cart.remove(item)
        return redirect(get_cart)
    except Exception as e:
        return HttpResponse(e)


@login_required
def get_cart(request):
    try:
        # request.session['total'] = ''
        return render(request, 'cart.html', dict(cart=Cart(request)))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def get_cart_total(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('fail')

    try:
        total = request.POST['total']
        request.session['total'] = total
        if request.session['total'] != total:
            return Http404()
    except Exception as e:
        return HttpResponse(e)


@login_required
def before_checkout(request):
    if request.method == 'POST':
        total = request.POST['total']
        request.session['total'] = total

    return redirect(checkout)


def checkout(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    # total = request.session['total']
    if request.method == 'POST':
        token = request.POST['stripeToken']
        total = request.session['total']
        try:
            customer = stripe.Customer.retrieve(customer_id)
            customer.sources.create(source=token)
            # idempotency prevents multiple charges when submitted more than once
            i = str(uuid.uuid4().time_low)
            d = "Item Purchased by %s" % request.user.profile.email
            charge = stripe.Charge.create(
                amount=total,
                currency="usd",
                description=d,
                customer=customer,
                idempotency_key=i,
                metadata=None,
            )

            cart = Cart(request)
            cart.clear()
            # return HttpResponse('Thanks for checking out!')
            return redirect(billing_view)
        except stripe.error.CardError as e:
            # Card was declined
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
            # param is '' in this case
            print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']

    # item_id = request.GET['item_id']
    # item = Item.objects.get(id=item_id)
    context = {'publishKey': publishKey}
    template = 'checkout.html'
    return render(request, template, context)


@login_required
def add_subscription(request):
    customer_id = request.user.userstripe.stripe_id
    request.session['cart_items'] = 0
    if request.method == 'POST':
        planid = request.POST['planid']
        value = request.POST['plan_value']
        request.session['cart_items'] += 1
        request.session['planid'] = planid
        request.session['carttype'] = 'subscription'
        request.session['total'] = value
        plan = Service.objects.get(sku=planid)
        cart = Cart(request)
        cart.add(plan, value, 1)

    return redirect(get_cart)


@login_required
def remove_subscription(request):
    try:
        plan_id = request.GET['planid']
        plan = Service.objects.get(sku=plan_id)
        cart = Cart(request)
        cart.remove(plan)
        return redirect(get_cart)
    except Exception as e:
        return HttpResponse(e)


@login_required
def subscribe(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    planid = request.session['planid']
    if request.method == 'POST':
        # token = request.POST['stripeToken']
        # total = request.session['total']
        try:
            c = stripe.Customer.retrieve(customer_id)
            # if customer has no sources, redirect to add new card info
            if len(c['sources']['data']) == 0:
                return redirect(subscribe_savecard)
            else:
                # create new plan
                plan = stripe.Plan.retrieve(planid)
                # create description
                # d = "Plan Purchased by %s" % request.user.profile.email
                stripe.Subscription.create(
                    customer=c,
                    plan=plan,
                )
                # clear cart after customer is subscribed
                cart = Cart(request)
                cart.clear()
                # reset carttype
                request.session['carttype'] = None
                # return HttpResponse('Thanks for subscribing!')
                return redirect(my_services)
        except stripe.error.CardError as e:
            # Card was declined
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
            # param is '' in this case
            print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']

    context = {'publishKey': publishKey}
    template = 'checkout.html'
    return render(request, template, context)


@login_required
def unsubscribe(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    if request.method == 'POST':
        # token = request.POST['stripeToken']
        # total = request.session['total']
        try:
            planid = request.POST['planid']
            customer = stripe.Customer.retrieve(customer_id)
            plan = stripe.Plan.retrieve(planid)
            l = stripe.Subscription.list(customer=customer_id)
            planid = l['data'][0]['id']
            sub = stripe.Subscription.retrieve(
                id=planid
            )
            sub.delete()
            # return HttpResponse('You have been unsubscribed')
            return redirect(get_cart)
        except stripe.error.CardError as e:
            # Card was declined
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
            # param is '' in this case
            print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']

    context = {'publishKey': publishKey}
    template = 'checkout.html'
    return render(request, template, context)


@login_required
def subscribe_savecard(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    planid = request.session['planid']
    if request.method == 'POST':
        token = request.POST['stripeToken']
        # print request.POST
        try:
            customer = stripe.Customer.retrieve(customer_id)
            card = customer.sources.create(source=token)
            plan = stripe.Plan.retrieve(planid)
            stripe.Subscription.create(
                customer=customer,
                plan=plan
            )
            cart = Cart(request)
            # adding logic to record cart sales items to ItemSale model
            # want to update model before we clear it
            # for each item in cart:
            # c = cart.objects.all()
            cart.clear()
            return HttpResponse('Thanks for subscribing!')
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
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
def chargeView(request):
    customer_id = request.user.userstripe.stripe_id
    if request.method == 'GET':
        try:
            # serviceItem
            customer = stripe.Customer.retrieve(customer_id)
            charge = stripe.Charge.create(
                amount=1000,
                currency="usd",
                description="chargeView test",
                customer=customer,
                idempotency_key=None,
                metadata=None,
            )
            return redirect(checkoutThanks)
        except stripe.error.CardError as e:
            # Card was declined
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
            # param is '' in this case
            print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']
    context = {'value': value}
    template = 'chargeitems.html'
    return render(request, template, context)


@login_required
def capture(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    if request.method == 'POST':
        token = request.POST['stripeToken']
        # print request.POST
        try:
            customer = stripe.Customer.retrieve(customer_id)
            card = customer.sources.create(source=token)
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
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
def checkoutThanks(request):
    return HttpResponse("Placeholder, but thanks for using checkout!")
