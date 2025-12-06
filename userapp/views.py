from django.shortcuts import render
from .serializer import UserSerilaizer,ProfileSerializer as PrSerilaizer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class=UserSerilaizer
    queryset=User.objects.all()

    def perform_create(self, serializer):
        user=serializer.save()
        data={}
        if user:
            for user in User.objects.all():
                token,created=Token.objects.get_or_create(user=user)
                data['token']=token.key
            data['message']="User registered successfully"
            data['username']=user.username
            data['email']=user.email
            return Response(data,status=201)
        raise ValidationError("User could not be created")


# class RegisterView(APIView):
#     def post(self,request):
#         serializer=UserSerilaizer(data=request.data)
#         data ={}
#         if serializer.is_valid():
#             account=serializer.save()
#             for user in User.objects.all():
#                 token,created=Token.objects.get_or_create(user=user)
#                 data['token']=token.key
#             data['message']="User registered successfully"
#             data['username']=account.username
#             data['email']=account.email
#             return Response(data,status=201)
#         return Response(serializer.errors,status=400)


class profile_view(APIView):
    def get(self,request):
        curr_user=request.user
        account=User.objects.filter(username=curr_user)
        if account.exists() is False:
            raise ValidationError("User does not exist",code=404)    
        account=account.first()
        serializer=PrSerilaizer(account)
        return Response(serializer.data,status=200)
    
class profile_view(generics.RetrieveAPIView):
    serializer_class=PrSerilaizer
    # queryset=User.objects.all()
    # lookup_field='username'

    def get_object(self):
        return self.request.user
    
class logout_view(APIView):
    def get(self,request):
        curr_user=request.user
        Token.objects.filter(user=curr_user).delete()
        return Response({"message":"User logged out successfully"},status=200)
        
