from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.PageRoute, name="index"),
    path('', views.PageRoute, name="index")
]