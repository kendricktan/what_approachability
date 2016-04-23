from django import forms
from models import *

class DetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = tandaAccount
        fields = '__all__'
        #widgets = {
        #    'email': forms.TextInput(attrs={'placeholder': 'email'}), 
        #    'password': forms.PasswordInput(attrs={'placeholder': 'password'}), 
        #}

class URLForm(forms.ModelForm):
    class Meta:
        model = customURL
        fields = '__all__'
