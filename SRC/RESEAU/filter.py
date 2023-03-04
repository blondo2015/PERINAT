import django_filters
from .models import Enceinte,Appartenir

class EnceinteFilter(django_filters.FilterSet):    
    class Meta:
        model=Enceinte
        fields=['secteur','category','reso','nivo'] 

class Equipementfilter(django_filters.FilterSet):
    class Meta:
        model= Appartenir
        fields=['service']         