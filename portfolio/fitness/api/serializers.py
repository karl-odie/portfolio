from rest_framework import serializers

from ..models import Activity
from ..models import Biometrics


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "uuid",
            "owner",
            "name",
            "time",
            "distance",
            "duration",
            "elevation",
            "trimp",
        )
        read_only_fields = fields


class ActivitySVGSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("uuid", "svg_points")
        read_only_fields = fields
        model = Activity


class ActivitySVGPointsSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class ActivityGEOJSONSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("uuid", "geo_json")
        read_only_fields = fields
        model = Activity


class BiometricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometrics
        fields = (
            "heart_rate",
            "cadence",
            "time",
            "latitude",
            "longitude",
            "altitude",
        )

    heart_rate = serializers.IntegerField(read_only=True, allow_null=True)
    cadence = serializers.IntegerField(read_only=True, allow_null=True)
    time = serializers.DateTimeField(source="point.time", read_only=True)
    latitude = serializers.FloatField(source="point.latitude", read_only=True)
    longitude = serializers.FloatField(source="point.longitude", read_only=True)
    altitude = serializers.FloatField(source="point.altitude", read_only=True)
