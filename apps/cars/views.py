from django.db.models import prefetch_related_objects
from django.shortcuts import render
from django.template.context_processors import request
from drf_spectacular.utils import extend_schema,OpenApiTypes,OpenApiParameter
from jsonschema.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.serializers import as_serializer_error
from yaml import serialize
from apps.locations.models import Location
from apps.cars.models import Car,Brand
from rest_framework.views import APIView
from apps.cars.serializers import CarsSerializer, TariffSerializer, ChangeCarLocation,BrandSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

tags=["Cars"]


class CarsView(APIView):

    serializer_class = CarsSerializer

    @extend_schema(
        summary="Listing",
        description="This endpoint returns list of all cars. Cars could be fitered by body,color,price",
        tags=tags,
        parameters=[
            OpenApiParameter(
                name="brand",
                description="Filter cars by brand",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="color",
                description="Filter cars by color",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="year_min",
                description="Filter cars by min year",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="year_max",
                description="Filter cars by max year",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="price_max",
                description="Filter cars by max year",
                required=False,
                type=OpenApiTypes.DOUBLE,
            ),
            OpenApiParameter(
                name="price_min",
                description="Filter cars by max year",
                required=False,
                type=OpenApiTypes.DOUBLE,
            ),
        ]
    )
    def get(self,request,*args,**kwargs):
        brand = request.GET.get('brand')
        if brand:
            brand = Brand.objects.get_or_none(slug=brand)
            queryset= Car.objects.select_related('brand','tariff_plan','current_location').filter(brand=brand)
            if not queryset:
                return Response(data={"mesage":"No cars for this brand"})
        else:
            queryset = Car.objects.all()
        color = request.GET.get('color')

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        year_min = self.request.query_params.get('year_min')
        year_max = self.request.query_params.get('year_max')


        if color:
            queryset = queryset.filter(color__iexact=color)
        if price_min:
            queryset = queryset.filter(tariff_plan__price_per_day__gte=price_min)
        if price_max:
            queryset = queryset.filter(tariff_plan__price_per_day__lte=price_max)
        if year_min:
            queryset = queryset.filter(year_released__gte=year_min)
        if year_max:
            queryset = queryset.filter(year_released__lte=year_max)

        serializer = self.serializer_class(queryset,many=True)
        if not serializer.data:
            return Response(status=204)
        return Response(serializer.data,status=200)
        # serializer = self.serializer_class(cars, many=True)
        # if not serializer.data:
        #     return Response(data={"message": "No cars!"})
        # return Response(serializer.data, status=200)



    @extend_schema(
        summary="Creating",
        description="This endpoint creates new car",
        tags=tags,

    )
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=201)
        else:
            return Response(serializer.errors)



class CarView(APIView):
    serializer_class = CarsSerializer

    def get_object(self,request,*args,**kwargs,):
        try:
            car = Car.objects.get_or_none(slug=kwargs["slug"])
            return car
        except car.DoesNotExist:
            return Response(data={"message": "Car does not exist!"})

    @extend_schema(
        summary="Detail info about car",
        tags=tags
    )
    def get(self,request,*args,**kwargs):
        car = self.get_object(request,*args,**kwargs)
        if car:
            serializer = self.serializer_class(car)
            return Response(serializer.data,status=200)
        return Response(data={"message": "No such car"})

    @extend_schema(
        summary="Partial updating",
        description="This endpoint partially updates car",
        tags=tags,
    )
    def put(self,request,*args,**kwargs):
        car = self.get_object(self,request,*args,**kwargs)
        serializer = self.serializer_class(car,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=200)
        return Response(serializer.errors,status=400)

    @extend_schema(
        summary="Deleting car",
        description="This endpoint delete car",
        tags=tags,
    )
    def delete(self,request,*args,**kwargs):
        car = self.get_object(request,*args,**kwargs)
        car.delete()
        car.save()
        return Response(data={"message":"car has been deleted"})



class TariffView(APIView):
    serializer_class = TariffSerializer

    def get_object(self,request,*args,**kwargs,):
        try:
            car = Car.objects.get_or_none(slug=kwargs["slug"])
            return car
        except car.DoesNotExist:
            return Response(data={"message": "Car does not exist!"})


    @extend_schema(
        summary="Create Tariff",
        description="This endpoint creates tariff and add it to existing car",
        tags=tags
    )
    def post(self,request,*args,**kwargs):
        car = self.get_object(request,*args,**kwargs)
        if car:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                tariff = serializer.save()
                car.tariff_plan = tariff
                car.save()
                return Response(serializer.validated_data,status=200)
            return Response(serializer.errors,status=400)
        return Response(data={"message":"No such car!"})

    @extend_schema(
        summary="Update Tariff",
        tags=tags
    )
    def put(self,request,*args,**kwargs):
        car = self.get_object(request,*args,**kwargs)
        if car:
            tariff = car.tariff_plan
            if not tariff:
                return Response(data={"message":"No tariff plan existing"})
            serializer = self.serializer_class(tariff,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data,status=200)
            return Response(serializer.errors,status=400)

class CarLocationView(APIView):
    serializer_class = ChangeCarLocation

    @extend_schema(
        summary="Edit car location",
        description="This endpoint changes car location that already exists",
        tags=tags,
    )
    def patch(self, request, *args,**kwargs):
        car = Car.objects.get_or_none (slug=kwargs["slug"])
        location_slug = request.data.get("location_slug")

        if not location_slug:
            return Response({"error": "location_slug is required"}, status=400)

        location = Location.objects.get_or_none(slug=location_slug)
        if not location:
            return Response(data={"message":"No such location"})
        car.current_location = location
        car.save()

        return Response({"message": "Location updated!"}, status=200)

class BrandsView(APIView):
    serializer_class = BrandSerializer

    @extend_schema(
        summary="Fetch cars brands",
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        serializer = self.serializer_class(brands,many=True)
        return Response(serializer.data)