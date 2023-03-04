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
class filtrenceinteforms(forms.ModelForm):
    class Meta:
        model=Enceinte
        fields=('secteur','category','reso','nivo')
        ''' widgets={
            'secteur':forms.Select(attrs={'class':'col-3 form-control'}),
            'category':forms.Select(attrs={'class':'col-3 form-control'}),
            'reso':forms.Select(attrs={'class':' col-3 form-control'}),
            'nivo':forms.Select(attrs={'class':'col-3 form-control'}),
        } '''
    
class EnceinteForms(forms.ModelForm):
    class Meta:
        model=Enceinte
        fields=('secteur','category','reso','nivo','parent','nomEnceinte','adresse','contact1','contact2',)
        
class patientfiltreform(forms.Form):
    rechercher=forms.CharField(max_length=20,
                               label="",
                               widget=forms.TextInput(
                                attrs={
                                    'PlaceHolder':'rechercher le patient',
                                    'class':'form-control',
                                }))  
    
class Service(forms.ModelForm):
    class Meta:
        model=Servico
        fields=['enceinte','nomService','cautionAdminission']          