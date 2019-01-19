from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


from . import forms
from restaurants.models import Restaurant, Category, FavouriteRestaurants, RestauratsCategory

class SignUp(CreateView):
    """
        A handle of the sign up

        **Context**

        **Template:**

        :template:`accounts/signup.html`
    """

    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


def listFavouriteRestaurants(request):

    """

        Makes a list of favourite restaurants.
        From request extracts logged :model:`auth.User`,
        then from :model:`restaurants.FavouriteRestaurants` 
        extrsacts favourite rsetaurnat for a given user

        **Context**

        items - list of favourite restaurants on a given page_range

        page_range - given page

        categories - all :model:`restaurants.RestauratsCategory` objects

        **Template**

        :template:`accounts/profile.html`

    """
    template = 'profile.html'
    queryset = FavouriteRestaurants.objects.filter(user =request.user)

    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        "items":items,
        "page_range":page_range,
        "categories":RestauratsCategory.objects.all()

    }
    return render(request, template, context)
