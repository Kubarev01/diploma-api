from rest_framework import serializers
from apps.cars.models import Car,TariffPlan,Brand
from apps.locations.serializers import LocationSerializer
import  datetime

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields ="__all__"

class ChangeCarLocation(serializers.Serializer):
    location_slug = serializers.CharField(max_length=50)

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffPlan
        fields = "__all__"
        read_only_fields = ["is_deleted", "deleted_at"]

class CarsSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(read_only=True)
    tariff_plan = TariffSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ["is_deleted","deleted_at"]

    def validate_year_released(self, value):
        current_year = datetime.now().year
        if value < 1886 or value > current_year + 1:  # первый автомобиль = 1886
            raise serializers.ValidationError("Введите корректный год выпуска")
        return value

