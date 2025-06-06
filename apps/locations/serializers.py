from rest_framework import serializers
from apps.locations.models import Location



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ["is_deleted","deleted_at"]


