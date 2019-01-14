from django import forms

from .models import Restaurant,Hours

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['name','category','opening_hours','closing_hours','price','address']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].label = 'nazwa'
        self.fields['category'].label = 'kategoria'
        self.fields['opening_hours'].label = 'godzina otwarcia'
        self.fields['closing_hours'].label = 'godzina zamkniecia'
        self.fields['price'].label = 'zakres cen'
        self.fields['address'].label = 'adres'

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = Hours
        fields = ['restaurant','day','opening_time','closing_time']
