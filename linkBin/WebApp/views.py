from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from . import models
from django.urls import reverse

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
    user = models.User.objects.get(username=username)
    links = models.Link.objects.filter(id_user=user.id_user)[:5] #limiteaza la 5 linkuri
    link1 = links[0].link if len(links) >= 1 else None
    link2 = links[1].link if len(links) >= 2 else None
    link3 = links[2].link if len(links) >= 3 else None
    link4 = links[3].link if len(links) >= 4 else None
    link5 = links[4].link if len(links) >= 5 else None

    context = {
        'username': username,
        'data': user,
        'link1': link1,
        'link2' : link2,
        'link3': link3,
        'link4' :link4,
        'link5':link5

    }
    linkReq = str(request.path)
    if linkReq.find('/index/') != -1:
        return redirect('WebApp:index/avioane')
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

@login_required
def EditProfileRoute(request,username):
    data = models.User.objects.get(username=username)
    links = models.Link.objects.filter(id_user=data)[:5]

    if request.method == 'POST':
        if 'email_sumbit' in request.POST:
        # Primeste date din formuluar despre email
            new_email = request.POST.get('new_email')

            # Modifica email
            data.email = new_email
            data.save()
        elif 'bio_submit' in request.POST:
            new_bio = request.POST.get('new_bio')
        # Modifica bio
            data.bio = new_bio
            data.save()
        elif 'card_submit' in request.POST:
            new_card_code = request.POST.get('new_card')
        # Modifica card
            user_instance = models.User.objects.get(id_user=data.id_user)
            ownership = models.Ownership.objects.filter(id_user=user_instance).first()
            #Cele 2 instante fac legatura intre card si user
            if ownership: #caz in care actualizeaza
                ownership.id_card.key = new_card_code
                ownership.id_card.save()
            else: #creaza instanta noua de card si ownership
                new_card = models.Card()
                new_card.key = new_card_code
                new_card.save()

                new_ownership = models.Ownership()
                new_ownership.id_card = new_card
                new_ownership.id_user = user_instance
                new_ownership.save()
        elif any(link_form in request.POST for link_form in
                 ['link1_submit', 'link2_submit', 'link3_submit', 'link4_submit', 'link5_submit']): #parcurge toate formurile cu linkuri
            i = 0
            for link_form in ['link1_submit', 'link2_submit', 'link3_submit', 'link4_submit', 'link5_submit']:
                i += 1
                if link_form in request.POST:
                    new_link = request.POST.get(f'new_link{i}') #formatare link(n) unde n este linkul respectiv

                    if new_link:
                        old_instance =models.Link.objects.filter(id_user_id=data, index = i).first()
                        if old_instance: #caz in care actualizeaza link
                            old_instance.link = new_link
                            old_instance.save()
                        else: #creare instanta link
                            new_link_instance = models.Link()
                            new_link_instance.link = new_link
                            new_link_instance.id_user = data
                            new_link_instance.index = i
                            new_link_instance.save()
                        # Adauga link in context
                        setattr(data, f'link{i}', new_link)

            data.save()

            # Salvare date
            data.save()
        # Template pagina profile_edit
        template = loader.get_template('profile_edit.html')

        context = {          #context post formular
            'username': username,
            'data': data
        }

        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)
        return redirect('profile_edit/<str:username>/') #redirectionare post formular
    template = loader.get_template('profile_edit.html')
    data.link1 = links[0].link if len(links) >= 1 else None #completeaza cu none daca nu exista link
    data.link2 = links[1].link if len(links) >= 2 else None
    data.link3 = links[2].link if len(links) >= 3 else None
    data.link4 = links[3].link if len(links) >= 4 else None
    data.link5 = links[4].link if len(links) >= 5 else None
    context = {
        'username': username,
        'data': data
    }
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def ProfileRedirect(request, key):
    card = models.Card.objects.get(key=key)
    ownership = models.Ownership.objects.get(id_card=card.id_card)
    user = models.User.objects.get(id_user=ownership.id_user.id_user)
    return redirect("WebApp:profile", username=user.username)
