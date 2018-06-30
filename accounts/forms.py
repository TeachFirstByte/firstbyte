from django import forms
from allauth.account.forms import SignupForm
from . import models, fields


class UserRegistrationForm(SignupForm):
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
        label="Would you like to receive occasional updates from FirstByte?",
        required=True
    )

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2',
                   'school', 'grade_level', 'proficiency_description', 'wants_email']

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