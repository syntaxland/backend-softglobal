from django.urls import path
from . import views

urlpatterns = [
    path('user-register/', views.UserRegisterView.as_view(), name='user-register'),
    path('user-login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('user-logout/', views.LogoutView.as_view(), name='user-logout'),
    path('get-users/', views.GetAllUsersView.as_view(), name='get-users'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
