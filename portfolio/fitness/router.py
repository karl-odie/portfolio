from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r"activities", viewsets.ActivityViewSet, base_name="activity")
router.register(r"trimp", viewsets.TrimpViewSet, base_name="trimp")
