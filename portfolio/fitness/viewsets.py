from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from . import models
from . import serializers


class ActivityViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet,
):
    def get_queryset(self):
        return models.Activity.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        return {
            "retrieve": serializers.ActivityDetailSerializer,
            "create": serializers.RunSerializer,
        }.get(self.action) or serializers.ActivityListSerializer


class TrimpViewSet(viewsets.ViewSet):
    queryset = models.Activity.objects.all()

    def list(self, request):
        serializer = serializers.TrimpSerializer(
            models.TrainingStressBalance.history_for_user(self.request.user),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
