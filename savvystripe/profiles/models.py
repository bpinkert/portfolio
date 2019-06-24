from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class profile(models.Model):
	

	'''
	Profile object to integrate django user with stripe customer
	'''
	# def __init__(self):
	# 	self.name = ''
	# 	self.email = ''

	name = models.CharField(max_length=120)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
	description = models.TextField(default='description default text')
	email = models.CharField(max_length=50, null=True, blank=True)
	# stripe_id = models.ForeignKey(stripeCustomer, null=True, blank=True)

	def __str__(self):
		return self.user.email

	def __unicode__(self):
		return str(self.user.email)

class userStripe(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=200, null=True, blank=True)

	def delete(self, *args, **kwargs):
        	cu = stripe.Customer.retrieve(self.stripe_id)
        	cu.delete()
        	super(userStripe, self).delete(*args, **kwargs)    

	def __unicode__(self):
		if self.stripe_id:
			return str(self.stripe_id)
		else: 
			return self.user.username

	def __str__(self):
		if self.stripe_id:
			return str(self.stripe_id)
		else: 
			return self.user.username

    	# def save(self, *args, **kwargs):
     #    	s = stripeCustomer.objects.create(user=self.user, sid=self.stripe_id)
     #    	super(userStripe, self).save(*args, **kwargs)

def stripeCallback(sender, request, user, **kwargs):
	user_stripe_account, created = userStripe.objects.get_or_create(user=user)
	if created:
		print 'created for %s' % user.username
	if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
		desc = "Portal User: %s" % user.username
		new_stripe_id = stripe.Customer.create(description=desc,email=user.email)
		user_stripe_account.stripe_id = new_stripe_id['id']
		user_stripe_account.save()

def profileCallback(sender, request, user, **kwargs):
	userProfile, is_created = profile.objects.get_or_create(user=user)
	if is_created:
		userProfile.name = user.username
		userProfile.email = user.email
		userProfile.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(profileCallback)
user_signed_up.connect(stripeCallback)