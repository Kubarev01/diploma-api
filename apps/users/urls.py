from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.users.views import RegisterAPIView, MyTokenObtainPairView, UserMeView, UserMeRentalsView, ProfileView

urlpatterns = [
    path('', RegisterAPIView.as_view(),name="registration"),
    path('token/',MyTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('token/verify/',TokenVerifyView.as_view(),name='token_verify'),
    path("me/",UserMeView.as_view(),name="user_info"),
    path("me/rentals",UserMeRentalsView.as_view(),name="user_rentals"),
    path("me/profile",ProfileView.as_view(),name="user_profile")
]
