from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime

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
    cat = models.CharField(max_length=50, default="", blank=True, null=True)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.cat


class Reso(models.Model):
    nomreso = models.CharField(max_length=50, default="CENTRE")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nomreso


class Nivo(models.Model):
    nivo = models.CharField(max_length=50, default="FOSA")
    codenivo=models.CharField(max_length=2,default="FS")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nivo


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
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=0, null=True, blank=True)
    reso = models.ForeignKey(Reso, on_delete=models.CASCADE, default=1, null=True, blank=True)
    nivo = models.ForeignKey(Nivo, on_delete=models.CASCADE, default=1, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.code
    def codens(self):
        code=""
        try:
            code=Nivo.objects.get(nivo=self.nivo)
        except:
            pass    
        list=Enceinte.objects.filter(nivo=self.nivo)
        if len(list)<10:
            self.code=str(code.codenivo)+"0"+str(len(list)+1)
        elif len(list)>=10 :
            self.code=str(code.codenivo)+str(len(list)+1)
            return self.code   

class Service(models.Model):
    nomService = models.CharField(max_length=10, default="NeoNat")
    cautionAdminission = models.FloatField(default=0)
    enceinte = models.ForeignKey(Enceinte, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class Equipement(models.Model):
    nomEquip = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nomEquip


class Appartenir(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    pu = models.FloatField(default=0)
    periodicite = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class EncUser(models.Model):
    pointfocal = models.BooleanField(default=False)
    dte = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    enceinte = models.ForeignKey(Enceinte, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nompatient = models.CharField(max_length=250)
    dtenaiss = models.DateField(blank=True, null=True)
    lieunaiss = models.CharField(max_length=100, null=True, default="")
    poids = models.DecimalField(max_digits=5, decimal_places=2)
    petitpoids = models.BooleanField(default=False)
    pathologie = models.CharField(max_length=250)
    choixsexe = (
        ("F", "F"),
        ("M", "M"),
    )
    sexe = models.CharField(max_length=150, choices=choixsexe, default="F")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class Demande(models.Model):
    patient = models.ForeignKey(Patient, max_length=25, on_delete=models.CASCADE, default="")
    encuser = models.ForeignKey(EncUser, max_length=100, on_delete=models.CASCADE, default="")
    caregiven = models.CharField(max_length=150, default="")
    choixTransport = (
        ("AMBULANCE", "AMBULANCE"),
        ("VEHICULE PERSONNEL", "VEHICULE PERSONNEL"),
        ("TRANSPORT EN COMMUN", "TRANSPORT EN COMMUN"),
        ("AUTRE MOYEN", "AUTRE MOYEN"),
    )
    transport = models.CharField(max_length=150, choices=choixTransport, default="AUTRE MOYEN")
    detailtransport = models.CharField(max_length=150, default="")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)


class Referer(models.Model):
    dterefencement = models.DateField(default="")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    mvt_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    modified_at = models.DateTimeField(default=datetime.now, blank=True)
