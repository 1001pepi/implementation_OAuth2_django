from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import forms, authenticate, login, logout
from django.shortcuts import redirect, render  
from django.contrib import messages  

from .components.forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.models import User

import requests
from .models import Authorisation
from .API_links import API_links
# Create your views here.  
    
def signup(request):  
    """
    fonction de création de compte
    """

    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()
            return redirect('/clouddisk/signin')  
        else:
            return render(request, 'clouddisk/signup.html', {'form': form})  

    else:  
        form = CustomUserCreationForm()  
       
    context = {  
        'form':form  
    }  

    return render(request, 'clouddisk/signup.html', context)

def signin(request):
    """
    fonction de connexion d'un utilisateur
    """

    if request.method == 'POST': 
        form = CustomUserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        tmp_user = User.objects.filter(username = username)  

        if not tmp_user.count():
            return render(request, 'clouddisk/signin.html', {'form': form, 'message': "Username incorrect!!"})

        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/clouddisk') 
        
            else:
                return render(request, 'clouddisk/signin.html', {'form': form, 'message': "Password incorrect!!"})
    else:  
        form = CustomUserLoginForm()

    return render(request, 'clouddisk/signin.html', {'form': form}) 


def custom_logout(request):
    """
    fonction de déconnexion d'un utilisateur
    """

    logout(request)

    return redirect('/clouddisk/signin') 


def home(request):
    """
    fonction permettant d'accéder à la page d'accueil
    """

    current_user = request.user

    if Authorisation.objects.filter(owner=current_user, application='imgCloud').exists():
        authorisation = Authorisation.objects.get(owner=current_user, application='imgCloud')

        images = getUserImages(authorisation)

    else:
        images = []

    if current_user.is_authenticated:
       return render(request, 'clouddisk/home_image.html', {"current_user": current_user, "images":images}) 

    else:
        return redirect('/clouddisk/signin') 

def home_songs(request):
    """
    fonction permettant d'accéder à la page d'accueil
    """

    current_user = request.user

    if Authorisation.objects.filter(owner=current_user, application='audioCloud').exists():
        authorisation = Authorisation.objects.get(owner=current_user, application='audioCloud')

        songs = getUserSongs(authorisation)

    else:
        songs = []

    if current_user.is_authenticated:
       return render(request, 'clouddisk/home_song.html', {"current_user": current_user, "songs":songs}) 

    else:
        return redirect('/clouddisk/signin') 


def handle_authorisation_code(request):
    """
    fonction pour récupérer le code d'autorisation
    """

    if 'code' in request.GET:
        authorisation_code = request.GET['code']

        request_link = "http://127.0.0.1:8000/o/token/"

        result = requests.post(request_link, data={
            'client_id':'yhfZi6cl05r4PtozlvIGoSlK9xtsJhiFemXkaADn',
            'client_secret':'F2YbDUHbMbd30ertUcs4hzh3j1HCceMvTYwC5RoFGasrLajRVnBgVSnOGJm0txswUNTooXGSMdoqrV09NvADVRKn5qYrlQgfTEmNO4V27xvQpenFv3pWgTvTRNKkDvls',
            'code': authorisation_code,
            'grant_type':'authorization_code',
        }, allow_redirects=True)

        if result.status_code == 200:
            if Authorisation.objects.filter(owner_id=request.user.id, application="imgCloud").exists():
                Authorisation.objects.get(owner_id=request.user.id, application="imgCloud").delete()

            Authorisation.objects.create(owner=request.user, application='imgCloud', access_token=result.json()['access_token'])

    return redirect('/clouddisk/')

def handle_audio_cloud_authorisation_code(request):
    """
    fonction pour récupérer le code d'autorisation
    """

    if 'code' in request.GET:
        authorisation_code = request.GET['code']

        request_link = "http://127.0.0.1:8002/o/token/"

        result = requests.post(request_link, data={
            'client_id':'08KX5jBb0oIt4XyNJwFeolufhP1eYK9BtWTT6bmQ',
            'client_secret':'WFLO7Xqd7VEG9uiqmiLnhtChYwUlB9ICSA03BUFLYqEAsKUxW01ffx9KZ6EAhXfeUpVR3aJ9fAbgDyEjRizRU4bLH5kLdwxlWKqZyNMGXGsXx1Y8UthbNgsngRnTojbV',
            'code': authorisation_code,
            'grant_type':'authorization_code',
        }, allow_redirects=True)

        if result.status_code == 200:
            if Authorisation.objects.filter(owner_id=request.user.id, application="audioCloud").exists():
                Authorisation.objects.get(owner_id=request.user.id, application="audioCloud").delete()

            Authorisation.objects.create(owner=request.user, application='audioCloud', access_token=result.json()['access_token'])

    return redirect('/clouddisk/songs')


def getUserImages(authorisation):
    """
    fonction pour récupérer la liste des images de l'utilisateur
    """

    request_link = API_links.images_link
    headers = {"Authorization": "Bearer " + authorisation.access_token}

    result = requests.get(request_link, headers=headers)

    return result.json()

def getUserSongs(authorisation):
    """
    fonction pour récupérer la liste des images de l'utilisateur
    """

    request_link = API_links.songs_link
    headers = {"Authorization": "Bearer " + authorisation.access_token}

    result = requests.get(request_link, headers=headers)

    return result.json()

   