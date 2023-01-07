from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, telephone, password=None):
   
        if not telephone:
            raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')
        user = self.model(
        telephone=self.normalize_email(telephone),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_staffuser(self, telephone, password):
        user = self.create_user(telephone,password=password,)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password):        
        user = self.create_user(telephone,password=password,)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser): 
    nom=models.CharField(max_length=150,default="") 
    telephone =models.CharField(max_length=9,unique=True)    
    dteEnrollement=models.DateField(null=True, blank=True)    
    choixsexe=(
        ("F","F"),
        ("M","M"),
    )
    sexe=models.CharField(max_length=150,choices=choixsexe,default="F")
    foto=models.ImageField(upload_to='user/',default="",blank=True,null=True)
    mvt_at=models.DateTimeField(auto_now_add=True)  
    suspendu=models.BooleanField(default=False)  
    is_active=models.BooleanField(default=True)
    staff=models.BooleanField(default=True)    
    admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modify_at=models.DateTimeField(default=datetime.now, blank=True)   
    
          
    USERNAME_FIELD='telephone'
    REQUIRED_FIELDS = []
    
    objets = UserManager ()
    
    def get_full_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.telephone
    def get_short_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.telephone
    def __str__(self):
        return self.telephone
    def has_perm(self, perm, obj=None):
        # "L'utilisateur a-t-il une autorisation spécifique ?"
        # Réponse la plus simple possible : Oui, toujours
        return True
    def has_module_perms(self, app_label):
        # "L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application ?`app_label`?"
        # Réponse la plus simple possible : Oui, toujours
        return True
    @property
    def is_staff(self):
        "L'utilisateur est-il un membre du personnel ?"
        return self.staff
    @property
    def is_admin(self):
        "L'utilisateur est-il un membre administrateur?"
        return self.admin
    
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
    nivo=models.CharField(max_length=50,default="FOSA")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)        
    def __str__(self):
        return self.nivo  
    
class Secteur(models.Model):
    nomSecteur=models.CharField(max_length=50,default="PUBLIC")
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
    def __str__(self):
        return self.nomSecteur       

class Enceinte(models.Model):
    code=models.CharField(max_length=10,default="")
    nomEnceinte=models.CharField(max_length=100)
    adresse=models.CharField(max_length=150,default="")
    contact1=models.CharField(max_length=9,default="",blank=True,null=True)
    contact2=models.CharField(max_length=9,default="",blank=True,null=True)
    secteur=models.ForeignKey(Secteur,on_delete=models.CASCADE,default=1)
    category=models.ForeignKey(Categorie,on_delete=models.CASCADE,default=0,null=True,blank=True)
    reso=models.ForeignKey(Reso,on_delete=models.CASCADE,default=1,null=True,blank=True)   
    nivo=models.ForeignKey(Nivo,on_delete=models.CASCADE,default=1,null=True,blank=True)    
    parent=models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    mvt_at=models.DateTimeField(auto_now_add=True) 
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    modified_at=models.DateTimeField(default=datetime.now, blank=True)  
    def __str__(self):
        return self.code  

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