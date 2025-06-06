from django.shortcuts import render
from rest_framework.views import APIView
from apps.locations.serializers import LocationSerializer
from rest_framework.response import Response
from apps.cars.models import Car
from apps.locations.models import Location
from drf_spectacular.utils import extend_schema


# Create your views here.


tags=["Location"]

class LocationsView(APIView):
    serializer_class= LocationSerializer

    @extend_schema(
        summary="Get all locations",
        tags=tags
    )
    def get(self,request,*args,**kwargs):
       location = Location.objects.all()
       if location:
           serializer = self.serializer_class(location,many=True)
           return Response(serializer.data,status=200)
       return Response(data={"message":"No locations"})

    @extend_schema(
        summary="Create location",
        tags=tags
    )
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=201)
        return Response(serializer.errors,status=400)


class LocationViewDetail(APIView):
    serializer_class = LocationSerializer

    def get_object(self, request, *args, **kwargs, ):
        try:
            location = Location.objects.get_or_none(slug=kwargs["slug"])
            return location
        except Location.DoesNotExist:
            return Response(data={"message": "Location does not exist!"})

    @extend_schema(
        summary="Get location",
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        location = self.get_object( request, *args, **kwargs)
        if location:
            serializer = self.serializer_class(location)
            return Response(serializer.data, status=200)
        return Response(data={"message": "No such location"})


    @extend_schema(
        summary="Update location",
        tags=tags
    )

    def put(self,request,*args,**kwargs):
        location = self.get_object( request, *args, **kwargs)
        if not location:
            return Response(data={"message":"No location existing"})
        serializer = self.serializer_class(location,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=200)
        return Response(serializer.errors,status=400)


    @extend_schema(
        summary="Delete location",
        tags=tags
    )

    def delete(self,request,*args,**kwargs):
        location = self.get_object( request, *args, **kwargs)
        if not location:
            return Response(data={"message":"No such location"})
        location.delete()
        location.save()
        return Response(data={"message":"Location deleted successfully!"})

