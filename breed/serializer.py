from rest_framework import serializers
from .models import Breed

class BreedSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100,required=True)
    breed=serializers.CharField(max_length=100,required=False)
    age=serializers.IntegerField(required=False)
    weight=serializers.FloatField(required=False)

    def create(self,validated_data):
        return Breed.objects.create(**validated_data) 
    
    def update(self,instance,data):
        instance.name=data.get('name',instance.name)
        instance.breed=data.get('breed',instance.breed)
        instance.age=data.get('age',instance.age)
        instance.weight=data.get('weight',instance.weight)
        instance.save()

        return instance