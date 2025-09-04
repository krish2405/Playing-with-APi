from django.shortcuts import render
from .models import Dogs_Info,Prev_Owner,Liked_Dogs
from django.contrib.auth.models import User
from .serializer import DogInfoSerializer,Prev_ownerSerilaizer,Liked_DogSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,NotAuthenticated
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins,generics
from breed import serializer
from .permissions import ReadonlyorAdminPermission
from rest_framework import permissions


class AllDogsAV(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        dogs=Dogs_Info.objects.all()
        serializer=DogInfoSerializer(dogs,many=True,context={'request':request})
        return Response(serializer.data,status='200')
    

    def post(self,request):
        serializer=DogInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
class DogBYidAV(APIView):
    def get(self,request,pk):
        try:
            dog=Dogs_Info.objects.get(pk=pk,)
        except Dogs_Info.DoesNotExist:
            return Response(status=404)
        
        serializer=DogInfoSerializer(dog,context={'request':request})
        return Response(serializer.data,status=200)
    

    def put(self,request,pk):
        try:
            dog=Dogs_Info.objects.get(pk=pk)
        except Dogs_Info.DoesNotExist:
            return Response(status=404)
        serializer=DogInfoSerializer(instance=dog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status='200')
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        try:
            dog=Dogs_Info.objects.get(pk=pk)
        except Dogs_Info.DoesNotExist:
            return Response(status=404)
        serializer=DogInfoSerializer(dog)
        dog.delete()
        return Response(serializer.data, status=204)
    
    
    
class Prev_OwnerAV(APIView):
    permission_classes=[ReadonlyorAdminPermission]
    def get(self,request):
        try:
            PreV_ownerlist=Prev_Owner.objects.all()
        except Prev_Owner.DoesNotExist:
            return Response(status="400")
            
        serializerOW=Prev_ownerSerilaizer(PreV_ownerlist,many=True,context={'request':request})
        return Response(serializerOW.data,status="200")
    
    def post(self,request):
        serializerOW=Prev_ownerSerilaizer(data=request.data,context={'request':request})
        if serializerOW.is_valid():
            serializerOW.save()
            return Response(serializerOW.data,status="200")
        return Response(serializerOW.errors,status="401")
    
class Owner_detailAV(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,pk):
        try:
            owner=Prev_Owner.objects.get(pk=pk)
        except Prev_Owner.DoesNotExist:
            return Response(status="404")
        serializerOW=Prev_ownerSerilaizer(owner,context={'request':request})
        return Response(serializerOW.data,status="200")
        
        
    def put(self,request,pk):
        try:
            owner=Prev_Owner.objects.get(pk=pk)
        except Prev_Owner.DoesNotExist:
            return Response(status="401")
            
        serializerOW=Prev_ownerSerilaizer(instance=owner,data=request.data)
        if serializerOW.is_valid():
            serializerOW.save()
            return Response(serializerOW.data,status="200")
        return Response(serializerOW.errors,status="401")

# class Liked_DogAV(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,generics.GenericAPIView):
    
#     queryset=Liked_Dogs.objects.all()
#     serializer_class=Liked_DogSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
class UserLikedDogAV(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Liked_DogSerializer
    queryset=Liked_Dogs.objects.all()
    # def get_queryset(self):
    #     return 

class Liked_DogList(generics.ListAPIView):
    serializer_class=Liked_DogSerializer
    
    def get_queryset(self):
        dog_id=self.kwargs['pk']
        return Liked_Dogs.objects.filter(dog__id=dog_id,active=True,liked=True)

class Liked_create(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Liked_DogSerializer

    def get_queryset(self):
        return Liked_Dogs.objects.all()

    def perform_create(self, serializer):
        dog_id=self.kwargs['pk']
        dog=Dogs_Info.objects.get(id=dog_id)
        curr_user=self.request.user
        if curr_user.is_anonymous:
            raise NotAuthenticated("You must be logged in to like")
        liked_queryset=Liked_Dogs.objects.filter(dog=dog,liked=True,liked_by=curr_user)
        print(liked_queryset)
        if liked_queryset.exists():
            raise ValidationError("You have---- already liked this dog")
        else:
            serializer.save(dog=dog,liked_by=curr_user,liked=True)


class update_like(generics.UpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Liked_DogSerializer
    def get_object(self):
        dog_id=self.kwargs['pk']
        curr_user=self.request.user
        if curr_user.is_anonymous:
            raise NotAuthenticated("You must be logged in to update like")
        try:
            print(Liked_Dogs.objects.get(dog__id=dog_id,liked=True,liked_by=curr_user))
            isliked=Liked_Dogs.objects.get(dog__id=dog_id,liked=True,liked_by=curr_user)
            return isliked
        except Liked_Dogs.DoesNotExist:
            raise ValidationError("You have not liked this dog yet")
    
    
    def perform_update(self,serializer,):
        data=self.request.data  
        if 'liked' not in data:
            raise ValidationError("You must provide liked field to update")
        if data['liked'] not in [True,False]:
            raise ValidationError("liked field must be true or false")
        if data['liked']==True:
            serializer.save(liked=True)
        else:   
            serializer.save(liked=False)
        

class yourliked(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Liked_DogSerializer
    def get_queryset(self):
        dog_id=self.kwargs['pk']
        curr_user=self.request.user
        if curr_user.is_anonymous:
            raise NotAuthenticated("You must be logged in to view your liked dogs")
        return Liked_Dogs.objects.filter(dog__id=dog_id,liked=True,liked_by=curr_user)

        
    

            
        
        
    
        
    


##Using APIViewclass based views
# Create your views here.

# @api_view(['GET','POST'])
# def all_dogs(request):
#     if request.method=='POST':
#         serializer=DogInfoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)
        
#     dogs=Dogs_Info.objects.all()
#     serializer=DogInfoSerializer(dogs,many=True)
#     return Response(serializer.data,status='200')


# @api_view(['GET','PUT','DELETE'])
# def user_by_id(request,pk):
#     try:
#         dog=Dogs_Info.objects.get(pk=pk)
#     except Dogs_Info.DoesNotExist:
#         return Response(status=404)
    
     
#     serializer=DogInfoSerializer(dog)
#     if request.method=='DELETE':
        
#         dog.delete()
#         return Response(serializer.data, status=204)
    
#     if request.method=='PUT':
#         serializer=DogInfoSerializer(instance=dog,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status='200')
#         return Response(serializer.errors,status='300')

    
    
#     return Response(serializer.data,status=200)