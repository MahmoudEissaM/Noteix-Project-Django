from django import forms
from .models import Note, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'link', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'content': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 4}),
            'link': forms.URLInput(attrs={'class': 'form-control bg-dark text-white'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=Note.CATEGORY_CHOICES),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}),
        }

class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}))
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark text-white'})
        }

from django.contrib.auth.forms import PasswordChangeForm
class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
