from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request
from django.conf import settings
from django.core.mail import send_mail
from .forms import TicketForm
from .models import Ticket
from profiles.models import profile
from django.views import generic

# from profiles.models import profile
# Create your views here.

# @login_required
# def submit_ticket(request):
#         ticket = TicketForm() # Look at the (), they are needed for instantiation
#         return render_to_response('tickets.html', {'TicketForm': ticket})

@login_required 
def submit_ticket(request):
	title = 'Submit Ticket'
	form = TicketForm(request.POST or None)
	confirm_message = None
	user = request.user.profile

	if form.is_valid():
		description = form.cleaned_data['description']
		ticktype = form.cleaned_data['ticktype']
		confirm_message = 'Thanks for submitting a ticket, we will get right back to you.'
		form = None
		t = Ticket.objects.create(description=description, user=user, ticktype=ticktype)
		subject = 'Ticket submitted at payments.savantdigital.net'
		message = 'Description: %s\n Ticket Type: %s\n User: %s' % (description, ticktype, user)
		emailFrom = user
		# emailTo = [settings.EMAIL_HOST_USER]
		emailTo = ['admin@savantdigital.net']
		send_mail(subject, message, emailFrom, emailTo, fail_silently=True,)
		title = 'Thanks!'

	context = {'user': user, 'title': title,'form': form, 'confirm_message': confirm_message, }	
	template = 'tickets.html'
	return render(request, template, context)

@login_required
def my_tickets(request):
	user = request.user.profile
	tickets = Ticket.objects.filter(user=user)
	
	context = {'user':user, 'tickets': tickets}
	template = 'my_tickets.html'
	return render(request, template, context)

@login_required
class TicketListView(generic.ListView):
	model = Ticket  

	def get_queryset(self):
		user = request.user.profile
		return Ticket.objects.filter(user=user)
    
	# def get_queryset(self):
 #        	return Service.objects.all()


class TicketDetailView(generic.DetailView):
	model = Ticket