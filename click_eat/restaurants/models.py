from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import User
from enum import Enum
from django.utils import timezone

PriceChoice = [
    (1, "tanio"),
    (2, "przystępnie"),
    (3, "drogo"),
]


class Category(models.Model):
    """

    Stores a unique category of :model:`restaurants.Restaurant`


    """

    name = models.CharField(max_length = 255, unique = True,help_text="category's unique name")
    slug = models.SlugField(max_length=200, unique=True,help_text="slugified name (so it can be used as web address)")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def __str__(self):
        return "@{}".format(self.name)

class Restaurant(models.Model):
    """

    Stores a unique named restaurant


    """


    name = models.CharField(max_length = 255,unique=True,help_text="Unique restaurant name")
    address = models.CharField(max_length = 255,blank=True, null=True,default=None,help_text="Restaurnat address" )
    created = models.DateTimeField(editable=False,blank=True, null=True,help_text="Date when the instance was created")
    updated = models.DateTimeField(help_text="Date when the instance was last updated")
    author = models.CharField(max_length = 255,blank=True, null=True,help_text="Username of author")
    price = models.IntegerField(choices=PriceChoice,null=True,blank=True,help_text="Range of the prices")
    opening_hours = models.TimeField(blank=True, null=True,help_text="Opening hours")
    closing_hours = models.TimeField(blank=True, null=True,help_text="Closing hours")
    rate = models.FloatField(blank=True,null=True,help_text="Rating of the restaurnt")
    infoRate = models.IntegerField(default=0,blank=True,null=True,help_text="Rating of the displayed information about the restaurnt since the last update")
    slug = models.SlugField(max_length=200, unique=True,help_text="Slugified name (so it can be used as web address)")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.id:
            self.created = timezone.now()
            self.rating = 0
            self.infoRate = 0
        self.updated = timezone.now()
        super(Restaurant, self).save(*args,**kwargs)


    def __str__(self):
        return "@{}".format(self.name)

class Comment(models.Model):
    """

    Stores a comment

    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE,null=True,help_text="Instance of :model:`restaurants.Restaurant`")
    author = models.CharField(max_length = 255, blank=True, null=True,help_text="Username of author")
    created = models.DateTimeField(editable=False, blank=True, null=True,help_text="Date when the instance was created")
    title = models.CharField(max_length=255, blank=True, null=True,help_text="Title of the comment")
    body = models.CharField(max_length=255, blank=True, null=True,help_text="The messenge of the comment")
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        super(Comment, self).save(*args,**kwargs)
    def __str__(self):
        return "@{}".format(self.author +" "+ self.restaurant.name +" "+self.title)

class FavouriteRestaurants(models.Model):
    """

    Connection between a restaurnat and an user , that indicates that the restaurant is user's favourite

    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE,null=True,help_text="Instance of :model:`restaurants.Restaurant`")
    user = models.CharField(max_length=255,help_text="Instance of :model:`auth.User`")

    def __str__(self):
        return "@{}".format(self.user+" "+ self.restaurant.name)

class Rating(models.Model):
    """

    Connection between a restaurnat and an user, that indicates the user's rating for the restaurant


    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, null=True,help_text="Instance of :model:`restaurants.Restaurant`")
    user = models.CharField(max_length=255,help_text="Instance of :model:`auth.User`")
    score = models.IntegerField(null=True,help_text="Value of the user's rating")

    def __str__(self):
        return "@{}".format(self.user+" "+ self.restaurant.name + " " + str(self.score))

class InfoRating(models.Model):
    """

    Connection between a restaurnat and an user, that indicates the user's rating for the displayed infrmation about the restaurant since latest update


    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, null=True,help_text="Instance of :model:`restaurants.Restaurant`")
    user = models.CharField(max_length=255,help_text="Instance of :model:`auth.User`")
    rate = models.IntegerField(null=True,help_text="Value of the user's rating, (-1,1,0 = default)")
    def save(self, *args, **kwargs):
        if not self.id:
            self.rate = 0
        super(InfoRating, self).save(*args,**kwargs)

    def __str__(self):
        return "@{}".format(self.user+" "+ self.restaurant.name + " " + str(self.rate))


class RestauratsCategory(models.Model):
    """

    Connection between a restaurnat and an category, that indicates that the restaurant has the category


    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, null=True,help_text="Instance of :model:`restaurants.Restaurant`")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True,help_text="Instance of :model:`restaurants.Category`")
    def __str__(self):
        return "@{}".format(self.restaurant.name+" "+ str(self.category))
