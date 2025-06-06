from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.rentals.serializers import RentalsSerializer
from apps.users.models import User
from apps.rentals.models import Rentals
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import MyTokenObtainPairSerializer, CreateUserSerializer, UserSerializer, ProfileSerializer

# Create your views here.

tags=['User']

class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"success"},status=201)
        return Response(serializer.errors,status=400)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="My info",
        tags=tags,
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)



class UserMeRentalsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RentalsSerializer

    @extend_schema(
        summary="Get my rentals",
        tags=tags
    )
    def get(self,request,*args,**kwargs):
        user = request.user
        rentals = Rentals.objects.filter(user=user).all()
        serializer = self.serializer_class(rentals,many=True)
        if not serializer.data:
            return Response(data={"message":"No rentals for this user!"})
        return Response(serializer.data,status=200)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Edit profile",
        tags=tags
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=200)
        return Response(serializer.errors,status=400)