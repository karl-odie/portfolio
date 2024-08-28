from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from . import models


class UserActivityMixin(LoginRequiredMixin):
    model = models.Activity

    def get_queryset(self):
        return models.Activity.objects.filter(owner=self.request.user)


class ActivityList(UserActivityMixin, ListView):
    template_name = "fitness/activity_list.html"
    paginate_by = 30


class ActivityDetail(UserActivityMixin, DetailView):
    template_name = "fitness/activity_detail.html"


class ActivitySVG(UserActivityMixin, DetailView):
    template_name = "fitness/activity.svg"
