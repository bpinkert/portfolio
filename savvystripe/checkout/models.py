from __future__ import unicode_literals
from django.db import models
from profiles.models import userStripe
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.forms import forms
from stdimage import StdImageField
from cart.models import ItemManager
from cart.cart import Cart
from PIL import Image
from image_cropping import ImageRatioField
import StringIO
from random import randrange
from customers.models import StripeObject
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your models here.

class PhotoField(forms.FileField, object):

    def __init__(self, *args, **kwargs):
        super(PhotoField, self).__init__(*args, **kwargs)
        self.help_text = "Images over 500kb will be resized to keep under 500kb limit, which may result in some loss of quality"

    def validate(self,image):
        if not str(image).split('.')[-1].lower() in ["jpg","jpeg","png","gif"]:
            raise ValidationError("File format not supported, please try again and upload a JPG/PNG/GIF file")

    def to_python(self, image):
        try:
            limit = 500000
            num_of_tries = 10
            img = Image.open(image.file)
            width, height = img.size
            ratio = float(width) / float(height)

            upload_dir = settings.FILE_UPLOAD_TEMP_DIR if settings.FILE_UPLOAD_TEMP_DIR else '/tmp'
            tmp_file = open(os.path.join(upload_dir, str(uuid.uuid1())), "w")
            tmp_file.write(image.file.read())
            tmp_file.close()

            while os.path.getsize(tmp_file.name) > limit:
                num_of_tries -= 1
                width = 900 if num_of_tries == 0 else width - 100
                height = int(width / ratio)
                img.thumbnail((width, height), Image.ANTIALIAS)
                img.save(tmp_file.name, img.format)
                image.file = open(tmp_file.name)
                if num_of_tries == 0:
                    break                    
        except:
            pass
        return image


class Item(models.Model):
    # image = models.ImageField(
    #     upload_to='product_pictures/', 
    #     blank=True, 
    #     editable=True, 
    #     null=True, 
    #     help_text="Product Picture", 
    #     verbose_name="Product Picture"
    #     )
    image1 = StdImageField(upload_to='product_pictures/', help_text= "Product Picture", verbose_name="Product Pictures", null=True, blank=True, variations={'big-thumbnail': (250, 250, True), 'small-thumbnail': (150, 150, True)})
    # image2 = StdImageField(upload_to='path/to/img', blank=True, null=True) # can be deleted throwgh admin
    # image3 = StdImageField(upload_to='path/to/img', null=True, variations={'thumbnail': (100, 75)}) # creates a thumbnail resized to maximum size to fit a 100x75 area
    # image4 = StdImageField(upload_to='path/to/img', null=True ,variations={'thumbnail': (100, 100, True)}) # creates a thumbnail resized to 100x100 croping if necessary

    # image_all = StdImageField(upload_to='path/to/img', blank=True, variations={'large': (640, 480), 'thumbnail': (100, 100, True)}) # all previous features in one declaration
    # cropping = ImageRatioField('image', '150x150')
    title = models.CharField(max_length=20, null=False)
    value = models.DecimalField(decimal_places=0, max_digits=9, null=False)
    # quantity = models.DecimalField(decimal_places=0, max_digits=7, null=False)
    sku = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=25, null=False)
    # tax_rate = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    # upload image and change height / width
    # image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    # image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    # object_id = models.PositiveIntegerField()
    # purchase_time = models.DateTimeField(auto_now=True, null=True)
    # purchased_by = models.ForeignKey(stripeCustomer, null=False)

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.id)  

    objects = ItemManager()
    # product
    # def get_product(self):
        # return self.content_type.get_object_for_this_type(pk=self.object_id)

    # def set_product(self, product):
    #     # self.content_type = ContentType.objects.get_for_model(type(product))
    #     self.object_id = self.pk


    # def save(self):
    #     if not self.image:
    #         return            

    #     super(Item, self).save()
    #     imageFile = Image.open(self.image)
    #     # (width, height) = image.size     
    #     size = ( 150, 150)
    #     # image = image.resize(size, Image.ANTIALIAS)
    #     imageFile.save(self) 

    # def resize_image(self):
    # # resize image
    #     if not self.image:
    #         return

    #     imagefile  = StringIO.StringIO(i.read())
    #     imageImage = Image.open(imagefile)

    #     (width, height) = imageImage.size
    #     (width, height) = scale_dimensions(width, height, longest_side=240)

    #     resizedImage = imageImage.resize((width, height))

    #     imagefile = StringIO.StringIO()
    #     resizedImage.save(imagefile,'JPEG')
        # ...     


class Service(models.Model):
    image = StdImageField(upload_to='product_pictures/', help_text= "Service Picture", verbose_name="Service Pictures", null=True, blank=True, variations={'big-thumbnail': (250, 250, True), 'small-thumbnail': (150, 150, True)})
    title = models.CharField(max_length=20, null=False)
    planid = models.CharField(max_length=20, null=False, blank=False)
    value = models.DecimalField(decimal_places=2, max_digits=9, null=False)
    # quantity = models.DecimalField(decimal_places=0, max_digits=7, null=False)
    sku = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=25, null=False)
    # image = models.ImageField(upload_to='service_pictures/', null=True)
    # tax_rate = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    
    def __str__(self):
        return str(self.id)
    # def save(self, *args, **kwargs):
    #     super(Service, self).__init__(*args, **kwargs)
    #     ServicePlan.objects.create(title=self.title, planid=self.planid, value=self.value)

    def save(self, *args, **kwargs):
        stripe.Plan.create(
          amount = self.value,
          interval = "month",
          name = self.title,
          currency ="usd",
          id = self.planid
        )
        super(Service, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        plan = stripe.Plan.retrieve(self.planid)
        plan.delete()
        super(Service, self).delete(*args, **kwargs)



class ItemSale(models.Model):
    """
    A sale item, with the associated products, quantity and price
    """
    item = models.ForeignKey(Item)
    # cart = models.ForeignKey(Cart)
    purchaser = models.ManyToManyField(userStripe)
    purchase_time = models.DateTimeField(auto_now=True, null=False)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=9, null=False)

    objects = ItemManager()

class SubscriptionSale(models.Model):
    """
    A sale item, with the associated service and price
    """
    service = models.ForeignKey(Service)
    # cart = models.ForeignKey(Cart)
    purchaser = models.ManyToManyField(userStripe)
    purchase_time = models.DateTimeField(auto_now=True, null=False)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=9, null=False)
