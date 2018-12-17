from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import User
from enum import Enum
# Create your models here.

class PriceChoice(Enum):   # A subclass of Enum
    T = "TANIO"
    U = "UMIARKOWANIE"
    D = "DROGO"

class Category(models.Model):
    name = models.CharField(max_length = 255)
    def __str__(self):
        return "@{}".format(self.name)

class Restaurant(models.Model):
    name = models.CharField(max_length = 255)
    adress = models.CharField(max_length = 255,blank=True, null=True,default=None )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    author = models.CharField(max_length = 255)
    price = models.CharField(max_length = 5, choices=[(tag, tag.value) for tag in PriceChoice],null=True,blank=True)
    opening_hours = models.TimeField(blank=True, null=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE,unique=False)
    category = models.ForeignKey(Category, on_delete =models.CASCADE,unique=False)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant, self).save(*args,**kwargs)


    def __str__(self):
        return "@{}".format(self.name)
