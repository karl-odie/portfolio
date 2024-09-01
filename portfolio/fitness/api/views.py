from uuid import UUID

from django.http.request import HttpRequest
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .. import models
from . import serializers


class ActivityViewSet(viewsets.ViewSet):
    def list(self, request: HttpRequest):
        query = models.Activity.objects.filter(owner=request.user)
        serializer = serializers.ActivityListSerializer(query, many=True)
        return Response(serializer.data)

    def retrieve(self, request: HttpRequest, pk: UUID):
        activity = models.Activity.objects.get(uuid=pk)
        serializer = serializers.ActivityDetailSerializer(activity)
        return Response(serializer.data)

    @action(detail=True)
    def svg(self, request: HttpRequest, pk: UUID):
        activity = models.Activity.objects.get(uuid=pk)
        return Response(activity.svg_points())

    @action(detail=True)
    def geo_json(self, request: HttpRequest, pk: UUID):
        activity = models.Activity.objects.get(uuid=pk)
        return Response(activity.geo_json())
