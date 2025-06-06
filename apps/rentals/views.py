from django.shortcuts import render
from rest_framework import generics
from apps.rentals.models import Rentals
from .serializers import RentalsSerializer



class RentalListCreateView(generics.ListCreateAPIView):
    queryset = Rentals.objects.all()
    serializer_class = RentalsSerializer

class RentalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rentals.objects.all()
    serializer_class = RentalsSerializer
    lookup_field = 'pk'