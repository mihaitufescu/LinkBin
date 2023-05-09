
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include('WebApp.urls')), #face legatura cu url-urile din aplicatia web
    path('admin/', admin.site.urls)
]
