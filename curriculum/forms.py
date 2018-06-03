from django import forms
from .models import LessonPlan


class LessonPlanForm(forms.ModelForm):

    class Meta:
        model = LessonPlan
        fields = ['title', 'grade_level', 'prep_time',
                  'class_time', 'summary', 'materials', 'web_only', 'feedback_enabled',
                  'notify_of_feedback']


class LessonPlanFeedback(forms.Form):
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)
    success = forms.CharField(max_length=2500, widget=forms.Textarea, label="Successful parts")
    failure = forms.CharField(max_length=2500, widget=forms.Textarea, label="Unsuccessful parts")
