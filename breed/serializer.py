from rest_framework import serializers
from .models import Breed

class BreedSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    breed=serializers.CharField(max_length=100)
    age=serializers.IntegerField()
    weight=serializers.FloatField()

    def create(self,validated_data):
        return Breed.objects.create(**validated_data) 
    
    def update(self,instance,data):
        instance.name=data.get('name',instance.name)
        instance.breed=data.get('breed',instance.breed)
        instance.breed=data.get('age',instance.age)
        instance.breed=data.get('weight',instance.weight)
        instance.save()

        return instance