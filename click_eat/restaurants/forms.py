from django import forms

from .models import Restaurant,Hours

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['name','category','opening_hours','closing_hours','price','address']

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = Hours
        fields = ['restaurant','day','opening_time','closing_time']
