from django.views.generic.edit import CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms, models


def index(request):
    return render(request, 'curriculum/index.html', {'user': request.user})


class CreateLessonPlanView(LoginRequiredMixin, CreateView):
    template_name = 'curriculum/lessonplan_new.html'
    form_class = forms.LessonPlanForm

    def get_success_url(self):
        return reverse('detail-lesson-plan', kwargs={'pk': self.object.pk })


class LessonPlanView(View):
    template_name = 'curriculum/lessonplan_detail.html'

    @property
    def lesson_plan(self):
        return models.LessonPlan.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, request, form=None, success=False):
        return {
            'lessonplan': self.lesson_plan,
            'form': form or forms.LessonPlanFeedback(),
            'user': request.user,
            'success': success,
        }

    def get_default_template_response(self, request, *args):
        response = TemplateResponse(request, template=self.template_name)
        response.context_data = self.get_context_data(request, *args)
        return response

    def get(self, request, **kwargs):
        return self.get_default_template_response(request)

    def post(self, request, **kwargs):
        form = forms.LessonPlanFeedback(request.POST)

        if not request.user.is_authenticated:
            # User must log in before posting
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        if not self.lesson_plan.feedback_enabled:
            form.add_error(None, 'Feedback not allowed on this object')
            return self.get_default_template_response(request, form)

        if form.is_valid():
            feedback = models.LessonFeedback.objects.create(
                lesson=self.lesson_plan,
                author=request.user,
                overall_rating=form.cleaned_data['rating'],
                strengths=form.cleaned_data['success'],
                weaknesses=form.cleaned_data['failure']
            )
            feedback.save()

            # Clear the form, mark success
            form = forms.LessonPlanFeedback()

        return self.get_default_template_response(request, form)
