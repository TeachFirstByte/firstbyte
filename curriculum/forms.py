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
    ('0:00', '0:00'),
    ('0:15', '0:15'),
    ('0:30', '0:30'),
    ('0:45', '0:45'),
    ('1:00', '1:00'),
    ('1:15', '1:15'),
    ('1:30', '1:30'),
    ('1:45', '1:45'),
    ('2:00', '2:00'),
    ('2:15', '2:15'),
    ('2:30', '2:30'),
    ('2:45', '2:45'),
    ('3:00', '3:00'),
    ('3:15', '3:15'),
    ('3:30', '3:30'),
    ('3:45', '3:45'),
    ('4:00', '4:00'),
    ('4:15', '4:15'),
    ('4:30', '4:30'),
    ('4:45', '4:45'),
    ('5:00', '5:00'),
    ('5:15', '5:15'),
    ('5:30', '5:30'),
    ('5:45', '5:45'),
    ('6:00', '6:00'),
)

def parse_timedelta(value):
    parts = value.split(':')
    return timedelta(hours=int(parts[0]), minutes=int(parts[1]))

class LessonPlanForm(forms.ModelForm):
    resource_ids = forms.CharField(required=False, widget=forms.HiddenInput)
    filetypes = forms.CharField(required=False, widget=forms.HiddenInput)
    filenames = forms.CharField(required=False, widget=forms.HiddenInput)
    files = forms.FileField(required=False, widget=forms.HiddenInput)

    materials = forms.CharField(required=True, widget=forms.HiddenInput)

    total_prep_time = forms.ChoiceField(
        choices=TIME_OPTIONS,
    )
    single_class_time = forms.ChoiceField(
        choices=TIME_OPTIONS,
    )

    jsonResponse = forms.BooleanField(required=True, initial=False, widget=forms.HiddenInput)

    agree = forms.BooleanField(required=True)

    def clean_resource_ids(self):
        data = json.loads(self.cleaned_data['resource_ids'])
        return [int_or_false(num) for num in data]

    def clean_filetypes(self):
        return json.loads(self.cleaned_data['filetypes'])

    def clean_filenames(self):
        return json.loads(self.cleaned_data['filenames'])

    def clean_total_prep_time(self):
        return parse_timedelta(self.cleaned_data['total_prep_time'])

    def clean_single_class_time(self):
        return parse_timedelta(self.cleaned_data['single_class_time'])

    def clean_materials(self):
        return json.loads(self.cleaned_data['materials'])

    class Meta:
        model = LessonPlan
        fields = ['title', 'grade_level', 'num_classes', 'summary',
                  'total_prep_time', 'single_class_time',
                  'web_only', 'feedback_enabled',
                  'draft']


class MinimalLessonResource(forms.Form):
    file = forms.FileField()


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
