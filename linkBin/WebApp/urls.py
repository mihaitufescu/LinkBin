from django.urls import path
from . import views
from django.urls import re_path
app_name = 'WebApp'
urlpatterns = [
    path('index/', views.PageRoute, name="index"),
    path('', views.PageRoute, name="index"),
    re_path(r'^index/$', views.PageRoute, name='index'),
    path('register/',views.RegisterRequest,name='register'),
    path('login/',views.LoginRequest,name='login'),
    path('profile_edit/<str:username>/',views.EditProfileRoute,name='profile_edit'),
    path('profile/key/<str:key>/', views.ProfileRedirect, name='profile_redirect'),
    path('profile/<str:username>/',views.ProfileRoute,name='profile')

]