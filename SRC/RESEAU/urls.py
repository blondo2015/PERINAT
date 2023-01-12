from django.urls import path,include
from .views import *
from django.conf.urls.static import  static
from django.conf import settings
#from rest_framework_simplejwt import views as jwt_views


#router = routers.DefaultRouter()
# router.register(r'Register', RegisterView)

urlpatterns = [
    path('',acceuil,name='acceuil'), 
    path('api/Register',Register,name='Registeruser'), 
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/connexion/',CustomAuthTokenlogin.as_view(), name='apiconnexion'),  
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
