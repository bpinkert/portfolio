from django.contrib import admin

# Register your models here.
from .models import profile, userStripe

class profileAdmin(admin.ModelAdmin):
	list_display = ['name','user','description', 'email']
	
	class Meta: 
		model = profile

admin.site.register(profile, profileAdmin)

class userStripeAdmin(admin.ModelAdmin):
	list_display = ['user', 'stripe_id']
	class Meta:
		model = userStripe

admin.site.register(userStripe, userStripeAdmin)