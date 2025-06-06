
from rest_framework import serializers
from apps.rentals.models import Rentals
from apps.cars.serializers import CarsSerializer

class RentalsSerializer(serializers.ModelSerializer):
    car = CarsSerializer()
    class Meta:
        model = Rentals
        fields ="__all__"
        read_only_fields =["deleted_at","is_deleted"]