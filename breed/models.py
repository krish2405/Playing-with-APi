from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Prev_Owner(models.Model):
    name=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    phone=models.IntegerField()
    
    def __str__(self):
        return self.name
    


class Dogs_Info(models.Model):
    name=models.CharField(max_length=100,)
    breed=models.CharField(max_length=100)
    age=models.IntegerField()
    weight=models.FloatField()
    in_shelter_date=models.DateTimeField(timezone.now)
    prev_owner=models.ForeignKey(Prev_Owner,related_name='dogs',on_delete=models.CASCADE,null=True,blank=True)
    adopted=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name} of {self.breed}"


class Liked_Dogs(models.Model):
    dog=models.ForeignKey(Dogs_Info,related_name='liked_dogs',on_delete=models.CASCADE)
    liked_by=models.ForeignKey(User,related_name='liked_User',on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    liked=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.liked_by} liked {self.dog.name}'