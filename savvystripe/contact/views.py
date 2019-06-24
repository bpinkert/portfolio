from django.shortcuts import render, render_to_response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from profiles.models import userStripe
import json
from django.http import HttpResponse, request
from django import forms 
from .models import whois
from .forms import WhoisForm
import subprocess
#from django_pixels import utils, handlers
from django.core.urlresolvers import reverse
from snowplow_tracker import Subject, Tracker, Emitter

stripe.api_key = settings.STRIPE_SECRET_KEY
from .forms import contactForm

# Create your views here.
#@login_required
def contact(request):
	title = 'Contact'
	form = contactForm(request.POST or None)
	confirm_message = None
	e = Emitter("192.168.2.133:8090/contact")
        tracker = Tracker(e , namespace="sdp", app_id="sdp-11", encode_base64=False)
	

	if form.is_valid():
		name = form.cleaned_data['name']
		comment = form.cleaned_data['comment']
		subject = 'Message from Mysite.com'
		message = '%s %s' % (comment, name)
		emailFrom = form.cleaned_data['email']
		# emailTo = [settings.EMAIL_HOST_USER]
		emailTo = ['admin@savantdigital.net']
		send_mail(subject, message, emailFrom, emailTo, fail_silently=True,)
		title = 'Thanks!'
		confirm_message = 'Thanks for the message, we will get right back to you.'
		form = None
		tracker.track_page_view("192.168.2.133:8090/contact")

	context = {'title': title,'form': form, 'confirm_message': confirm_message, }	
	template = 'contact.html'
	return render(request, template, context)

@login_required
def searchDomains(request):
	title = 'Search Domains'
	form = WhoisForm(request.POST or None)
	confirm_message = None

	if form.is_valid():
		domain = form.cleaned_data['domainname']
		answer = whois(domain)
		a = str(answer[0])
		b = a.decode('utf-8').split('\n')
		registrar = b[8]
		domname = b[7]
		ns1 = b[12]
		ns2 = b[13]
		ns3 = b[14]
		status = b[16]
		updated = b[17]
		created = b[18]
		expiration = b[19]
		# registrant info
		reg_name = b[70]
		reg_org = b[71]
		reg_st = b[72]
		reg_st2 = b[73]
		reg_city = b[74]
		reg_state = b[75]
		reg_zip = b[76]
		reg_country = b[77]
		reg_phone = b[78]
		reg_email = b[82]
		# admin info
		adm_name = b[84]
		adm_org = b[85]
		adm_st = b[86]
		adm_st2 = b[87]
		adm_city = b[88]
		adm_state = b[89]
		adm_zip = b[90]
		adm_country = b[91]
		adm_phone = b[92]
		adm_email = b[96]
		# tech info
		tech_name = b[98]
		tech_org = b[99]
		tech_st = b[100]
		tech_st2 = b[101]
		tech_city = b[102]
		tech_state = b[103]
		tech_zip = b[104]
		tech_country = b[105]
		tech_phone = b[106]
		tech_email = b[110]
		d = dict([
			("registrar", registrar),
			("domname", domname), 
			("ns1", ns1),  
			("ns2", ns2),
			("ns3", ns3), 
			("status", status),
			("updated", updated),
			("created", created),
			("expiration", expiration),
			("reg_name", reg_name),
			("reg_org", reg_org ),
			("reg_st", reg_st) ,
			("reg_st2", reg_st2), 
			("reg_city", reg_city), 
			("reg_state", reg_state), 
			("reg_zip", reg_zip), 
			("reg_country", reg_country), 
			("reg_phone", reg_phone), 
			("reg_email", reg_email), 
			("adm_name", adm_name),
			("adm_org", adm_org), 
			("adm_st", adm_st), 
			("adm_st2", adm_st2), 
			("adm_city", adm_city),  
			("adm_state", adm_state),  
			("adm_zip", adm_zip), 
			("adm_country", adm_country), 
			("adm_phone", adm_phone), 
			("adm_email", adm_email), 
			("tech_name", tech_name), 
			("tech_org", tech_org),
			("tech_st", tech_st), 
			("tech_st2", tech_st2), 
			("tech_city", tech_city), 
			("tech_state", tech_state), 
			("tech_zip", tech_zip), 
			("tech_country", tech_country), 
			("tech_phone", tech_phone),
			("tech_email", tech_email),
		   ])
		

	context = {'title': title, 'form':form, 'confirm_message': confirm_message}
	template = 'search-domains.html'
	return render(request, template, context)


