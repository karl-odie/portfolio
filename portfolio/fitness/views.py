from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from . import forms
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


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = "fitness/activity_upload.html"


class TrimpView(LoginRequiredMixin, TemplateView):
    template_name = "fitness/trimp.html"


class ControlPanelView(LoginRequiredMixin, View):
    template_name = "fitness/control_panel.html"

    def get(self, request, *args, **kwargs):
        user_form = forms.UserForm(
            initial={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "email": self.request.user.email,
            },
        )
        profile_form = forms.ProfileForm(
            initial={
                "theme": self.request.user.profile.theme,
                "gender": self.request.user.profile.gender,
            },
        )
        heart_form = forms.HeartRateForm(
            initial={
                "minimum_heart_rate": self.request.user.profile.minimum_heart_rate,
                "maximum_heart_rate": self.request.user.profile.maximum_heart_rate,
            },
        )
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "heart_form": heart_form,
                "view": self,
            },
        )

    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)
        heart_form = forms.HeartRateForm(request.POST)
        if all(a.is_valid() for a in (user_form, profile_form, heart_form)):
            for key, value in user_form.cleaned_data.items():
                setattr(self.request.user, key, value)
            for key, value in profile_form.cleaned_data.items():
                setattr(self.request.user.profile, key, value)
            for key, value in heart_form.cleaned_data.items():
                setattr(self.request.user.profile, key, value)
            self.request.user.save()
            self.request.user.profile.save()
        return self.get(request, *args, **kwargs)


class RecalculateTRIMPView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        activity = models.Activity.objects.filter(owner=request.user, id=pk).first()
        if activity:
            activity.trimp = activity.calculate_trimp()
            activity.save()
        return HttpResponse("Done")
