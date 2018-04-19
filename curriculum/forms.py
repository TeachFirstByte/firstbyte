from django import forms
from .models import LessonPlan


class LessonPlanForm(forms.ModelForm):

    class Meta:
        model = LessonPlan
        fields = ['title', 'grade_level', 'prep_time',
                  'class_time', 'summary', 'materials',]
