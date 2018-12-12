from django.db import models

# Create your models here.


class Restaurant(models.Model):
    tx = models.CharField(max_length = 255)
    update_date = models.DateField()
