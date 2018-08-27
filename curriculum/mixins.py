from .models import LessonPlan
from django.http import HttpResponseForbidden

class MustOwnLessonPlanMixin(object):
    model = LessonPlan
    def dispatch(self, request, *args, **kwargs):
        if super().get_object().owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Not allowed!")