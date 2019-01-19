from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q,Sum
from django.contrib import messages
from django.utils import timezone



from .models import Restaurant, Category, FavouriteRestaurants, Comment,Rating,InfoRating,RestauratsCategory
from .forms import RestaurantForm,CategoryRestaurantForm

# Create your views here.

def list_categories(request):

    """

        Makes a list of restaurant categories.
        And lists them with all corresponding restaurants using :model:`restaurants.RestauratsCategory`


        **Context**

        ``items``
        List of :model:`restaurants.Category` on a given page

        ``page_range``
        Given page

        ``now``
        Current time

        ``categories``
        All :model:`restaurants.RestauratsCategory` objects

        **Template**

        :template:`restaurants/categories.html`

    """

    template = 'categories.html'
    queryset = Category.objects.all()

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
        "now":now,
        "categories":RestauratsCategory.objects.all()
    }
    return render(request, template, context)

def list_restaurants(request):

    """
    Display a list of all of :model:`restaurants.Restaurant` using pagination from django.core.paginator.Paginator.
    For each restaurnat the corresponding :model:`restaurants.Category` are listed using :model:`restaurants.RestauratsCategory`

    **Context**

    ``items``
        An list of :model:`restaurants.Restaurant`.
    ``page_range``
        A list of pages which should be displayed.
    ``now``
        Current time obtained from timezone.now() used to calculate if the :model:`restaurants.Restaurant` is currently open for buisness.
    ``categories``
        All :model:`restaurants.RestauratsCategory` objects


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
        "now":now,
        "categories":RestauratsCategory.objects.all()
    }
    return render(request, template, context)

def restaurant_detail(request, slug):

    """
    Display a detailed page of :model:`restaurants.Restaurant` by slug
    with all comments and ratings visible for all users, and user's ratings visible for looge users

    **Context**

    ``restaurant``
        A unique instance of :model:`restaurants.Restaurant`.
    ``isFav``
        Boolean - true if the restaurant is one of the logged user favourite, information from :model:`restaurants.FavouriteRestaurants`
    ``items``
        List of :model:`restaurants.Comment` on a given page
    ``page_range``
        Given page

    ``userRating``
        Loqged user's ratign of the restaurant, using :model:`restaurants.Rating`
    ``userInfoRating``
        Loqged user's ratign of the informations about the restaurant since the last update, using :model:`restaurants.InfoRating`
    ``categories``
        All :model:`restaurants.RestauratsCategory` objects, to display the restaurant's categories

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

    # hendlig buttons/user inputs

    if(request.POST.get('addRating')):
        addRating(request,restaurant)
    if(request.POST.get('positiveRating')):
        addInfoRating(request,restaurant,1)
    if(request.POST.get('negativeRating')):
        addInfoRating(request,restaurant,-1)
    if(request.POST.get('add_fav')):
        addFavRestaurant(request,restaurant)
    if(request.POST.get('del_fav')):
        delFavRestaurant(request,restaurant)
    isFavourite = isFav(request,restaurant)

    context = {
        'restaurant':restaurant,
        'isFav':isFavourite,
        "items":items,
        "page_range":page_range,
        "userRating":dispalyUserRating(request,restaurant),
        "userInfoRating":dispalyUserInfoRating(request,restaurant),
        "categories":RestauratsCategory.objects.all()


    }

    return render(request,template,context)

def category_detail(request, slug):

    """
    Display a detailed page of :model:`restaurants.Category` by slug
    with all restaurant corresponding to the category

    **Context**

    ``resturant_by_category``
        List of :model:`restaurants.Restaurant` objects with the category

    ``category``
        Instance of the :model:`restaurants.Category`

    **Template:**

    :template:`detail.html`
    """

    template = 'category_detail.html'
    category = get_object_or_404(Category, slug=slug)
    restaurant = RestauratsCategory.objects.filter(category=category)
    context = {
        'resturant_by_category':restaurant,
        'category':category,
    }
    return render(request,template,context)


def search(request):


    """
        Display a list of all of :model:`restaurants.Restaurant` using pagination from django.core.paginator.Paginator using filtration by name and category

        **Context**

        ``items``
            An list of :model:`restaurants.Restaurant`.
        ``page_range``
            A list of pages which should be displayed.
        ``query``
            A query from GET with name q.
        ``categories``
            All :model:`restaurants.RestauratsCategory` objects, to search by the restaurant's categories
        **Template:**

        :template:`search.html`
    """

    template = 'search.html'
    query = request.GET.get('q')

    if query:
        queryset1 = Restaurant.objects.filter(Q(name__icontains=query))
        queryset2_obj = RestauratsCategory.objects.filter(Q(category__name__icontains=query))
        queryset2 = []
        for restaurant in queryset2_obj:
            queryset2.append(restaurant.restaurant)

        queryset = list(set(list(queryset1)+queryset2))

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
        "query":query,
        "categories":RestauratsCategory.objects.all()
    }
    return render(request, template, context)

