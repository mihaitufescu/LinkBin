from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from . import models

app_name = 'WebApp'

def PageRoute(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render()) #la request returneaza pagina web index

#Metoda pentru redirectionare catre formularul de inregistrare
def RegisterRequest(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("WebApp:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    context = {
        'register_form': form
    }
    template = loader.get_template('register.html')
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def LoginRequest(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("WebApp:profile_edit", username=username)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {
        'login_form': form
    }
    template = loader.get_template('login.html')
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def ProfileRoute(request,username):
    template = loader.get_template('profile.html')
    context = {
        'username': username
    }
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def EditProfileRoute(request,username):
    template = loader.get_template('profile_edit.html')
    data = models.User.objects.get(username=username)
    context = {
        'username': username,
        'data': data
    }
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)