from django.shortcuts import render,get_object_or_404
from .models import *
from .forms import *
from .filter import *
from .serializers import *
from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime
# les classes de l'admin 
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# les classes du drf
from rest_framework.generics  import ListCreateAPIView,RetrieveUpdateDestroyAPIView
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
    listfosa=Enceinte.objects.all().order_by('-id')    
    myfilter=EnceinteFilter(request.GET,queryset=listfosa)
    listfosa=myfilter.qs
    p=Paginator(listfosa,8)
    page_number = request.GET.get('page') 
    try:
        po=p.page(page_number)   
    except PageNotAnInteger:
        po=p.page(1)   
    except EmptyPage:
        po=p.page(p.num_pages)
    return render(request,'listefosa.html',{
                        'user':request.user,
                        'myfilter':myfilter, 
                        'po':po                       
                        })
    
 
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
        enceinte=get_object_or_404(Enceinte,code=user.code)
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


# @api_view(['GET','POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def apipaient(request,date_start=None):
#     if request.method=='GET':
#         listpatient=""
#         if date_start is None:
#             listpatient=Patient.objects.filter(user=request.user).all().order_by('-modified_at')
#         else:
#             listpatient=Patient.objects.filter(user=request.user,modified_at__gt=date_start).all().order_by('-modified_at')        
#             serializer=serializers.Patientserialize(listpatient,many=True)
#         return Response(serializer.data)
     
#     if request.method=='POST':
#         serializer=serializers.Patientserialize(data=request.data) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PatientListcreateApiview(ListCreateAPIView):
    queryset=Patient.objects.all()
    serializer_class=Patientserializer
    def get_queryset(self):            
       return Patient.objects.all()
    
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PatientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Patient.objects.all()
    serializer_class=Patientserializer 
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DemandeListcreateApiview(ListCreateAPIView):
    queryset=Demande.objects.all()
    serializer_class=Damandeserializer
    def get_queryset(self):              
       return Demande.objects.filter(encuser__user=self.request.user)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DemandeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Demande.objects.all()
    serializer_class=Referencementserializer
       
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RefererListcreateApiview(ListCreateAPIView):
    queryset=Referer.objects.all()
    serializer_class=Referencementserializer  
    def get_queryset(self):              
       return Referer.objects.filter(demande__encuser__user=self.request.user) 
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RefererRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Referer.objects.all()
    serializer_class=Referencementserializer     
    
    
     
           
def detailenceinte(request,id):
    if request.user.is_authenticated:
        dtl=get_object_or_404(Enceinte,id=id)
        liste=Servico.objects.filter(enceinte_id=id)
        p=Paginator(liste,2)
        page_number = request.GET.get('page') 
        try:
            po=p.page(page_number)   
        except PageNotAnInteger:
            po=p.page(1)   
        except EmptyPage:
            po=p.page(p.num_pages)
        listequip=Appartenir.objects.filter(service__enceinte_id=id)
        myfilter=Appartenirfilter(request.GET,queryset=listequip)
        listequip=myfilter.qs
        return render(request,'enceintDetail.html', {
            'dtl':dtl,
            'user':request.user,
            'po':po,
            'listequip':listequip,
            'myfilter':myfilter
            })
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

@login_required            
def patientfiltre(request):
    if request.method=='POST':
        form=patientfiltreform(request.POST or None)
        if form.is_valid():
            list=Patient.objects.filter(nompatient__icontains=form.cleaned_data['rechercher'])
            p=Paginator(list.order_by('-created'),10)
            page_numberjj = request.GET.get('page') 
            try :
                po=p.page(page_numberjj) 
            except PageNotAnInteger:
                po=p.page(1) 
            except EmptyPage:
                po=p.page(p.num_pages)
            return render(request,'patient.html',{'form':form,'po':po,'user':request.user}) 
        else: 
            list=Patient.objects.all()
            p=Paginator(list.order_by('-created'),10)
            page_number = request.GET.get('page') 
            try :
                po=p.page(page_number) 
            except PageNotAnInteger:
                po=p.page(1) 
            except EmptyPage:
                po=p.page(p.num_pages)
            return render(request,'patient.html',{'form':form,'po':po,'user':request.user})
    else:
        form=patientfiltreform()
        list=Patient.objects.all()
        p=Paginator(list.order_by('-created'),10)
        page_number = request.GET.get('page') 
        try :
            po=p.page(page_number) 
        except PageNotAnInteger:
            po=p.page(1) 
        except EmptyPage:
            po=p.page(p.num_pages)
        return render(request,'patient.html',{'form':form,'po':po,'user':request.user})
                    
