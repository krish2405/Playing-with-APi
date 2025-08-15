from django.db import models
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
    in_shelter_date=models.DateTimeField(auto_now_add=True)
    adopted=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name} of {self.breed}"