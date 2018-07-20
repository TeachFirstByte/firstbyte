from django import forms
from django.urls import reverse
from .models import LessonPlan, WebsiteFeedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field

class LessonPlanForm(forms.ModelForm):
    resources = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'lesson-plan-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(Div(Field('title'), css_class='col'), css_class='row'),
            Div(Div(Field('summary'), css_class='col'), css_class='row'),
            Div(
                Div(Field('grade_level'), css_class='col'),
                Div(Field('total_prep_time'), css_class='col'),
                css_class='row'
            ),
            Div(
                Div(Field('single_class_time'), css_class='col'),
                Div(Field('num_classes'), css_class='col'),
                css_class='row'
            ),
            Div(Div(Field('materials'), css_class='col'), css_class='row'),
            Div(
                Div(Field('web_only'), css_class='col'),
                Div(Field('feedback_enabled'), css_class='col'),
                Div(Field('notify_of_feedback'), css_class='col'),
                Div(Field('draft'), css_class='col'),
                css_class='row'
            )
        )

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
                  'notify_of_feedback', 'draft']


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
