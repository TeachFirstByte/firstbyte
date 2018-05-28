from django import forms
from allauth.account.forms import SignupForm


class UserRegistrationForm(SignupForm):
    first_name = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': "First name"}))
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': "Last name"}))

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']
