from .models import LessonPlan
from django.shortcuts import get_object_or_404

def must_own_lesson_plan_or_none(klass, *args, **kwargs):
    obj = get_object_or_404(klass, *args, **kwargs)
    if obj.owner == request.user or request.user.is_superuser:
        return obj
    return None