@login_required
def detailpatient(request,id):
    patient=get_object_or_404(Patient,id=id)
    liste=Referer.objects.filter(demande__patient_id=id) 
    p=Paginator(liste.order_by('-created'),5)
    page_number = request.GET.get('page') 
    try:
        po=p.page(page_number)   
    except PageNotAnInteger:
        po=p.page(1)   
    except EmptyPage:
        po=p.page(p.num_pages)
    return render(request,'patientdetail.html',{'po':po,'user':request.user,'patient':patient})  

@login_required 
def createservice(request,id):
    enceinte=Enceinte.objects.get(id=id)
    if request.method=='POST':
        form=CreateService(request.POST or None)
        if form.is_valid():           
            service=form.save()
            service.enceinte=enceinte
            service.save()
            form=CreateService()
            return render(request,'createservice.html',{
                'form':form,
                'msg':'enregistrement effectué avec succès',
                'user':request.user,
                'enc':enceinte
                })
        else:
            form=CreateService()
            return render(request,'createservice.html',{
                'form':form,
                'msg':'verifiez vos champs',
                'user':request.user,
                'enc':enceinte
                })
    else: 
        form=CreateService()
        return render(request,'createservice.html',{
                'form':form,
                'user':request.user,
                'enc':enceinte
                })       
                
@login_required            
def listedesequipements(request):
    liste=Equipement.objects.all()
    myFilter=EquipementFiltre(request.GET,queryset=liste)
    liste=myFilter.qs
    return render(request,'listequipement.html',{'list':liste,'user':request.user,'myFilter':myFilter})


@login_required
def listutilisateur(request):
    listuser=EncUser.objects.all()
    myFilter=EncuserFilter(request.GET,queryset=listuser)
    listuser=myFilter.qs
    p=Paginator(listuser,8)
    page_number = request.GET.get('page') 
    try:
        po=p.page(page_number)
    except PageNotAnInteger :
        po=p.page(1)
    except EmptyPage:
        po=p.page(p.num_pages) 
    return render(request,'user.html',{'user':request.user,'po':po,'myFilter':myFilter})

@login_required
def loadparent(request):
    nivo_id=request.GET['niveau']
    nivo=Nivo.objects.get(id=nivo_id)
    if nivo.niveau=='REGION':
        parent=Enceinte.objects.none()
    elif nivo.niveau=='DISTRICT':   
        parent=Enceinte.objects.filter(niveau_niveau='REGION').order_by('+nomEnceinte')
    elif nivo.niveau=='FOSA':   
        parent=Enceinte.objects.filter(niveau_niveau='DISTRICT').order_by('+nomEnceinte') 
    return render(request,'select_parent_enceint.html',{'parent':parent})   

@login_required
def EquipemmentCreate(request):
    if request.method=='POST':
        form=EquipementForms(request.POST or None) 
        if form.is_valid():
            equip=form.save()  
            equip.compteservice()
            equip.save()
            form=EquipementForms()
            return render(request,'equipementcreate.html',{
                'msg':'enregistrement effectué avec succès',
                'form':form,
                'user':request.user
            })
        else:
            form=EquipementForms()
            return render(request,'equipementcreate.html',{
                'msg':'',
                'form':form,
                'user':request.user
            })
    else:
        form=EquipementForms()
        return render(request,'equipementcreate.html',{
            'msg':'',
            'form':form,
            'user':request.user
        })
        
@login_required
def EquipemntUpdate(request,pk):
    equip=get_object_or_404(Equipement,pk=pk)
    if request.method=='POST':
        form=EquipementForms(request.POST or None,instance=equip)
        if form.is_valid():
            e=form.save()
            e.compteservice()
            e.save()
            return redirect('listequipement')
        else:
            form=EquipementForms(request.POST or None,instance=equip)
            return render(request, 'equipementUpdate.html',{'form':form,'user':request.user,'equip':equip})
    else:
        form=EquipementForms(request.POST or None,instance=equip)
        return render(request, 'equipementUpdate.html',{'form':form,'user':request.user,'equip':equip})    
            
                
@login_required
def detailEquipement(request,pk):
    equip=get_object_or_404(Equipement,pk=pk)
    enceinte=Appartenir.objects.filter(equipement_id=pk)
    return render(request,'DetailEquipement.html',{'equip':equip,'user':request.user,'enceinte':enceinte})
    