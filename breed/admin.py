from django.contrib import admin
from .models import Dogs_Info,Prev_Owner,Liked_Dogs

# Register your models here.

admin.site.register(Dogs_Info,)
admin.site.register(Prev_Owner)
admin.site.register(Liked_Dogs)