def new_Restaurant(request):
    """
        Handle of the RestaurantForm

        **Context**

        ``form``
            A form of the new added :model:`restaurants:Restaurant`.
        ``checked``
            List of :model:`restaurants.Category` 's names that the restaurant already have, to check in the multiplechoice checkboxes,
            here: []
        ``notChecked``
            List of :model:`restaurants.Category` 's names that the restaurant does not have, using information from :model:`restaurants.RestauratsCategory`

        **Template:**

        :template:`new_restaurant.html`
    """

    template = 'new_restaurant.html'
    form = RestaurantForm(request.POST or None)
    categoriesChecked = []
    categoriesNotChecked = getCategoryNames()

    try:
        if form.is_valid():
            form.save()

            updateRestaurantCategories(Restaurant.objects.get(name = request.POST.get('name')),request.POST.getlist('categories'))
            messages.success(request, 'new restaurant was added')

    except Exception as e:
        form = RestaurantForm()
        messages.warning(request, 'restaurant was not added. Error {}'.format(e))


    context = {
        'form':form,
        'checked':categoriesChecked,
        'notChecked':categoriesNotChecked
    }

    return render(request,template,context)

def edit_restaurant(request, pk):
    """
        Handle of the RestaurantForm while editing an existing one

        **Context**

        ``form``
            A form of the new added :model:`restaurants:Restaurant`.
        ``checked``
            List of :model:`restaurants.Category` 's names that the restaurant already have, to check in the multiplechoice checkboxes,
            using information from :model:`restaurants.RestauratsCategory`
        ``notChecked``
            List of :model:`restaurants.Category` 's names that the restaurant does not have, using information from :model:`restaurants.RestauratsCategory`
        ``restaurnat``
            Instance of :model:`restaurants.Restaurant` which is being updated

        **Template:**

        :template:`new_restaurant.html`
    """

    template = 'new_restaurant.html'
    restaurant = get_object_or_404(Restaurant, pk = pk)
    categoriesChecked = getCategoriesInitials(restaurant)
    categoriesNotChecked = getCategoriesNoINitials(restaurant,categoriesChecked)

    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        #form2= RestauratsCategory(request.POST)


        try:
            if form.is_valid():
                form.save()
                infoRatings = InfoRating.objects.filter(restaurant=restaurant).delete()
                restaurant.infoRate = 0
                restaurant.save()
                updateRestaurantCategories(restaurant,request.POST.getlist('categories'))
                messages.success(request, 'restaurant updated:)')
        except Exception as e:
            messages.warning(request,'Your update was not saved . error :()'.format(e))
            form = RestaurantForm(isinstance = restaurant)
    else:
        form = RestaurantForm(instance = restaurant)
        #form2 = RestauratsCategory()
    context = {
        'form': form,
        'checked':categoriesChecked,
        'notChecked':categoriesNotChecked,
        'restaurnat': restaurant,
    }
    return render(request, template, context)

def addFavRestaurant(request,restaurant):
    """
        Create a new :model:`restaurants.FavouriteRestaurants` instance using request.user.username and :model:`restaurants.Restaurant` restaurnat
    """
    FavouriteRestaurants.objects.get_or_create(user = request.user.username, restaurant = restaurant)

def delFavRestaurant(request,restaurant):
    """
        Delete if exists :model:`restaurants.FavouriteRestaurants` instance with fileds : request.user.username and :model:`restaurants.Restaurant` restaurnat
    """
    FavouriteRestaurants.objects.filter(user = request.user.username, restaurant = restaurant).delete()

def isFav(request,restaurant):
    """
        Check if :model:`restaurants.FavouriteRestaurants` instance with fileds : request.user.username and :model:`restaurants.Restaurant` restaurnat exists
    """
    return FavouriteRestaurants.objects.filter(user = request.user.username, restaurant = restaurant).exists()

def addComment(request, restaurant):
    """
        Create a new :model:`restaurants.Comment` instance using request.user.username, request POST messages and :model:`restaurants.Restaurant` restaurnat
    """
    title = request.POST.get('title').strip()
    body = request.POST.get('body').strip()
    Comment.objects.create(author = request.user.username, restaurant=restaurant,title=title,body=body)

