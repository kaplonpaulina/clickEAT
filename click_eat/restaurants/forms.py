from django import forms

from .models import Restaurant, RestauratsCategory, Category

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['name','opening_hours','closing_hours','price','address']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].label = 'nazwa'
        self.fields['opening_hours'].label = 'godzina otwarcia'
        self.fields['closing_hours'].label = 'godzina zamkniecia'
        self.fields['price'].label = 'zakres cen'
        self.fields['address'].label = 'adres'


class CategoryRestaurantForm(forms.Form):
    categories = Category.objects.all()
    names =[]
    for n in categories:
        names.append(str(n)[1:])
    CHOISES = zip(names,names)

    picked = forms.MultipleChoiceField(choices=CHOISES, widget=forms.CheckboxSelectMultiple())
