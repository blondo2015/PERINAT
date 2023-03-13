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
        fields=('secteur','categorie','reseau','niveau')
        ''' widgets={
            'secteur':forms.Select(attrs={'class':'col-3 form-control'}),
            'category':forms.Select(attrs={'class':'col-3 form-control'}),
            'reso':forms.Select(attrs={'class':' col-3 form-control'}),
            'nivo':forms.Select(attrs={'class':'col-3 form-control'}),
        } '''
    
class EnceinteForms(forms.ModelForm):   
    code=forms.CharField(label=" code de l'enceinte")
    nomEnceinte=forms.CharField(label="Nom de l'enceinte")
    class Meta:
        model=Enceinte
        exclude=['created_at','modified_at']
        
        def __init__(self,*args,**kwargs):
            super(EnceinteForms,self).__init__(*args,**kwargs)        
            self.fields['parent'].queryset=Enceinte.objects.none()        
            if 'niveau' in self.data:
                if self.data['niveau']=='REGION':                
                    self.fields['parent'].queryset=Enceinte.objects.none()
                elif self.data['niveau']=='DISTRICT':  
                    self.fields['parent'].queryset=Enceinte.objects.filter(niveau_niveau='REGION') 
                elif self.data['niveau']=='FOSA':
                    self.fields['parent'].queryset=Enceinte.objects.filter(niveau_niveau='DISTRICT') 
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
        fields=['enceinte','service','cautionAdminission']
        
class CreateService(forms.ModelForm):
    class Meta:
        model=Servico
        fields=['service','cautionAdminission']
        

class EquipementForms(forms.ModelForm):
    nomEquip=forms.CharField(label="Equiupement", max_length=150)
    class Meta:
        model=Equipement
        fields=['nomEquip' ]
    
           
                          