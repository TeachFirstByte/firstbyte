from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from . import forms, models


class CreateLessonPlanView(LoginRequiredMixin, CreateView):
    template_name = 'curriculum/lessonplan_new.html'
    form_class = forms.LessonPlanForm

    def get_success_url(self):
        return reverse('detail-lesson-plan', kwargs={'pk': self.object.pk })


class LessonPlanView(DetailView):
    model = models.LessonPlan
    template_name = 'curriculum/lessonplan_detail.html'


class LessonPlanList(ListView):
    model = models.LessonPlan
