from django.shortcuts import render
from .models import Breed
from .serializer import BreedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET','POST'])
def all_dogs(request):
    if request.method=='POST':
        serializer=BreedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
        
    dogs=Breed.objects.all()
    serializer=BreedSerializer(dogs,many=True)
    return Response(serializer.data,status='200')


@api_view(['GET','PUT','DELETE'])
def user_by_id(request,pk):
    try:
        dog=Breed.objects.get(pk=pk)
    except Breed.DoesNotExist:
        return Response(status=404)
    
     
    serializer=BreedSerializer(dog)
    if request.method=='DELETE':
        
        dog.delete()
        return Response(serializer.data, status=204)
    
    if request.method=='PUT':
        serializer=BreedSerializer(instance=dog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status='200')
        return Response(serializer.errors,status='300')

    
    
    return Response(serializer.data,status=200)