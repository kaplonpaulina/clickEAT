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
