from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'restaurants'

urlpatterns = [
    url(r'^$',views.list_restaurants, name="list"),
    url(r'^categories/$',views.list_categories,name="categories"),
    url(r'^results/$',views.search, name="search"),
    url(r'^new_restaurant/$', views.new_Restaurant, name="new_restaurant"),
    url(r'^edit-resturant/(?P<pk>\d+)/$',views.edit_restaurant, name="edit_restaurant"),
    url(r'^category_detail/(?P<slug>[-\w]+)/$',views.category_detail,name='category_detail'),
    url(r'^(?P<slug>[-\w]+)/$', views.restaurant_detail, name="detail"),

]
