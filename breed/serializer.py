from rest_framework import serializers,validators
from .models import Breed


def age_weight(value):
    if value<=0:
        raise serializers.ValidationError("Invalid value,less than equal to 0 not expected")
    return value

class BreedSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100,required=True)
    breed=serializers.CharField(max_length=100,required=False)
    age=serializers.IntegerField(required=False,validators=[age_weight])
    weight=serializers.FloatField(required=False,validators=[age_weight])

    def create(self,validated_data):
        return Breed.objects.create(**validated_data) 
    
    def update(self,instance,data):
        instance.name=data.get('name',instance.name)
        instance.breed=data.get('breed',instance.breed)
        instance.age=data.get('age',instance.age)
        instance.weight=data.get('weight',instance.weight)
        instance.save()

        return instance
    
    #feild level validation
    def validate_name(self,value):
        if len(value)<3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value
    
    #object level validations
    def validate(self,data):
        if data.get("name")==data.get('breed'):
            raise serializers.ValidationError("Name and breed cannot be same")
        return data