from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.cars.views import CarsView, CarView, TariffView, CarLocationView,BrandsView
from apps.users.views import RegisterAPIView

urlpatterns=[
    path('', CarsView.as_view()),

    path('brands/',BrandsView.as_view()),
    path('<slug:slug>/',CarView.as_view()),
    path('<slug:slug>/tariff/',TariffView.as_view()),
    path('<slug:slug>/location',CarLocationView.as_view(), name='update-car-location')
    ]