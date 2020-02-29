from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username   

    def clean_email(self):
        email = self.cleaned_data['email']
        r = User.objects.filter(email__iexact=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email       

class ProfileBioEditForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 27, 'rows': 7}), max_length=400)
    class Meta:
        model = Profile
        fields = ['bio',]       

class ProfilePicEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']       