import django_filters
from .models import *

class EnceinteFilter(django_filters.FilterSet):    
    class Meta:
        model=Enceinte
        fields=['secteur','categorie','reseau','niveau'] 

class Appartenirfilter(django_filters.FilterSet):
    #service=django_filters.ModelChoiceFilter(name='service',action='filtreservice')  
    class Meta:
        model= Appartenir
        fields=['service'] 
    
    
    
class EquipementFiltre(django_filters.FilterSet):
    nomEquip=django_filters.ModelChoiceFilter(label='Equipement', queryset=Equipement.objects.all().distinct().order_by('nomEquip'))
    class Meta:
        model=Equipement
        fields=['nomEquip']

class UserFiltre(django_filters.FilterSet): 
        class Meta:
            model=User
            fields=['nom']  
            
class EncuserFilter(django_filters.FilterSet):
    class Meta:
        model=EncUser
        fields=['enceinte']                     