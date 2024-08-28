from rest_framework import serializers

from ..models import Activity


class ActivityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("uuid", "name", "time", "geo_json", "svg_points")
