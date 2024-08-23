from django.urls import path

from . import views

app_name = "fitness"
urlpatterns = [
    path("control_panel/", views.ControlPanelView.as_view(), name="control_panel"),
    path("trimp/", views.TrimpView.as_view(), name="render_trimp"),
    path("list/", views.ActivityList.as_view(), name="activity_list"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("activity/<pk>/", views.ActivityDetail.as_view(), name="activity"),
    path("recalculate/<pk>/", views.RecalculateTRIMPView.as_view(), name="recalculate"),
    path("activity_svg/<pk>).svg", views.ActivitySVG.as_view(), name="activity_svg"),
]
