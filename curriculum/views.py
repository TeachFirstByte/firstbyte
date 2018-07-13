import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.views.generic.list import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from . import forms, models
from .errorlist import BootstrapErrorList, FormBootstrapErrorListMixin


class CreateLessonPlanView(LoginRequiredMixin, FormBootstrapErrorListMixin, CreateView):
    template_name = 'curriculum/lessonplan_form.html'
    form_class = forms.LessonPlanForm

    def __init__(self):
        self.object = None;
        super().__init__()

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user

        for resource_id in form.cleaned_data['resources']:
            self.object.resources.add(models.LessonResource.objects.get(pk=resource_id))

        self.object.save()
        # Don't let ModelFormMixin save the object
        return FormView.form_valid(self, form)


class MustOwnLessonPlanMixin(object):
    model = models.LessonPlan
    def dispatch(self, request, *args, **kwargs):
        if super().get_object().owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Not allowed!")


class UpdateLessonPlanView(LoginRequiredMixin, MustOwnLessonPlanMixin, FormBootstrapErrorListMixin, UpdateView):
    form_class = forms.LessonPlanForm


class DeleteLessonPlanView(LoginRequiredMixin, MustOwnLessonPlanMixin, FormBootstrapErrorListMixin, DeleteView):
    success_url = reverse_lazy('list-lesson-plan')


def slug_redirect_view(klass, to=None, permanent=True, *args, **kwargs):
    def view_fn(request, pk):
        obj = get_object_or_404(klass, id=pk)
        target = to or klass
        return redirect(target, *args, pk=pk, slug=obj.slug, permanent=permanent, **kwargs)
    return view_fn

class LessonPlanView(View):
    template_name = 'curriculum/lessonplan_detail.html'

    @property
    def lesson_plan(self):
        return models.LessonPlan.objects.get(id=self.kwargs['pk'])

    def get_object(self):
        return self.lesson_plan

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
        obj = self.get_object()

        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        if slug != obj.slug:
            # Replace old slug with correct one
            return redirect(obj.get_absolute_url(), permanent=True)

        return self.get_default_template_response(request)

    def post(self, request, **kwargs):
        form = forms.LessonPlanFeedback(request.POST, error_class=BootstrapErrorList)

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


class LessonPlanUserList(ListView):
    model = models.LessonPlan

    def get_queryset(self):
        return models.LessonPlan.objects.filter(owner=self.kwargs['pk'])


class SubmitWebsiteFeedbackView(FormBootstrapErrorListMixin, CreateView):
    model = models.WebsiteFeedback
    form_class = forms.SubmitWebsiteFeedbackForm
    success_url = reverse_lazy('website-feedback-done')


def website_feedback_done(request):
    return render(request, 'curriculum/websitefeedback_done.html')


@require_POST
@login_required
def create_lesson_resource(request):
    form = forms.MinimalLessonResource(request.POST, request.FILES)
    if form.is_valid():
        # TODO: Verify the file is not malicious
        uploaded_file = form.cleaned_data['file']
        lesson_resource = models.LessonResource(
            name=uploaded_file.name,
            file=uploaded_file,
            mime_type=uploaded_file.content_type,
            owner=request.user
        )
        lesson_resource.save()
        return JsonResponse({'id': lesson_resource.id})
    return JsonResponse({'err': True})


@login_required
def lesson_resource(request, pk):
    resource = get_object_or_404(models.LessonResource, id=pk)
    if request.method == 'DELETE':
        if resource.owner == request.user:
            resource.delete()
            return JsonResponse({'success': True})
    elif request.method == 'GET':
        return HttpResponse(resource.file.chunks(), resource.mime_type)
    elif request.method == 'PUT':
        patch = json.loads(request.body)

        try:
            resource.name = str(patch['name'])
            resource.semantic_type = patch['type']
        except KeyError:
            return JsonResponse({'err': True}, status=422)

        resource.save()
        return JsonResponse({'success': True})

    return HttpResponseForbidden()
