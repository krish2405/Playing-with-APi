from django.urls import path, include
from .views import AllDogsAV, DogBYidAV,Prev_OwnerAV,Owner_detailAV,Liked_DogAV


urlpatterns = [
    path("all_dogs",AllDogsAV.as_view(),name='all_dogs'),
    path("ownerlist",Prev_OwnerAV.as_view(),name='ownerlist'),
    path("<int:pk>",DogBYidAV.as_view(),name='dogs_by_id'),
    path("ownerlist/<int:pk>",Owner_detailAV.as_view(),name='owner_by_id'),
    path("likeddogs",Liked_DogAV.as_view(),name='liked_dogs')

    
]
