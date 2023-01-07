from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'Register', RegisterView)

urlpatterns = [
    path('',acceuil,name='acceuil'), 
    path('api/', include(router.urls)), 
]