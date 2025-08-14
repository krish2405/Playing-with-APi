from django.urls import path, include
from .views import AllDogsAV, DogBYidAV


urlpatterns = [
    path("all_dogs",AllDogsAV.as_view(),name='all_dogs'),
    path("<int:pk>",DogBYidAV.as_view(),name='user_by_id')
]
