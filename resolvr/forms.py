from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Case, Arbitrator, Customer
from .models import CustomUser

class ArbitratorForm(forms.ModelForm):
    """Form for registering an arbitrator."""

    class Meta:
        model = Arbitrator
        fields = ['user', 'qualifications', 'experience', 'certification', 'certification_file']

    def __init__(self, *args, **kwargs):
        super(ArbitratorForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = "User Account"  # Custom label for clarity


class CustomerForm(forms.ModelForm):
    """Form for registering a customer."""

    class Meta:
        model = Customer
        fields = ['user']  # Link to the User model instead of having separate username and email

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = "User Account"  # Custom label for clarity


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser  # Use CustomUser here
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class CaseForm(forms.ModelForm):
    """Form for creating or updating a case."""

    class Meta:
        model = Case
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CaseForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.created_by = user  # Automatically set created_by field to current user

    def clean(self):
        """Custom validation can be added here if needed."""
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if not title:
            raise forms.ValidationError("Title is required.")
