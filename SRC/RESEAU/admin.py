from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(EncUser)
admin.site.register(Enceinte)
admin.site.register(Secteur)
admin.site.register(Service)
admin.site.register(patient)
admin.site.register(Reso)
admin.site.register(Categorie)
admin.site.register(Equipement)
admin.site.register(EquipService)
admin.site.register(Referer)

