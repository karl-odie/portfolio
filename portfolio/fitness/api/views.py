from uuid import UUID

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from .. import models
from . import serializers


class ActivityViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.ActivitySerializer
    queryset = models.Activity.objects.all()

    def get_queryset(self) -> QuerySet:
        return models.Activity.objects.filter(owner=self.request.user)

    @extend_schema(
        responses=serializers.ActivitySVGPointsSerializer(many=True),
    )
    @action(detail=True)
    def svg(self, request: HttpRequest, pk: UUID):
        activity = models.Activity.objects.get(uuid=pk)
        return Response(activity.svg_points_xy(height=100, width=100))

    @action(detail=True)
    def geo_json(self, request: HttpRequest, pk: UUID):
        activity = models.Activity.objects.get(uuid=pk)
        return Response(activity.geo_json())
