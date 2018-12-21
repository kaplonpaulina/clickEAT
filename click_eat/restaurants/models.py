from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import User
from enum import Enum
from django.utils import timezone

# Create your models here.

#class PriceChoice(Enum):   # A subclass of Enum
#    T = "TANIO"
#    U = "UMIARKOWANIE"
#    D = "DROGO"

PriceChoice = [
    (1, "tanio"),
    (2, "przystępnie"),
    (3, "drogo"),
]

Weekdays = [
    (1, "poniedziałek"),
    (2, "wtorek"),
    (3, "środa"),
    (4, "czwartek"),
    (5, "piątek"),
    (6, "sobota"),
    (7, "niedziela")
]



class Category(models.Model):
    """

    Stores a unique category of :model:`restaurants.Restaurant`      

    """

    name = models.CharField(max_length = 255)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def __str__(self):
        return "@{}".format(self.name)

class Restaurant(models.Model):
    """

    Stores a unique named restaurant

    """


    name = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255,blank=True, null=True,default=None )
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    author = models.CharField(max_length = 255)
    #weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS)
    price = models.IntegerField(choices=PriceChoice,null=True,blank=True)
    opening_hours = models.TimeField(blank=True, null=True)
    closing_hours = models.TimeField(blank=True, null=True)

    #hours = models.ForeignKey(Hours, on_delete = models.CASCADE, blank=True, null=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE,unique=False)
    category = models.ForeignKey(Category, on_delete =models.CASCADE,unique=False)
    #ags = ArrayField(models.ForeignKey(Category, on_delete = models.CASCADE), null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Restaurant, self).save(*args,**kwargs)


    def __str__(self):
        return "@{}".format(self.name)

class Hours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE,null=True)
    day = models.IntegerField(choices=Weekdays,default=1)
    opening_time = models.TimeField(blank = True, null=True)
    closing_time = models.TimeField(blank = True, null=True)
