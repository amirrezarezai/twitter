from django.urls import path
from . import views

urlpatterns = [
    # authenticate
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='get-token'),
    path('register/', views.registration_views, name='register'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    # profiles
    path('profiles/', views.ProfileList.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    # change
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('change-username/', views.ChangeUsernameView.as_view(), name='change-username'),
]