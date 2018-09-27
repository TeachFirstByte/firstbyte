import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.views.generic.list import ListView
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from . import forms, models, mixins
from bootstrap.mixins import FormBootstrapErrorListMixin
from bootstrap.errorlist import BootstrapErrorList

forbidden = {'err': 'forbidden' }
forbidden_status = 403
bad_request = {'err': 'bad_request' }
bad_request_status = 400

@login_required
def create_lesson_plan_view(request):
    if request.method == 'POST':
        form = forms.LessonPlanForm(request.POST, request.FILES)
        if form.is_valid():
            filetypes = form.cleaned_data['filetypes']
            filenames = form.cleaned_data['filenames']
            files = request.FILES.getlist('files[]')

            if len(filetypes) != len(filenames) or len(filetypes) != len(files):
                # BAD!
                return JsonResponse(bad_request, status=bad_request_status)

            # Create lesson plan
            lessonplan = form.save()
            lessonplan.owner = request.user

            # Create new files
            for index, file in enumerate(files):
                resource = models.LessonResource(
                    owner=lessonplan.owner,
                    semantic_type=filetypes[index],
                    name=filenames[index],
                    file=file)
                resource.save()
                lessonplan.resources.add(resource)

            lessonplan.save()
            if form.cleaned_data['jsonResponse']:
                return JsonResponse({'id': lessonplan.id})

            return redirect(lessonplan.get_absolute_url())

        return JsonResponse({
            'err': 'form invalid',
            'form_errors': dict(form.errors.items())
        }, status=bad_request_status)

    form = forms.LessonPlanForm()
    return render(request, 'curriculum/lessonplan_form.html', context={ 'form': form })

@login_required
def update_lesson_plan_view(request, pk):
    lessonplan = get_object_or_404(models.LessonPlan, id=pk)

    if lessonplan.owner != request.user and not request.user.is_superuser:
        # If someone owns a lesson plan they can modify resources that aren't theirs.
        # Is this an issue?
        if request.method == 'POST':
            return JsonResponse(forbidden, status=forbidden_status)
        else:
            return HttpResponseForbidden()

    if request.method == 'POST':
        form = forms.LessonPlanForm(request.POST, request.FILES, instance=lessonplan)
        if form.is_valid():
            resource_ids = form.cleaned_data['resource_ids']
            filetypes = form.cleaned_data['filetypes']
            filenames = form.cleaned_data['filenames']
            files = request.FILES.getlist('files[]')

            if len(filetypes) != len(filenames):
                # BAD!
                return JsonResponse(bad_request, status=bad_request_status)

            resources = []
            for index, id in enumerate(resource_ids):
                if id is not None:
                    resource = models.LessonResource.objects.get(id=id)
                    resource.semantic_type = filetypes[index]
                    resource.name = filenames[index]
                    resources.append(resource)
                else:
                    file = files.pop(0)
                    resource = models.LessonResource(
                        owner=lessonplan.owner,
                        semantic_type=filetypes[index],
                        name=filenames[index],
                        file=file
                    )
                    resources.append(resource)

            lessonplan = form.save()
            lessonplan.resources.clear()
            for resource in resources:
                lessonplan.resources.add(resource)
                resource.save()

            lessonplan.save()
            if form.cleaned_data['jsonResponse']:
                return JsonResponse({'id': lessonplan.id})

            return redirect(lessonplan.get_absolute_url())
    else:
        form = forms.LessonPlanForm(instance=lessonplan)

    return render(request, 'curriculum/lessonplan_form.html', context={'LESSON_PLAN_ID': pk, 'form': form })

class DeleteLessonPlanView(LoginRequiredMixin, mixins.MustOwnLessonPlanMixin, FormBootstrapErrorListMixin, DeleteView):
    success_url = reverse_lazy('list-lesson-plan')


def slug_redirect_view(klass, to=None, permanent=True, *args, **kwargs):
    def view_fn(request, pk):
        obj = get_object_or_404(klass, id=pk)
        return redirect(obj, *args, pk=pk, slug=obj.slug, permanent=permanent, **kwargs)
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
            'average_rating': self.lesson_plan.lessonfeedback_set.aggregate(rating=Avg('overall_rating')).get('rating')
        }

    def get_default_template_response(self, request, *args):
        response = TemplateResponse(request, template=self.template_name)
        response.context_data = self.get_context_data(request, *args)
        return response

    def get(self, request, **kwargs):
        obj = self.get_object()

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
                comments=form.cleaned_data['comments'],
                #notify_author_of_changes=form.cleaned_data['notify_author_of_changes']
            )
            feedback.save()

            # Clear the form, mark success
            form = forms.LessonPlanFeedback()

        return self.get_default_template_response(request, form)


@require_GET
def list_lessonplans(request):
    queryset = models.LessonPlan.objects.all()
    form = forms.LessonPlanAdvancedSearchForm(request.GET)

    show_advanced_search_options = False
    if not form.is_valid():
        form = forms.LessonPlanAdvancedSearchForm()

    if len(form.cleaned_data['grade_level']) != 0:
        queryset = queryset.filter(grade_level__in=form.cleaned_data['grade_level'])
        show_advanced_search_options = True

    if form.cleaned_data['web_only']:
        queryset = queryset.filter(web_only=form.cleaned_data['web_only'])
        show_advanced_search_options = True

    if form.cleaned_data['sort_by'] == forms.SORT_BY_MOST_RECENTLY_MODIFIED:
        queryset = queryset.order_by('-last_modified_time', 'title')
    elif form.cleaned_data['sort_by'] == forms.SORT_BY_NUMBER_OF_CLASSES:
        queryset = queryset.order_by('-num_classes', 'title')
    elif form.cleaned_data['sort_by'] == forms.SORT_BY_SINGLE_CLASS_TIME:
        queryset = queryset.order_by('-single_class_time', 'title')
    elif form.cleaned_data['sort_by'] == forms.SORT_BY_TOTAL_PREP_TIME:
        queryset = queryset.order_by('-total_prep_time', 'title')
    else: # SORT_BY_AVERAGE_RATING and none
        queryset = queryset.annotate(average_rating=Avg('lessonfeedback__overall_rating')).order_by('-average_rating', 'title')

    query = form.cleaned_data['q']
    if len(query) != 0:
        queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))

    restricted_user_id = form.cleaned_data.get('user_id')
    if restricted_user_id:
        queryset = queryset.filter(owner__id=restricted_user_id)
    else:
        queryset = queryset.filter(draft=False)

    return render(request, 'curriculum/lessonplan_list.html', {
        'user': request.user,
        'form': form,
        'show_advanced_search_options': show_advanced_search_options,
        'object_list': queryset
    })


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


def lesson_resource(request, pk):
    resource = get_object_or_404(models.LessonResource, id=pk)
    if request.method == 'GET':
        return HttpResponse(resource.file.chunks(), resource.mime_type)

    if request.user.is_authenticated and (resource.owner == request.user or request.user.is_superuser):
        if request.method == 'DELETE':
            resource.delete()
            return JsonResponse({'success': True})
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
