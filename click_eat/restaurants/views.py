from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone



from .models import Restaurant, Category
from .forms import RestaurantForm,OpeningHoursForm

# Create your views here.
def list_restaurants(request):

    """
    Display a list of all of :model:`restaurants.Restaurant` using pagination from django.core.paginator.Paginator.

    **Context**

    ``items``
        An list of :model:`restaurants.Restaurant`.
    ``page_range``
        A list of pages which should be displayed.
    ``now``
        current time obtained from timezone.now() used to calculate if the :model:`restaurants.Restaurant` is currently open for buisness.



    **Template:**

    :template:`search.html`
    """


    template = 'search.html'
    queryset = Restaurant.objects.all()

    paginator = Paginator(queryset, 10)
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

    now = timezone.now()

    context = {
        "items":items,
        "page_range":page_range,
        "now":now
    }
    return render(request, template, context)

def restaurant_detail(request, slug):

    """
    Display a detailed page of :model:`restaurants.Restaurant` by slug

    **Context**

    ``restaurant``
        A unique instance of :model:`restaurants.Restaurant`.

    **Template:**

    :template:`detail.html`
    """

    template = 'detail.html'

    restaurant = get_object_or_404(Restaurant, slug=slug)
    context = {
        'restaurant':restaurant,
    }
    return render(request,template,context)

def category_detail(request, slug):

    template = 'category_detail.html'
    category = get_object_or_404(Category, slug=slug)
    restaurant = Restaurant.objects.filter(category=category)
    context = {
        'resturant_by_category':restaurant,'category':category,
    }
    return render(request,template,context)


def search(request):


    """
        Display a list of all of :model:`restaurants.Restaurant` using pagination from django.core.paginator.Paginator using filtration by name

        **Context**

        ``items``
            An list of :model:`restaurants.Restaurant`.
        ``page_range``
            A list of pages which should be displayed.
        ``query``
            A query from GET with name q.

        **Template:**

        :template:`search.html`
    """

    template = 'search.html'
    query = request.GET.get('q')

    if query:
        queryset = Restaurant.objects.filter(Q(name__icontains=query))
    else:
        queryset = Restaurant.objects.all()

    paginator = Paginator(queryset, 10)
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
        "query":query
    }
    return render(request, template, context)

def new_Restaurant(request):
    """
        Handle of the RestaurantForm

        **Context**

        ``form``
            A form of the new added :model:`restaurants:Restaurant`.
        **Template:**

        :template:`new_restaurant.html`
    """

    template = 'new_restaurant.html'
    form = RestaurantForm(request.POST or None)

    try:
        if form.is_valid():
            form.save()
            messages.success(request, 'new restaurant was added')

    except Exception as e:
        form = RestaurantForm()
        messages.warning(request, 'restaurant was not added. Error {}'.format(e))

    context = {
        'form':form
    }

    return render(request,template,context)

def Opening(request):
    template = 'new.html'
    form = OpeningHoursForm(request.POST or None)

    try:
        if form.is_valid():
            form.save()
            messages.success(request, 'information updated')

    except Exception as e:
        form = OpeningHoursForm()
        messages.warning(request, 'something wet wrong. Error {}'.format(e))

    context = {
        'form':form
    }

    return render(request,template,context)
