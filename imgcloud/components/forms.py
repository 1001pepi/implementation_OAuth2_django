from django import forms  
from django.contrib.auth.models import User  
from imgcloudAPI.models import Image

from django.forms import ModelForm

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  

from ..API_links import API_links
import requests
from django.contrib.auth.hashers import make_password

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(min_length=4, max_length=150, label="", widget=forms.TextInput(attrs={'placeholder':'username', 'class':'form-control', 'style': 'max-width: 300px;',}))
    password1 = forms.CharField(label = "", widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control',
        'style': 'max-width: 300px;',
    }))  
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
        'class':'form-control',
        'style': 'max-width: 300px;',
    }))  
  
    def clean_username(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("This username is already used!")  
        return username  
  
    def clean_password2(self): 
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:
            raise ValidationError("The passwords don't match!")
            
        return password2  
  
    def save(self, commit = True): 
        request_link = API_links.users_link

        payload={
            'username': self.cleaned_data['username'],
            'password': make_password(self.cleaned_data['password1']),
        }

        result = requests.post(request_link, data=payload)

        return result


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(min_length=4, max_length=150, label="", widget=forms.TextInput(attrs={'placeholder':'username', 'class':'form-control', 'style': 'max-width: 300px;',}))
    password = forms.CharField(label = "", widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control',
        'style': 'max-width: 300px;',
    })) 

class UploadImageForm(ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={
        'accept':'image/*',
    }))
    
    class Meta:
        model = Image
        fields = ['image']

   