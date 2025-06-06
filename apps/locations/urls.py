from django.urls import path
from apps.locations.views import LocationsView,LocationViewDetail

urlpatterns =[
    path('' ,LocationsView.as_view()),
    path('<slug:slug>/',LocationViewDetail.as_view())
    ]