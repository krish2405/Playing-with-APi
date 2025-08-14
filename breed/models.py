from django.db import models

# Create your models here.

class Breed(models.Model):
    name=models.CharField(max_length=100)
    breed=models.CharField(max_length=100,required=False)
    age=models.IntegerField(required=False)
    weight=models.FloatField(required=False)
