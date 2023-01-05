from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    username = models.EmailField(max_length=254,unique=True, null=True) 
    telephone =models.CharField(max_length=9,default="")       
    nom=models.CharField(max_length=150,default="") 
    foto=models.ImageField(upload_to='user/',default="",blank=True,null=True)
    administrateur=models.BooleanField(default=False)
    suspendu=models.BooleanField(default=False)
    dteEnrollement=models.DateField(null=True, blank=True)
    password=models.CharField(max_length=150) 
    choixsexe=(
        ("F","F"),
        ("M","M"),
    )
    sexe=models.CharField(max_length=150,choices=choixsexe,default="F") 
    mvt_at=models.DateTimeField(auto_now_add=True) 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modify_at=models.DateTimeField(default=datetime.now, blank=True)   
    
    USERNAME_FIELD='username'
    
class Categorie(models.Model):
    cat=models.CharField(max_length=50,default="",blank=True,null=True)
    mvt_at=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
        
    def __str__(self):
        return self.cat

class Reso(models.Model):
    nonreso=models.CharField(max_length=50,default="CENTRE")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)      
        
    def __str__(self):
        return self.nonreso

class Nivo(models.Model):
    nomNivo=models.CharField(max_length=50,default="FOSA")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
        
    def __str__(self):
        return self.nomNivo  
    
class Secteur(models.Model):
    nomSecteur=models.CharField(max_length=50,default="PUBLIC")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
    def __str__(self):
        return self.nomSecteur       

class Enceinte(models.Model):
    code=models.CharField(max_length=10,default="")
    nomEnceinte=models.CharField(max_length=100)
    adresse=models.CharField(max_length=250,default="")
    contact1=models.CharField(max_length=13,default="")
    contact2=models.CharField(max_length=13,default="")
    category=models.ForeignKey(Categorie,on_delete=models.CASCADE,default=0,null=True,blank=True)
    reso=models.ForeignKey(Reso,on_delete=models.CASCADE,default=0,null=True,blank=True)
    nivo=models.ForeignKey(Nivo,on_delete=models.CASCADE,default=0,null=True,blank=True)
    secteur=models.ForeignKey(Secteur,on_delete=models.CASCADE,default=1)
    parent=models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    mvt_at=models.DateTimeField(auto_now_add=True) 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
    def __str__(self):
        return self.nomNivo  

class Service(models.Model):
    nomService=models.CharField(max_length=10,default="NeoNat")
    cautionAdminission=models.FloatField(default=0) 
    enceinte=models.ForeignKey(Enceinte,on_delete=models.CASCADE) 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)           

class Equipement(models.Model):
    nomEquip=models.CharField(max_length=50)
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)   
    
    def __str__(self):
        return self.nomEquip  
class EquipService(models.Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE)  
    equipement=models.ForeignKey(Equipement,on_delete=models.CASCADE) 
    pu=models.FloatField(default=0)
    periodicite=models.CharField(max_length=10)
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)   

class EncUser(models.Model):
    pointfocal=models.BooleanField(default=False)
    dte=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    enceinte=models.ForeignKey(Enceinte,on_delete=models.CASCADE) 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  


class patient(models.Model):
    nompatient=models.CharField(max_length=250) 
    dtenaiss=models.DateField(blank=True,null=True)
    lieunaiss=models.CharField(max_length=100, null=True,default="")
    poids=models.DecimalField(max_digits=5,decimal_places=2)
    petitpoids=models.BooleanField(default=False)        
    pathologie=models.CharField(max_length=250)
    choixsexe=(
        ("F","F"),
        ("M","M"),
    )
    sexe=models.CharField(max_length=150,choices=choixsexe,default="F") 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)    
    
class Referer(models.Model):
    dterefencement=models.DateField(default="")
    mvt_at=models.DateTimeField(auto_now_add=True) 
    caregiven=models.CharField(max_length=150,default="")
    choixTransport=(
    ("AMBULANCE", "AMBULANCE"),
    ("VEHICULE PERSONNEL", "VEHICULE PERSONNEL"),
    ("TRANSPORT EN COMMUN", "TRANSPORT EN COMMUN"),
    ("AUTRE MOYEN", "AUTRE MOYEN"),
)
    transport=models.CharField(max_length=150,choices=choixTransport,default="AUTRE MOYEN")
    detailtransport=models.CharField(max_length=150,choices=choixTransport,default="")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  