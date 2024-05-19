from .models import Store, items, Profile, cart
from django import forms
from django.contrib.auth.models import User

class OrderForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your email'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your phone number'})
    )
    delivery_address = forms.CharField(
        label='Delivery Address',
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your delivery address', 'rows': 3})
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)



class LogoutForm(forms.Form):
    pass


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user']

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'phone_number', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter your address'}),
        }