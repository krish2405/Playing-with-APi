from django.shortcuts import render
from .models import Breed
from .serializer import BreedSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView


class AllDogsAV(APIView):
    def get(self,request):
        dogs=Breed.objects.all()
        serializer=BreedSerializer(dogs,many=True)
        return Response(serializer.data,status='200')
    

    def post(self,request):
        serializer=BreedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
class DogBYidAV(APIView):
    def get(self,request,pk):
        try:
            dog=Breed.objects.get(pk=pk)
        except Breed.DoesNotExist:
            return Response(status=404)
        
        serializer=BreedSerializer(dog)
        return Response(serializer.data,status=200)
    

    def put(self,request,pk):
        try:
            dog=Breed.objects.get(pk=pk)
        except Breed.DoesNotExist:
            return Response(status=404)
        serializer=BreedSerializer(instance=dog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status='200')
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        try:
            dog=Breed.objects.get(pk=pk)
        except Breed.DoesNotExist:
            return Response(status=404)
        serializer=BreedSerializer(dog)
        dog.delete()
        return Response(serializer.data, status=204)


##Using APIViewclass based views
# Create your views here.

# @api_view(['GET','POST'])
# def all_dogs(request):
#     if request.method=='POST':
#         serializer=BreedSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)
        
#     dogs=Breed.objects.all()
#     serializer=BreedSerializer(dogs,many=True)
#     return Response(serializer.data,status='200')


# @api_view(['GET','PUT','DELETE'])
# def user_by_id(request,pk):
#     try:
#         dog=Breed.objects.get(pk=pk)
#     except Breed.DoesNotExist:
#         return Response(status=404)
    
     
#     serializer=BreedSerializer(dog)
#     if request.method=='DELETE':
        
#         dog.delete()
#         return Response(serializer.data, status=204)
    
#     if request.method=='PUT':
#         serializer=BreedSerializer(instance=dog,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status='200')
#         return Response(serializer.errors,status='300')

    
    
#     return Response(serializer.data,status=200)