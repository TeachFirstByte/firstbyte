from django import forms
from django.urls import reverse
from .models import LessonPlan, WebsiteFeedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LessonPlanForm(forms.ModelForm):
    resources = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'lesson-plan-form'
        self.helper.form_method = 'post'

    def clean_resources(self):
        resources = self.cleaned_data['resources']
        if resources:
            return list([int(str_id) for str_id in resources.split(',')])
        else:
            return []

    class Meta:
        model = LessonPlan
        fields = ['title', 'grade_level', 'total_prep_time', 'num_classes',
                  'single_class_time', 'summary', 'materials', 'web_only', 'feedback_enabled',
                  'notify_of_feedback']


class LessonPlanFeedback(forms.Form):
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)
    success = forms.CharField(max_length=2500, widget=forms.Textarea, label="Successful parts")
    failure = forms.CharField(max_length=2500, widget=forms.Textarea, label="Unsuccessful parts")

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Feedback'))


class SubmitWebsiteFeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'text-center'
        self.helper.add_input(Submit('submit', 'Submit Feedback'))

    class Meta:
        model = WebsiteFeedback
        fields = ['overall_rating', 'strengths', 'weaknesses', 'email']


class MinimalLessonResource(forms.Form):
    file = forms.FileField()
