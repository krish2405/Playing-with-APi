from rest_framework import serializers,validators
from .models import Prev_Owner,Dogs_Info,Liked_Dogs
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User



class Liked_DogSerializer(serializers.ModelSerializer):
    liked_by=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model=Liked_Dogs
        fields="__all__"
        read_only_fields=['id','created_at','updated_at']

    def validate_active(self,value):
        if value is False:
            raise serializers.ValidationError("Active must be True")
        return value

    
class DogInfoSerializer(serializers.ModelSerializer):

    liked_dogs=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    len_name=serializers.SerializerMethodField(method_name="get_len_name")
    day_in_shelter=serializers.SerializerMethodField(method_name="get_days")
    prev_owner=serializers.StringRelatedField(read_only=True) 
    class Meta:
        model=Dogs_Info
        fields="__all__"
        # fields=['id','name','breed','len_name']
        read_only_fields=['id']

    def get_len_name(self,object):
        return len(object.name)
    
    def get_days(self,object):
        today=timezone.now()
        return (today - object.in_shelter_date).days

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


class Prev_ownerSerilaizer(serializers.HyperlinkedModelSerializer):
    dogs=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='dogs_by_id')
    class Meta:
        model=Prev_Owner
        fields="__all__"
        # read_only_fields=['id']
        extra_kwargs = {
            'url': {'view_name': 'owner_by_id'}  # must match urls.py
        }
        
    def validate_phone(self,value):
        if value==0:
            raise serializers.ValidateError("invalid phone number")
        return value
    
