from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, reverse

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import models
from .serializers import LessonPlanSerializer

def get_lessonplan(request, pk):
    """Return a JSON description object for some LessonPlan."""

    if not request.user.is_authenticated:
        return JsonResponse({
            'err': 'api access is restricted to authenticated users'
        }, status=403)

    lessonplan = get_object_or_404(models.LessonPlan, id=pk)

    include_resources = request.GET.get('include_resources', True)
    include_feedback = request.GET.get('include_feedback', False)

    res = {
        'owner': lessonplan.owner.id,
        'title': lessonplan.title,
        'grade_level': lessonplan.grade_level,
        'total_prep_time': lessonplan.total_prep_time,
        'num_classes': lessonplan.num_classes,
        'single_class_time': lessonplan.single_class_time,
        'summary': lessonplan.summary,
        'materials': lessonplan.materials,
        'web_only': lessonplan.web_only,
        'feedback_enabled': lessonplan.feedback_enabled,
        # 'notify_of_feedback': lessonplan.notify_of_feedback,
        'draft': lessonplan.draft,
        'last_modified_time': lessonplan.last_modified_time,
        'create_time': lessonplan.create_time,
    }
    if include_resources:
        resources = []
        for resource in lessonplan.resources.all():
            resources.append({
                'id': resource.id,
                'name': resource.name,
                'mime_type': resource.mime_type,
                'semantic_type': resource.semantic_type,
                'url': reverse('detail-lesson-resource', kwargs={'pk': resource.id}),
                'create_time': resource.create_time,
            })
        res['resources'] = resources

    if include_feedback:
        feedbacks = []
        for feedback in lessonplan.feedback_set:
            feedbacks.append({
                'author': feedback.author.id,
                # 'notify_author_of_changes': feedback.notify_author_of_changes,
                'overall_rating': feedback.overall_rating,
                'comments': feedback.comments,
                'create_time': feedback.create_time,
            })
        res['feedbacks'] = feedbacks

    return JsonResponse(res)


class LessonPlanViewSet(ModelViewSet):
    queryset = models.LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }
