from __future__ import unicode_literals

from django.db import models
from profiles.models import profile
from django.conf import settings
from django.core.mail import send_mail
# Create your models here.
class Ticket(models.Model):

    

	user = models.ForeignKey(profile, null=True, blank=True, unique=False)	
	description = models.TextField(null=False, blank=True, default='ticket text')
	time = models.DateTimeField(auto_now=True)
	PROGRESS = (
        ('N', 'New'),
        ('I', 'In Progress'),
        ('R', 'Resolved'),
    )
	progress = models.CharField(max_length=1, choices=PROGRESS, default='New')
    	TICKTYPE = (
    	('C', 'Customer Support'),
        ('B', 'Billing'),
    	('S', 'Sales'),
    )
	ticktype = models.CharField(max_length=1, choices=TICKTYPE, default='Customer Support')

        def save(self, *args, **kwargs):
            subject = 'Ticket submitted at payments.savantdigital.net'
            message = 'Description: %s\n Ticket Type: %s\n User: %s' % (self.description, self.ticktype, self.user)
            emailFrom = self.user
            # emailTo = [settings.EMAIL_HOST_USER]
            emailTo = ['admin@savantdigital.net']
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True,)
            title = 'Thanks!'
            super(Ticket, self).save(*args, **kwargs)