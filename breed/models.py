from django.db import models

# Create your models here.

class Breed(models.Model):
    name=models.CharField(max_length=100,required=False)
    breed=models.CharField(max_length=100,required=False)
    age=models.IntegerField(required=False)
    weight=models.FloatField(required=False)

    def __str__(self): 
        return f'{self.name} is breed of {self.breed}' 