from django.shortcuts import render
from .models import Dogs_Info,Prev_Owner,Liked_Dogs
from django.contrib.auth.models import User
from .serializer import DogInfoSerializer,Prev_ownerSerilaizer,Liked_DogSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins,generics
from breed import serializer
from rest_framework import permissions


class AllDogsAV(APIView):
    permission_classes=[permissions.IsAuthenticated]
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
    def get(self,request):
        try:
            PreV_ownerlist=Prev_Owner.objects.all()
        except Prev_Owner.DoesNotExist:
            return Response(status="400")
            
        serializerOW=Prev_ownerSerilaizer(PreV_ownerlist,many=True,context={'request':request})
        return Response(serializerOW.data,status="200")
    
    def post(self,request):
        serializerOW=Prev_ownerSerilaizer(data=request.data)
        if serializerOW.is_valid():
            serializerOW.save()
            return Response(serializerOW.data,status="200")
        return Response(serializerOW.errors,status="401")
    
class Owner_detailAV(APIView):
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

class Liked_DogList(generics.ListAPIView):
    serializer_class=Liked_DogSerializer
    
    def get_queryset(self):
        dog_id=self.kwargs['pk']
        return Liked_Dogs.objects.filter(dog__id=dog_id,active=True,liked=True)

class Liked_create(generics.CreateAPIView):
    serializer_class=Liked_DogSerializer

    def get_queryset(self):
        return Liked_Dogs.objects.all()

    def perform_create(self, serializer):
        dog_id=self.kwargs['pk']
        dog=Dogs_Info.objects.get(id=dog_id)
        curr_user=self.request.user
        liked_queryset=Liked_Dogs.objects.filter(dog=dog,liked_by=curr_user)
        if liked_queryset.exists():
            raise ValidationError("You have already liked this dog")
        else:
            serializer.save(dog=dog,likeed_by=curr_user)


class update_like(generics.UpdateAPIView):
    serializer_class=Liked_DogSerializer
    def get_queryset(self):
        dog_id=self.kwargs['pk']
        return Liked_Dogs.objects.filter(dog__id=dog_id,active=True,liked=True)
    
    
    def perform_update(self,serializer):
        serializer.save(active=True)
        

        
    

            
        
        
    
        
    


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