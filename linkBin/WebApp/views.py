from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def PageRoute(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render()) #la request returneaza pagina web index

def RegisterRequest(request):
    template = loader.get_template('autentificare.html')
    return HttpResponse(template.render())

