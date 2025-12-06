from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator



class UserSerilaizer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model=User
        fields=['username','email','password','password2']
        extra_kwargs={'password':{'write_only':True}}  

    def validate(self,data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError("Password and Confirm Password must be same")
        return data
    
    def validate_user(self,value):
        curr_user=value
        queryset=User.objects.get(username=curr_user)
        if queryset:
            raise serializers.ValidationError("User with this username already exists")
        return curr_user



    def create(self,validated_data):
        password=validated_data.pop('password')
        validated_data.pop('password2')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']
        read_only_fields=['id','username','email']

    
