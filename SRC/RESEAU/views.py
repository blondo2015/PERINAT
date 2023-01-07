from django.shortcuts import render
from .models import *
from . import serializers
# les classes du drf
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response



def acceuil(request):
    return render(request,'Acceuil.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def Registeruser(request,code,format=None):
    if request.method == 'POST':        
        enceinte=""
        try:
            enceinte=Enceinte.objects.get(code=code)
            serializer=serializers.RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user=serializer.save()
                enuser=EncUser.objects.create(pointfocol=False)
                enuser.add(enceinte=enceinte,user=user)
                enuser.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
    # class RegisterView(ModelViewSet) :
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class =serializers.RegistrationSerializer