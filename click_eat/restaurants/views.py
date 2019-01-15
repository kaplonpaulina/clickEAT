from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q,Sum
from django.contrib import messages
from django.utils import timezone



from .models import Restaurant, Category, FavouriteRestaurants, Comment,Rating,InfoRating
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


    if(request.POST.get('addComm')):
        addComment(request, restaurant)

    queryset = Comment.objects.filter(restaurant =restaurant)

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


    if(request.POST.get('addRating')):
        addRating(request,restaurant)
    if(request.POST.get('positiveRating')):
        addInfoRating(request,restaurant,1)
    if(request.POST.get('negativeRating')):
        addInfoRating(request,restaurant,-1)
    if(request.POST.get('add_fav')):
        addFavRestaurant(request,restaurant) #int(request.GET.get('mytextbox')) )
    if(request.POST.get('del_fav')):
        delFavRestaurant(request,restaurant)
    isFavourite = isFav(request,restaurant)

    context = {
        'restaurant':restaurant,
        'isFav':isFavourite,
        "items":items,
        "page_range":page_range,
        "queryset":queryset,
        "userRating":dispalyUserRating(request,restaurant),
        "userInfoRating":dispalyUserInfoRating(request,restaurant)


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

def edit_restaurant(request, pk):
    template = 'new_restaurant.html'
    restaurant = get_object_or_404(Restaurant, pk = pk)

    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)

        try:
            if form.is_valid():
                form.save()
                infoRatings = InfoRating.objects.filter(restaurant=restaurant).delete()
                restaurant.infoRate = 0
                restaurant.save()
                messages.success(request, 'restaurant updated:)')
        except Exception as e:
            messages.warning(request,'Your update was not saved . error :()'.format(e))
    else:
        form = RestaurantForm(instance = restaurant)
    context = {
        'form': form,
        'restaurnat': restaurant,
    }



    return render(request, template, context)

def addFavRestaurant(request,restaurant):
    FavouriteRestaurants.objects.get_or_create(user = request.user.username, restaurant = restaurant)

def delFavRestaurant(request,restaurant):
    FavouriteRestaurants.objects.filter(user = request.user.username, restaurant = restaurant).delete()

def isFav(request,restaurant):
    return FavouriteRestaurants.objects.filter(user = request.user.username, restaurant = restaurant).exists()

def addComment(request, restaurant):
    title = request.POST.get('title').strip()
    body = request.POST.get('body').strip()
    Comment.objects.create(author = request.user.username, restaurant=restaurant,title=title,body=body)

def addRating(request, restaurant):
    rating, created = Rating.objects.update_or_create(user = request.user.username, restaurant = restaurant)
    rating.score = int(request.POST.get('rating'))
    rating.save()
    ratings = Rating.objects.filter(restaurant = restaurant)
    sum = ratings.aggregate(total=Sum('score'))['total']
    count = ratings.count()
    restaurant.rate = float(sum)/count
    restaurant.save()

def dispalyUserRating(request,restaurant):
    try:
        foo = int(Rating.objects.get(user = request.user.username, restaurant = restaurant).score)
    except Rating.DoesNotExist:
        foo = "no your rating yet, please rate"
    return foo

def addInfoRating(request, restaurant, score):
    rating, created = InfoRating.objects.update_or_create(user = request.user.username, restaurant = restaurant)
    rating.rate = score
    rating.save()
    ratings = InfoRating.objects.filter(restaurant = restaurant)
    sum = ratings.aggregate(total=Sum('rate'))['total']
    restaurant.infoRate = sum
    restaurant.save()

def dispalyUserInfoRating(request,restaurant):
    try:
        foo = InfoRating.objects.get(user = request.user.username, restaurant = restaurant).rate
    except InfoRating.DoesNotExist:
        foo = "no your rating yet, please rate"
    return foo
