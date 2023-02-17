from django.shortcuts import render,get_object_or_404
from .models import *
from .forms import *
from . import serializers
from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime
# les classes de l'admin 
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

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

# controle e session 

def connexion(request): 
    if request.user.is_authenticated:
        print('deconnexion',request.user)
        logout(request)
        return redirect('connexion')
        # print(request.user)
        # return redirect('Dashboard') 
    else:
        if request.method=='POST':
            form=ConnexionForms(request.POST)
            if form.is_valid():
                user=authenticate(username=form.cleaned_data['telephone'],password=form.cleaned_data['password']) 
                if user is not None:
                   login(request,user)
                   print(request.user,"ok")
                   return redirect('Dashboard')
                else:
                    form=ConnexionForms()
                    return render(request,'connexion.html',{'form':form,"msg":"vous n'avez pas le droit de vous connecter","dte":datetime.now})
            else:
                form=ConnexionForms()
                return render(request,'connexion.html',{'form':form,"msg":" les données en entrée ne sont pas vailidées","dte":datetime.now})
        else:
            form=ConnexionForms()
            return render(request,'connexion.html',{'form':form,"dte":datetime.now})
        
 

def deconnexion(request):
    print('deconnextion',request.user)
    logout(request)
    return redirect('connexion')
    
@login_required
def acceuil(request):
   if request.user.is_authenticated:
       return render(request,'menu.html',{'user':request.user})


@login_required 
def listefosa(request):
    if request.user.is_authenticated:
        reso=Reso.objects.all() 
        cat=Categorie.objects.all()        
        nivo=Nivo.objects.all()
        secteur=Secteur.objects.all()
        listfosa=Enceinte.objects.all().order_by('-id')
        p = Paginator(listfosa, 10)
        page_number = request.GET.get('page') 
        try:
            po = p.page(page_number)
        except PageNotAnInteger: 
            po = p.page(1)   
        except EmptyPage:
            po = p.page(p.num_pages)
        return render(request,'listefosa.html',{
                        'user':request.user,
                        'reso':reso,
                        'cat':cat,
                        'nivo':nivo,
                        'secteur':secteur,
                        'po':po,
                        })
        
@login_required 
def triefosa(request):
    if request.user.is_authenticated:
        categorie=request.POST.get['cat']   
        reso=request.POST.get['reso'] 
        nivo=request.POST.get['nivo']
        listtrie=Enceinte.objects.filter(reso=reso,nivo=nivo,category=categorie).all()    
        return render(request,'Enceintetrie.html',{'user':request.user,'page':'Trie Enceinte','listefosa':listtrie,})  


@login_required 
def Enceintecreation(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=EnceinteForms(request.POST or None)
            if form.is_valid():
                enc=form.save(commit=False)
                enc.codens()
                enc.save()
                form=EnceinteForms()
                return render(request,'Enceinte.html',{'form':form,'user':request.user,'msg':'message enregistré avec succès'})
            else:
                form=EnceinteForms() 
                return render(request,'Enceinte.html',{'form':form,'user':request.user,'msg':'données invalides'})
        else:
            form=EnceinteForms() 
            return render(request,'Enceinte.html',{'form':form,'user':request.user,})
            
    else:
        return redirect ('connexion') 
    
    
         
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
    
def detailenceinte(request,id):
    if request.user.is_authenticated:
        dtl=get_object_or_404(Enceinte,id=id)
        list=Enceinte.objects.filter(parent=dtl)
        return render(request,'enceintDetail.html', {'dtl':dtl,'user':request.user,'list':list})
    else:
        return redirect ('connexion') 
    
def enceinteupdate(request,id):
    if request.user.is_authenticated:
        enc=get_object_or_404(Enceinte,id=id)
        form=EnceinteForms(request.POST or None,instance=enc)
        if request.method=='POST':            
            if form.is_valid():
                enc=form.save()
                return redirect('Fosa')
            return render(request,'enceintUpdate.html', {'form':form,'user':request.user,'enc':enc})
        return render(request,'enceintUpdate.html', {'form':form,'user':request.user,'enc':enc})
    return redirect('connexion')
            
            
            
                
