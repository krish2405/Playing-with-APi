from django.urls import path, include
from .views import all_dogs,user_by_id


urlpatterns = [
    path("all_dogs",all_dogs,name='all_dogs'),
    path("<int:pk>",user_by_id,name='user_by_id')
]
