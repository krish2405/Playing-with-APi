from django.db import models

# Create your models here.

class Breed(models.Model):
    name=models.CharField(max_length=100,)
    breed=models.CharField(max_length=100)
    age=models.IntegerField()
    weight=models.FloatField()

    def __str__(self): 
        return f'{self.name} is breed of {self.breed}' 