from django.urls import path

from . import views

app_name = "fitness"
urlpatterns = [
    path("list/", views.ActivityList.as_view(), name="activity_list"),
    path("activity/<pk>/", views.ActivityDetail.as_view(), name="activity"),
    path("activity_svg/<pk>.svg", views.ActivitySVG.as_view(), name="activity_svg"),
]
