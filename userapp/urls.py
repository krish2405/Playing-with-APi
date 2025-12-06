from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView,profile_view,logout_view

urlpatterns = [
    path('login/',obtain_auth_token,name='api_auth_token'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',profile_view.as_view(),name='profile'),
    path('logout/',logout_view.as_view(),name='logout'),
]
