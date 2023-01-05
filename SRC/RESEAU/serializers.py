from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ["id","username","nom", "telephone","administrateur","dteEnrollement","sexe","foto"]

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)   
    
    class Meta:
        model = User
        fields = [
            "username",
            "nom",
            "telephone",
            "administrateur",
            "dteEnrollement",
            "sexe",
            "foto",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            telephone=validated_data['telephone'],
            nom=validated_data['nom'],
            administrateur=validated_data['administrateur'],
            dteEnrollement=validated_data['dteEnrollement'],   
            sexe=validated_data['sexe'], 
            foto=validated_data['foto'],           
            )
        user.set_password(validated_data['password'])        
        user.save()
        return user    
        