@login_required
def resultDomains(request):
	title = 'Domain Results'
	form = WhoisForm(request.POST or None)
	confirm_message = None

	if form.is_valid():
		domain = form.cleaned_data['domainname']
		answer = whois(domain)
		a = str(answer[0])
		b = a.decode('utf-8').split('\n')
		registrar = b[8]
		domname = b[7]
		ns1 = b[12]
		ns2 = b[13]
		ns3 = b[14]
		status = b[16]
		updated = b[17]
		created = b[18]
		expiration = b[19]
		# registrant info
		reg_name = b[70]
		reg_org = b[71]
		reg_st = b[72]
		reg_st2 = b[73]
		reg_city = b[74]
		reg_state = b[75]
		reg_zip = b[76]
		reg_country = b[77]
		reg_phone = b[78]
		reg_email = b[82]
		# admin info
		adm_name = b[84]
		adm_org = b[85]
		adm_st = b[86]
		adm_st2 = b[87]
		adm_city = b[88]
		adm_state = b[89]
		adm_zip = b[90]
		adm_country = b[91]
		adm_phone = b[92]
		adm_email = b[96]
		# tech info
		tech_name = b[98]
		tech_org = b[99]
		tech_st = b[100]
		tech_st2 = b[101]
		tech_city = b[102]
		tech_state = b[103]
		tech_zip = b[104]
		tech_country = b[105]
		tech_phone = b[106]
		tech_email = b[110]
		d = dict([
			("registrar", registrar),
			("domname", domname), 
			("ns1", ns1),  
			("ns2", ns2),
			("ns3", ns3), 
			("status", status),
			("updated", updated),
			("created", created),
			("expiration", expiration),
			("reg_name", reg_name),
			("reg_org", reg_org ),
			("reg_st", reg_st) ,
			("reg_st2", reg_st2), 
			("reg_city", reg_city), 
			("reg_state", reg_state), 
			("reg_zip", reg_zip), 
			("reg_country", reg_country), 
			("reg_phone", reg_phone), 
			("reg_email", reg_email), 
			("adm_name", adm_name),
			("adm_org", adm_org), 
			("adm_st", adm_st), 
			("adm_st2", adm_st2), 
			("adm_city", adm_city),  
			("adm_state", adm_state),  
			("adm_zip", adm_zip), 
			("adm_country", adm_country), 
			("adm_phone", adm_phone), 
			("adm_email", adm_email), 
			("tech_name", tech_name), 
			("tech_org", tech_org),
			("tech_st", tech_st), 
			("tech_st2", tech_st2), 
			("tech_city", tech_city), 
			("tech_state", tech_state), 
			("tech_zip", tech_zip), 
			("tech_country", tech_country), 
			("tech_phone", tech_phone),
			("tech_email", tech_email),
		   ])
		

	context = {'title': title, 'form':form, 'confirm_message': confirm_message, 'answer': d}
	template = 'domains.html'
	return render(request, template, context)


#def track_emails(request):
#	tracking_url = reverse('pixels:pixel')
#	pixel_ = utils.compose_pixel_url(tracking_url, 1)
#	handlers.register(1, track_emails)
#	response = HttpResponse(pixel_, content_type='image/gif')
#	return render(request, response)
def tracker(request):
	tracker = Tracker( Emitter("payments.savantdigital.net") , namespace="sdp", app_id="sdp-11", encode_base64=False)
	return render(request, response, context)
