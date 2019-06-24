from django.contrib import admin
from .models import Ticket

# Register your models here.
class ticketAdmin(admin.ModelAdmin):
	list_display = ['user', 'description', 'time', 'progress', 'ticktype']
	
	class Meta: 
		model = Ticket

admin.site.register(Ticket, ticketAdmin)
