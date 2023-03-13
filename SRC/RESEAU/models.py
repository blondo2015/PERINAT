from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
import uuid

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, telephone, password=None):
        if not telephone:
            raise ValueError('Les utilisateurs doivent avoir un numero de telephone')
        user = self.model(telephone=self.normalize_email(telephone), )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, telephone, password):
        user = self.create_user(telephone, password=password, )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password):
        user = self.create_user(telephone, password=password, )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    code = models.CharField(max_length=10, default="")
    nom = models.CharField(max_length=150, default="")
    telephone = models.CharField(max_length=9, unique=True)
    email=models.EmailField(max_length=254,default="")
    dteEnrollement = models.DateField(null=True, blank=True)
    choixsexe = (
        ("F", "F"),
        ("M", "M"),
    )
    sexe = models.CharField(max_length=150, choices=choixsexe, default="F")
    foto = models.ImageField(upload_to='user/', blank=True, null=True)
    mvt_at = models.DateTimeField(auto_now_add=True)
    suspendu = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modify_at = models.DateTimeField(default=datetime.now, blank=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        # L'utilisateur est identifier par son adresse e-mail
        return self.telephone

    def get_short_name(self):
        # Utilisation est identifier par son adresse e-mail
        return self.telephone

    def __str__(self):
        return self.telephone


    def has_perm(perm,obj=None):
        """L'utilisateur a-t-il une autorisation spécifique ?"""
        """Réponse la plus simple possible : Oui, toujours"""
        return True

    def has_module_perms(self, app_label):
        # "L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application ?`app_label`?"
        # Réponse la plus simple possible : Oui, toujours
        return True

    @property
    def is_staff(self):
        """L'utilisateur est-il un membre du personnel ?"""
        return self.staff

    @property
    def is_admin(self):
        """L'utilisateur est-il un membre administrateur?"""
        return self.admin


class Categorie(models.Model):
    categorie = models.CharField(max_length=50, default="", blank=True, null=True)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.categorie


class Reso(models.Model):
    reseau = models.CharField(max_length=50, default="CENTRE")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.reseau


class Nivo(models.Model):
    niveau = models.CharField(max_length=50, default="FOSA")
    codenivo=models.CharField(max_length=2,default="FS")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.niveau


class Secteur(models.Model):
    nom = models.CharField(max_length=50, default="PUBLIC")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nom


class Enceinte(models.Model):
    code = models.CharField(max_length=10, default="")
    nomEnceinte = models.CharField(max_length=100)
    adresse = models.CharField(max_length=150, default="")
    contact1 = models.CharField(max_length=9, default="", blank=True, null=True)
    contact2 = models.CharField(max_length=9, default="", blank=True, null=True)
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE, default=1, null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1, null=True, blank=True)
    reseau = models.ForeignKey(Reso, on_delete=models.CASCADE, default=1, null=True, blank=True)
    niveau = models.ForeignKey(Nivo, on_delete=models.CASCADE, default=1, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nomEnceinte
    def codens(self):
        code=""
        try:
            code=Nivo.objects.get(nivo=self.niveau)
        except:
            pass    
        liste=Enceinte.objects.filter(nivo=self.niveau)
        if len(liste)<10:
            self.code=str(code.codenivo)+"0"+str(len(liste)+1)
        elif len(liste)>=10 :
            self.code=str(code.codenivo)+str(len(liste)+1)
            return self.code   

class Servico(models.Model):
    service = models.CharField(max_length=25, default="")
    cautionAdminission = models.FloatField(default=0)
    enceinte = models.ForeignKey(Enceinte, on_delete=models.CASCADE,blank=True,null=True,related_name='services')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.service


class Equipement(models.Model):
    nomEquip = models.CharField(max_length=50,unique=True)
    mesenceintes=models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nomEquip
    
    def compteservice(self): 
        service=Appartenir.objects.filter(equipement_id=self.id).distinct()            
        self.mesenceintes=service.count()
        return self.mesenceintes


class Appartenir(models.Model):
    service = models.ForeignKey(Servico, on_delete=models.CASCADE,related_name='appartenirservice')
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE,related_name='appartenirequipement')
    pu = models.FloatField(default=0)
    periodicite = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.service.nomService


class EncUser(models.Model):
    pointfocal = models.BooleanField(default=False)
    dte = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='users')
    enceinte = models.ForeignKey(Enceinte, on_delete=models.CASCADE, null=True, blank=True,related_name='enceintes')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class Patient(models.Model):
    id=models.CharField(primary_key = True,editable = True,default = uuid.uuid4,unique=True,max_length=100)
    nompatient = models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1,related_name='unuser')
    dtenaiss = models.DateField(blank=True, null=True)
    lieunaiss = models.CharField(max_length=100, null=True, default="")
    poids = models.DecimalField(max_digits=5, decimal_places=2)
    pathologie = models.CharField(max_length=250)
    ethnie=models.CharField(max_length=15,default="")
    religion=models.CharField(max_length=15,default="")
    profession_tuteur=models.CharField(max_length=25,default="")
    contact=models.CharField(max_length=15,default="")
    choixsexe = (
        ("F", "F"),
        ("M", "M"),
    )
    sexe = models.CharField(max_length=150, choices=choixsexe, default="F")
    created=models.CharField(max_length=50,default="")
    modified=models.CharField(max_length=50,default="")


class Demande(models.Model):
    id=models.CharField(primary_key = True,editable = True,default = uuid.uuid4,unique=True,max_length=100)
    patient = models.ForeignKey(Patient, max_length=25, on_delete=models.CASCADE, default="",related_name='patients')
    encuser = models.ForeignKey(EncUser, max_length=100, on_delete=models.CASCADE, default="",related_name='encusers')    
    detailtransport = models.CharField(max_length=150, default="")
    created=models.CharField(max_length=50,default="")
    modified=models.CharField(max_length=50,default="")


class Referer(models.Model): 
    id=models.CharField(primary_key = True,editable = True,default = uuid.uuid4,unique=True,max_length=100)
    demande=models.ForeignKey(Demande,on_delete=models.CASCADE,default=1,null=True,related_name="demandes")   
    choixTransport = (
        ("AMBULANCE", "AMBULANCE"),
        ("VEHICULE PERSONNEL", "VEHICULE PERSONNEL"),
        ("TRANSPORT EN COMMUN", "TRANSPORT EN COMMUN"),
        ("AUTRE MOYEN", "AUTRE MOYEN"),
    )
    caregiven = models.CharField(max_length=150, default="")
    transport = models.CharField(max_length=150, choices=choixTransport, default="AUTRE MOYEN")
    dterefencement = models.DateField(default="")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created=models.CharField(max_length=50,default="")
    modified=models.CharField(max_length=50,default="")
