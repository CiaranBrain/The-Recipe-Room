from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'aria-label': 'Username'  # For accessibility
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'aria-label': 'Password'  # For accessibility
        })
    )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']