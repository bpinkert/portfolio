from django.contrib import admin
from image_cropping import ImageCroppingMixin
# Register your models here.
from .models import Item, Service, ItemSale, SubscriptionSale

class itemAdmin(ImageCroppingMixin, admin.ModelAdmin):
	list_display = ['title', 'value', 'sku', 'description', 'image1']
	
	class Meta: 
		model = Item

class serviceAdmin(ImageCroppingMixin, admin.ModelAdmin):
	list_display = ['title', 'value', 'sku', 'description', 'image']
	
	class Meta: 
		model = Service

# class saleAdmin(admin.ModelAdmin):
# 	list_display = ['item', 'purchase_time', 'purchase_price']
	
# 	class Meta: 
# 		model = ItemSale

# class subscriptionAdmin(admin.ModelAdmin):
# 	list_display = ['service', 'purchase_time', 'purchase_price']
	
# 	class Meta: 
# 		model = SubscriptionSale


# admin.site.register(SubscriptionSale, subscriptionAdmin)
# admin.site.register(ItemSale, saleAdmin)
admin.site.register(Item, itemAdmin)
admin.site.register(Service, serviceAdmin)