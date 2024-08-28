from rest_framework import viewsets

from .. import models
from . import serializers


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActivityDetailSerializer

    def get_queryset(self):
        return models.Activity.objects.filter(owner=self.request.user)
