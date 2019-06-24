from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from profiles.models import profile, userStripe
from django.utils.encoding import python_2_unicode_compatible
import stripe
from allauth.account.models import EmailAddress
from jsonfield.fields import JSONField
import json
from django.http import HttpResponse
from PIL import Image
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeObject(models.Model):
    stripe_id = models.ForeignKey(userStripe)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
		abstract = True
# class stripeCustomer(models.Model):
# 	'''
# 	Customer object, used for server-side storage of pulled stripe information
# 	'''
# 	# name = models.OneToOneField(profile.user, null=False, blank=False)
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
# 	email = models.OneToOneField(EmailAddress, null=False, blank=False)
# 	sid = models.ForeignKey(userStripe, null=False, blank=True, default='Placeholder',on_delete=models.CASCADE)
# 	account_balance = models.DecimalField(decimal_places=2, max_digits=9, null=True)
# 	currency = models.CharField(max_length=10, default="usd", blank=True)
# 	delinquent = models.BooleanField(default=False)
# 	# created_at = models.DateTimeField(default=timezone.now)
# 	date_purged = models.DateTimeField(null=True, editable=False)

# 	def __str__(self):
# 		return str(self.email)


	# def delete(self):
 #            cu = stripe.Customer.retrieve(self.sid)
 #            cu.delete()


# class subscriptionPlan(StripeObject):
#     amount = models.DecimalField(decimal_places=2, max_digits=9)
#     currency = models.CharField(max_length=15)
#     interval = models.CharField(max_length=15)
#     interval_count = models.IntegerField()
#     name = models.CharField(max_length=150)
#     statement_descriptor = models.TextField(blank=True)
#     trial_period_days = models.IntegerField(null=True)
#     metadata = JSONField(null=True)

#     def __str__(self):
# 		return "{} ({}{})".format(self.name, CURRENCY_SYMBOLS.get(self.currency, ""), self.amount)


# # class eventHistory(StripeObject):
# class EventProcessingException(models.Model):

#     event = models.ForeignKey("stripeEvent", null=True)
#     data = models.TextField()
#     message = models.CharField(max_length=500)
#     traceback = models.TextField()
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
# 		return "<{}, pk={}, Event={}>".format(self.message, self.pk, self.event)


# @python_2_unicode_compatible
class stripeEvent(models.Model):
    evtid = models.CharField(max_length=100, default='evt id')
    apiverison = models.CharField(max_length=20, default='api ph')
    created = models.CharField(max_length=10, default='created')
    title = models.CharField(max_length=100, default='default title')
    data = JSONField(null=True)
    livemode = models.BooleanField(default=False)
    #customer = models.ForeignKey("stripeCustomer", null=False, blank=True, default='customer')
    receiptemail = models.CharField(max_length=25, default='receipt email')
    #language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    #style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    pending_webhooks = models.IntegerField(null=True)
    request = models.CharField(max_length=15, default='default', null=True)
    evttype = models.CharField(max_length=15, default='default', null=True)

    class Meta:
	   ordering = ('evtid',)

class ArticleTag(models.Model):
    tag = models.CharField(max_length=100)
    def __str__(self):
        return self.tag
    class Meta:
        ordering = ['tag']
        verbose_name = "tag"
        verbose_name_plural = "tags"

class Article(models.Model):
    title = models.CharField(max_length=25, null=False)
    tags = models.ManyToManyField(ArticleTag)
    text = models.TextField()
    image = models.ImageField(
        upload_to='article_pictures/', 
        blank=True, 
        editable=True, 
        null=True, 
        help_text="Article Picture", 
        verbose_name="Article Pictures"
        )

    def __str__(self):
        return self.title
