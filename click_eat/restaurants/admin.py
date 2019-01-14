from django.contrib import admin

from .models import Restaurant, Category, Comment, FavouriteRestaurants


# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(FavouriteRestaurants)
