from django.urls import path, include
from .views import AllDogsAV, DogBYidAV,Prev_OwnerAV,Owner_detailAV,Liked_DogList,Liked_create,update_like


urlpatterns = [
    path("all_dogs",AllDogsAV.as_view(),name='all_dogs'),
    path("ownerlist",Prev_OwnerAV.as_view(),name='ownerlist'),
    path("<int:pk>",DogBYidAV.as_view(),name='dogs_by_id'),
    path("ownerlist/<int:pk>",Owner_detailAV.as_view(),name='owner_by_id'),
    path("dogs/<int:pk>/liked",Liked_DogList.as_view(),name='liked_dogs'),
    path("dogs/<int:pk>/do-like",Liked_create.as_view(),name='do_like'),
    path("dogs/<int:pk>/update-like",update_like.as_view(),name='update_like')

    
]
