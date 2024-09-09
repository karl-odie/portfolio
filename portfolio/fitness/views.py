from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from . import models


class UserActivityMixin(LoginRequiredMixin):
    model = models.Activity

    def get_queryset(self):
        return models.Activity.objects.filter(owner=self.request.user)


class ActivityList(UserActivityMixin, ListView):
    template_name = "fitness/list.html"


class ActivityDetail(UserActivityMixin, DetailView):
    template_name = "fitness/detail.html"


class ActivitySVG(UserActivityMixin, DetailView):
    template_name = "fitness/activity.svg"
