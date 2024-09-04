from rest_framework import serializers

from ..models import Activity


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
