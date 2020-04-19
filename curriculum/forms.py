from datetime import timedelta
import json
from django import forms
from django.urls import reverse
from .models import LessonPlan, WebsiteFeedback
from .util import int_or_false
from accounts.models import GradeLevels
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field

TIME_OPTIONS = (
    (timedelta(minutes=0), '0:00'),
    (timedelta(minutes=15), '0:15'),
    (timedelta(minutes=30), '0:30'),
    (timedelta(minutes=45), '0:45'),
    (timedelta(hours=1), '1:00'),
    (timedelta(hours=1, minutes=15), '1:15'),
    (timedelta(hours=1, minutes=30), '1:30'),
    (timedelta(hours=1, minutes=45), '1:45'),
    (timedelta(hours=2), '2:00'),
    (timedelta(hours=2, minutes=15), '2:15'),
    (timedelta(hours=2, minutes=30), '2:30'),
    (timedelta(hours=2, minutes=45), '2:45'),
    (timedelta(hours=3), '3:00'),
    (timedelta(hours=3, minutes=15), '3:15'),
    (timedelta(hours=3, minutes=30), '3:30'),
    (timedelta(hours=3, minutes=45), '3:45'),
    (timedelta(hours=4), '4:00'),
    (timedelta(hours=4, minutes=15), '4:15'),
    (timedelta(hours=4, minutes=30), '4:30'),
    (timedelta(hours=4, minutes=45), '4:45'),
    (timedelta(hours=5), '5:00'),
    (timedelta(hours=5, minutes=15), '5:15'),
    (timedelta(hours=5, minutes=30), '5:30'),
    (timedelta(hours=5, minutes=45), '5:45'),
    (timedelta(hours=6), '6:00'),
)

class LessonPlanForm(forms.ModelForm):
    resource_ids = forms.CharField(required=False, widget=forms.HiddenInput)
    filetypes = forms.CharField(required=False, widget=forms.HiddenInput)
    filenames = forms.CharField(required=False, widget=forms.HiddenInput)
    files = forms.FileField(required=False, widget=forms.HiddenInput)

    materials = forms.CharField(required=True, widget=forms.HiddenInput)

    total_prep_time = forms.ChoiceField(
        choices=TIME_OPTIONS,
        label='Total prep time (hh:mm)',
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
    single_class_time = forms.ChoiceField(
        choices=TIME_OPTIONS,
        label='Single class time (hh:mm)',
        widget=forms.Select(attrs={'class': 'custom-select'})
    )

    jsonResponse = forms.BooleanField(required=True, initial=False, widget=forms.HiddenInput)

    agree = forms.BooleanField(required=True, label="I am the sole author or I have permission to license this work under the CC BY-NC 4.0 license")

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
                Div(Field('draft'), css_class='col'),
                css_class='row'
            ),
            Div(Div(Field('agree'), css_class='col'), css_class='row'),
            Field('jsonResponse')
        )

    def clean_resource_ids(self):
        data = json.loads(self.cleaned_data['resource_ids'])
        return [int_or_false(num) for num in data]

    def clean_filetypes(self):
        return json.loads(self.cleaned_data['filetypes'])

    def clean_filenames(self):
        return json.loads(self.cleaned_data['filenames'])

    def clean_materials(self):
        return json.loads(self.cleaned_data['materials'])

    class Meta:
        model = LessonPlan
        fields = ['title', 'grade_level', 'num_classes', 'summary',
                  'total_prep_time', 'single_class_time',
                  'web_only', 'feedback_enabled',
                  'draft']
        widgets = {
            'summary': forms.Textarea(),
            'materials': forms.Textarea(attrs={'rows': 5})
        }


class LessonPlanFeedback(forms.Form):
    rating = forms.IntegerField(label="Rating (1-5)", min_value=1, max_value=5)
    comments = forms.CharField(max_length=2500, widget=forms.Textarea(attrs={'rows': 10, 'placeholder': "How did you use this curriculum?"}), label="Comments")
    #notify_author_of_changes = forms.BooleanField(required=False, label="Notify me if this lesson plan is updated", initial=True)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Review'))


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


SORT_BY_AVERAGE_RATING='AR'
SORT_BY_MOST_RECENTLY_MODIFIED='RM'
SORT_BY_NUMBER_OF_CLASSES='NC'
SORT_BY_SINGLE_CLASS_TIME='SC'
SORT_BY_TOTAL_PREP_TIME='TP'
SortByChoices=(
    (SORT_BY_AVERAGE_RATING, 'Average Rating'),
    (SORT_BY_MOST_RECENTLY_MODIFIED, 'Newest'),
    (SORT_BY_NUMBER_OF_CLASSES, 'Number of classes'),
    (SORT_BY_SINGLE_CLASS_TIME, 'Single class time'),
    (SORT_BY_TOTAL_PREP_TIME, 'Total prep time')
)

class LessonPlanAdvancedSearchForm(forms.Form):
    q = forms.CharField(required=False)
    sort_by = forms.ChoiceField(required=False, choices=SortByChoices, widget=forms.Select(attrs={'class': 'custom-select'}))
    grade_level = forms.MultipleChoiceField(required=False, choices=GradeLevels, widget=forms.CheckboxSelectMultiple)
    web_only = forms.BooleanField(required=False)
    user_id = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
