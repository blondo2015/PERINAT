from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction



#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ["id","nom", "telephone","administrateur","dteEnrollement","sexe","foto"]

class UneenceinteSerializer(serializers.ModelSerializer):
    class Meta:
       model = Enceinte
       fields=['code' ]         

class RegistrationSerializer(serializers.ModelSerializer):
    code=serializers.CharField(max_length=10,required=True)  
    class Meta:
        model = User
        fields = [
            "code",
            "nom",
            "telephone",
            "dteEnrollement",
            "sexe",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "code":{"read_only":True}
            }
        
    def get_code(self):
        enceinte=Enceinte.objects.filter(code=self.code)
        if len(enceinte)!=1:
            return self.code
        raise ValidationError("ce code nexiste pas ou autres chose")
    
    @transaction.atomic     
    def create(self, validated_data):
        user = User(            
            code=validated_data['code'],                  
            nom=validated_data['nom'],
            telephone=validated_data['telephone'],            
            dteEnrollement=validated_data['dteEnrollement'],   
            sexe=validated_data['sexe'], 
            #foto=validated_data['foto']#.request.FILES,           
            )
        user.set_password(validated_data['password']) 
        #images_data = validated_data['foto'].request.FILES 
        #user.foto=images_data      
        user.save()
        enceinte=Enceinte.objects.get(code=validated_data['code'])
        enuser=EncUser.objects.create(pointfocal=False)
        enuser.enceinte=enceinte
        enuser.user=user
        enuser.save()
        return user    
        