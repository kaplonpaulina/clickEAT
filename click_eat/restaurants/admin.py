from django.contrib import admin

from .models import Restaurant, Category, Hours


# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Hours)
