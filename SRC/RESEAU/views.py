from django.shortcuts import render
from .models import *
from .forms import *
from . import serializers
from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime
# les classes de l'admin 
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# les classes du drf
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

#  gestioin de l'admin 

def connexion(request):
    
    if request.method=='POST':
        form=ConnexionForms(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['telephone'],password=form.cleaned_data['password']) 
            if user is not None:
               login(request,user)
               return redirect('Menuprincipal')         
            else:
                form=ConnexionForms()
                return render(request,'connexion.html',{'form':form,"msg":"vous n'avez pas le droit de vous connecter","dte":datetime.now})
        else:
            form=ConnexionForms()
            return render(request,'connexion.html',{'form':form,"msg":" les données en entrée ne sont pas vailidées","dte":datetime.now})
    else:
            form=ConnexionForms()
            return render(request,'connexion.html',{'form':form,"dte":datetime.now})        #   
        


# gest ion des api 
@login_required
def acceuil(request):
    return render(request,'menu.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request, *args, **kwargs):
    if request.method == 'POST':        
        serializer=serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid():       
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class CustomAuthTokenlogin(ObtainAuthToken):    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        enceinte=Enceinte.objects.get(code=user.code)
        encuser=EncUser.objects.get(enceinte=enceinte,user=user)
        token, created = Token.objects.get_or_create(user=user)
        if user.foto:
            return Response({
            'token': token.key,
            'user_id': user.pk,
            'encuse_id': encuser.id,           
            'code':user.code,
            'nom':user.nom,
            'telephone':user.telephone,
            'dteEnrollement':user.dteEnrollement, 
            'foto':user.foto.url,
            'sexe' :user.sexe,              
            })  
        return Response({
            'token': token.key,
            'user_id': user.pk, 
            'encuse_id': encuser.id,             
            'code':user.code,
            'nom':user.nom,
            'telephone':user.telephone,
            'dteEnrollement':user.dteEnrollement, 
            'foto':"",
            'sexe' :user.sexe,              
            },status=status.HTTP_200_OK)            
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PAtientAPI(request,id=None):    
    if request.method=='POST':
        serializer=serializers.Patientserialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apipaient(request,date_start=None):
    if request.method=='GET':
        listpatient=""
        if date_start is None:
            listpatient=Patient.objects.filter(user=request.user).all().order_by('-modified_at')
        else:
            listpatient=Patient.objects.filter(user=request.user,modified_at__gt=date_start).all().order_by('-modified_at')        
        serializer=serializers.Patientserialize(listpatient,many=True)
        return Response(serializer.data)
     
    if request.method=='POST':
        serializer=serializers.Patientserialize(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    