def addRating(request, restaurant):
    """
        Create a new :model:`restaurants.Rating` instance or update existing using request.user.username and :model:`restaurants.Restaurant` restaurnat,
        update the restaurnat's rate field
    """
    rating, created = Rating.objects.update_or_create(user = request.user.username, restaurant = restaurant)
    rating.score = int(request.POST.get('rating'))
    rating.save()
    ratings = Rating.objects.filter(restaurant = restaurant)
    sum = ratings.aggregate(total=Sum('score'))['total']
    count = ratings.count()
    restaurant.rate = float(sum)/count
    restaurant.save()

def dispalyUserRating(request,restaurant):
    """
        Get a :model:`restaurants.Rating` instance' score for using request.user.username and :model:`restaurants.Restaurant` restaurnat,
        when none return string calling to rate
    """
    try:
        foo = int(Rating.objects.get(user = request.user.username, restaurant = restaurant).score)
    except Rating.DoesNotExist:
        foo = "no your rating yet, please rate"
    return foo

def addInfoRating(request, restaurant, score):
    """
        Create a new :model:`restaurants.InfoRating` instance or update existing using request.user.username, score - value of rating send by POST :model:`restaurants.Restaurant` restaurnat,
        update the restaurnat's inoRate field
    """
    rating, created = InfoRating.objects.update_or_create(user = request.user.username, restaurant = restaurant)
    rating.rate = score
    rating.save()
    ratings = InfoRating.objects.filter(restaurant = restaurant)
    sum = ratings.aggregate(total=Sum('rate'))['total']
    restaurant.infoRate = sum
    restaurant.save()

def dispalyUserInfoRating(request,restaurant):
    """
        Get a :model:`restaurants.InfoRating` instance' score for using request.user.username and :model:`restaurants.Restaurant` restaurnat,
        when none return string calling to rate
    """
    try:
        foo = InfoRating.objects.get(user = request.user.username, restaurant = restaurant).rate
    except InfoRating.DoesNotExist:
        foo = "no your rating yet, please rate"
    return foo

def addCategories(categories,restaurant_str):
    """
        Delete all :model:`restaurants.RestauratsCategory` corresponding to :model:`restaurants.Restaurant`'name,
        then create a new instance of :model:`restaurants.RestauratsCategory` for each :model:`restaurants.Category`'s name in given categories
    """
    restaurant = Restaurant.objects.get(name=restaurant_str)
    RestauratsCategory.objects.filter(restaurant=restaurant).delete()

    for category_str in categories:
        category = Category.objects.get(name = category_str)
        new_category = RestauratsCategory.objects.create(restaurant = restaurant, category = category)
        new_category.save()

def getCategoriesInitials(restaurant):
    """
        Get a list of :model:`restaurants.Category`'s names that a given :model:`restaurants.Restaurant` have,
        using :model:`restaurants.RestauratsCategory`
    """
    queryset = RestauratsCategory.objects.filter(restaurant = restaurant)
    categories = []
    for category in queryset:
        categories.append(category.category.name)
    return categories

def getCategoriesNoINitials(restaurant,checked):
    """
        Get a list of :model:`restaurants.Category`'s names that a given :model:`restaurants.Restaurant` does not have,
        using :model:`restaurants.RestauratsCategory`
    """
    queryset_name = getCategoryNames()

    queryset = set(queryset_name) - set(checked)
    categories = []
    for category in queryset:
        categories.append(category)
    print(categories)
    return categories

def getCategoryNames():
    """
        Get list of all :model:`restaurants.Category`'s names
    """
    queryset_obj = Category.objects.all()
    queryset_name = []
    for obj in queryset_obj:
        queryset_name.append(obj.name)
    return queryset_name

def updateRestaurantCategories(resturant,categories):
    """
        LIke addCategories, but uses :model:`restaurants.Restaurant`
    """
    RestauratsCategory.objects.filter(restaurant = resturant).delete()
    for category_str in categories:
        category = Category.objects.get(name = category_str)
        new_category = RestauratsCategory.objects.create(restaurant= resturant, category = category)
        new_category.save()
def getCategoryNamesFromRestaurntCategory():
    """
        Get list of all :model:`restaurants.RestauratsCategory`'s names
    """
    queryset_obj = RestauratsCategory.objects.all()
    queryset = []
    for obj in queryset_obj:
        queryset.append(obj.category)
    return list(set(queryset))
