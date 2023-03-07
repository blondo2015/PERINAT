import django_filters
from .models import *

class EnceinteFilter(django_filters.FilterSet):    
    class Meta:
        model=Enceinte
        fields=['secteur','categorie','reseau','niveau'] 

class Appartenirfilter(django_filters.FilterSet):
  
    class Meta:
        model= Appartenir
        fields=['service']   
    
    
class Appartenirfilter2(django_filters.FilterSet):
        class Meta:
            model=Appartenir
            fields=['equipement']

class UserFiltre(django_filters.FilterSet): 
        class Meta:
            model=User
            fields=['nom']  
            
class EncuserFilter(django_filters.FilterSet):
    class Meta:
        model=EncUser
        fields=['enceinte']                     