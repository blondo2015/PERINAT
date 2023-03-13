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
    path('loadparent/',loadparent,name='loadparent'),
    path('FosaDetail/<id>',detailenceinte,name='FosaDetail'),
    path('FosaUpdate/<id>',enceinteupdate,name='FosaUpdate'),
    path('Patientlist/',patientfiltre,name='Patientlist'), 
    path('patientDetail/<id>',detailpatient,name='patientDetail'),
    path('createservice/<id>',createservice,name='createservice'),
    path('listequipement/',listedesequipements,name='listequipement'),  
    path('equipementadd/',EquipemmentCreate,name='equipementadd'),  
    path('equipementupdate/<pk>',EquipemntUpdate,name='equipementupdate'),  
    path('equipementDetail/<pk>',detailEquipement,name='equipementDetail'),   
    path('listeuser/',listutilisateur,name='listeuser'),
    #les routes des apis
    path('api/Register',Register,name='Registeruser'), 
    path('api/Patient/',PatientListcreateApiview.as_view()),
    path('api/PatientPut/<pk>',PatientRetrieveUpdateDestroyAPIView.as_view()),
    path('api/Demande/',DemandeListcreateApiview.as_view()),
    path('api/DemandePut/<pk>',PatientRetrieveUpdateDestroyAPIView.as_view()),
    path('api/Referer/',RefererListcreateApiview.as_view()),
    path('api/RefererPut/<pk>',RefererRetrieveUpdateDestroyAPIView.as_view()),
    path('api/connexion/',CustomAuthTokenlogin.as_view()),  
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
