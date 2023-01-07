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
def Register(request, *args, **kwargs):
    if request.method == 'POST':        
        serializer=serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
    # class RegisterView(ModelViewSet) :
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class =serializers.RegistrationSerializer