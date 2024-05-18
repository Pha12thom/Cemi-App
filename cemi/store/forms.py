from .models import Store, items, Profile, cart 
from django import forms
from django.contrib.auth.models import User 


from django import forms

class OrderForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    delivery_address = forms.CharField(label='Delivery Address', widget=forms.Textarea)


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