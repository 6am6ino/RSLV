from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Case


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CaseForm, self).__init__(*args, **kwargs)
        if user:
            # Automatically set the created_by field to the current user
            self.instance.created_by = user
