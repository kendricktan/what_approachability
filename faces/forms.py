from django import forms
from models import *

class DetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = tandaAccount
        fields = '__all__'
