from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from .models import *
from . import serializers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet



def acceuil(request):
    return render(request,'Acceuil.html')

# class RegisterView(ModelViewSet) :
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class =serializers.RegistrationSerializer