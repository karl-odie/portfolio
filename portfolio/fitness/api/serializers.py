from rest_framework import serializers

from ..models import Activity


class ActivityDetailSerializer(serializers.ModelSerializer):
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
            "geo_json",
            "svg_points",
        )


class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("uuid", "name", "time", "distance", "duration", "elevation")
        read_only_fields = fields
        model = Activity


class AcvititySVGSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("uuid", "svg_points")
        read_only_fields = fields
        model = Activity


class AcvitityGeoJSONSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("uuid", "geo_json")
        read_only_fields = fields
        model = Activity
