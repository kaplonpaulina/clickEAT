from django.conf.urls import url
from main_app import views

# TEMPLATE URLS!
app_name = 'main_app'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]
