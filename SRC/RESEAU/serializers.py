from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ["id","nom", "telephone","administrateur","dteEnrollement","sexe","foto"]

class RegistrationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = User
        fields = [
            "nom",
            "telephone",
            "dteEnrollement",
            "sexe",
            "foto",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User(            
            nom=validated_data['nom'],
            telephone=validated_data['telephone'],            
            dteEnrollement=validated_data['dteEnrollement'],   
            sexe=validated_data['sexe'], 
            foto=validated_data['foto'],           
            )
        user.set_password(validated_data['password'])        
        #user.save()
        return user    
        