from django.contrib import admin

from .models import stripeEvent, Article, ArticleTag
# Register your models here.


class articleAdmin(admin.ModelAdmin):
	list_display = ['title', 'text', 'image', ]
	
	class Meta: 
		model = Article

admin.site.register(Article, articleAdmin)

class tagAdmin(admin.ModelAdmin):
	list_display = ['tag']
	
	class Meta: 
		model = ArticleTag

admin.site.register(ArticleTag, tagAdmin)


class eventAdmin(admin.ModelAdmin):
	list_display = ['created','evttype']
	
	class Meta: 
		model = stripeEvent

admin.site.register(stripeEvent, eventAdmin)


# class chargeAdmin(admin.ModelAdmin):
# 	# list_display = ['tag']
	
# 	class Meta: 
# 		model = chargeHistory

# admin.site.register(chargeHistory, chargeAdmin)
