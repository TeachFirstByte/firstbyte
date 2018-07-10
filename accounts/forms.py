from django import forms
from allauth.account import forms as account_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, Button, Submit, HTML
from . import models, fields


class UserRegistrationForm(account_forms.SignupForm):
    first_name = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': "First name"}))
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': "Last name"}))

    school = forms.CharField(
        label="Where do you teach?",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Name of school"})
    )
    grade_level = fields.EmptyChoiceField(
        required=False,
        empty_label="N/A",
        choices=models.GradeLevels
    )
    proficiency_description = fields.EmptyChoiceField(
        label="Which sentence best describes your proficiency level?",
        required=False,
        empty_label="I would rather not say",
        choices=models.TeacherProficiencies,
    )
    wants_email = forms.BooleanField(
        label="I want to receive occasional updates from FirstByte",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div('first_name', 'last_name', 'email', 'password1', 'password2', css_class='col'),
                Div('school', 'grade_level', 'proficiency_description', 'wants_email', css_class='col'),
                css_class='row'
            ),
            Div(
                Div(
                    Submit('submit', 'Create Account'),
                    css_class='col text-center'
                ),
                css_class='row'
            )
        )


    def save(self, request):
        user = super().save(request)

        user_profile = models.Profile(
            user=user,
            school=self.cleaned_data['school'],
            grade_level=self.cleaned_data['grade_level'],
            proficiency_description=self.cleaned_data['proficiency_description'],
            wants_email=self.cleaned_data['wants_email']
        )
        user_profile.save()

        return user


class LoginForm(account_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div('login', 'password'),
            Div(
                Div('remember', css_class='col'),
                HTML('<a class="col text-right" href="{% url \'account_reset_password\' %}">Forgot password?</a>'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Log in'),
                css_class='text-center'
            )
        )
