from django import forms
from .models import *
from django.contrib.auth import login,logout,authenticate


class ConnexionForms(forms.Form): 
    telephone=forms.CharField(max_length=9)
    password=forms.CharField(required=True,widget=forms.PasswordInput)   
    
    def clean_telephone(self):
        telephone=self.cleaned_data.get('telephone')
        if len(telephone)!=9:
            raise forms.ValidationError("le numero de telephone doit avoir 9 chiffres") 
        return telephone    
    
