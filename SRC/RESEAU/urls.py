from django.urls import path,include
from .views import *
from django.conf.urls.static import  static
from django.conf import settings


#router = routers.DefaultRouter()
# router.register(r'Register', RegisterView)

urlpatterns = [
    path('',connexion,name='connexion'),
    path('Dashboard/',acceuil,name='Dashboard'),
    path('Fosa/',listefosa,name='Fosa'),
    path('Fosadd/',Enceintecreation,name='Fosadd'),
    path('FosaDetail/<id>',detailenceinte,name='FosaDetail'),
    path('FosaUpdate/<id>',enceinteupdate,name='FosaUpdate'),
    path('Patientlist/',patientfiltre,name='Patientlist'), 
    path('patientDetail/<id>',detailpatient,name='patientDetail'),
    path('createservice/<id>',createservice,name='createservice'),
    path('listequipement/',listedesequipements,name='listequipement'),   
    path('listeuser/',listutilisateur,name='listeuser'),
    #les routes des apis
    path('api/Register',Register,name='Registeruser'), 
    path('api/Patient/<date_start>)',apipaient,name='Apipatient'),
    path('api/connexion/',CustomAuthTokenlogin.as_view(), name='apiconnexion'),  
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
