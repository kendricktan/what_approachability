from django import forms
from models import *

class DetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = tandaAccount
        fields = '__all__'

class URLForm(forms.ModelForm):
    class Meta:
        model = customURL
        fields = '__all__'
