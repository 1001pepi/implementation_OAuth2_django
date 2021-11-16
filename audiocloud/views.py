from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import forms, authenticate, login, logout
from django.shortcuts import redirect, render  
from django.contrib import messages  

from .components.forms import CustomUserCreationForm, CustomUserLoginForm, UploadSongForm
from django.contrib.auth.models import User  

import requests
from .API_links import API_links

# Create your views here.  
    
def signup(request):  
    """
    fonciton de création de compte
    """

    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()
            return redirect('/audiocloud/signin')  
        else:
            return render(request, 'audiocloud/signup.html', {'form': form})  

    else:  
        form = CustomUserCreationForm()  
       
    context = {  
        'form':form  
    }  

    return render(request, 'audiocloud/signup.html', context) 


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
            return render(request, 'audiocloud/signin.html', {'form': form, 'message': "Username incorrect!!"})

        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/audiocloud/') 
        
            else:
                return render(request, 'audiocloud/signin.html', {'form': form, 'message': "Password incorrect!!"})
    else:  
        form = CustomUserLoginForm()

    return render(request, 'audiocloud/signin.html', {'form': form}) 

def sign_in_for_authorisation(request):
    """
    fonction de connexion d'un utilisateur pour une confirmation d'autorisation
    """
    if request.method == 'POST': 
        form = CustomUserLoginForm(request.POST)
        
        username = request.POST['username']
        password = request.POST['password']

        tmp_user = User.objects.filter(username = username)  

        if not tmp_user.count():
            return render(request, 'audiocloud/signin.html', {'form': form, 'message': "Username incorrect!!"})

        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user) 
                return redirect(request.GET['next']) 
        
            else:
                return render(request, 'audiocloud/signin.html', {'form': form, 'message': "Password incorrect!!"})
    else:  
        form = CustomUserLoginForm()

    return render(request, 'audiocloud/signin.html', {'form': form})


def custom_logout(request):
    """
    fonction de déconnexion d'un utilisateur
    """
    
    logout(request)
   
    return redirect('/audiocloud/signin') 


def home(request):
    """
    fonction permettant d'accéder à la page d'accueil
    """

    current_user = request.user

    if current_user.is_authenticated:
        songs = getUserSongs(current_user.id)

        return render(request, 'audiocloud/home.html', {"current_user": current_user, "songs": songs, "delete_song": delete_song}) 

    else:
        return redirect('/audiocloud/signin')


def getUserSongs(userId):
    """
    fonction pour récupérer la liste des images de l'utilisateur
    """

    request_link = API_links.users_link + str(userId) + "/"

    result = requests.get(request_link)

    #construction de la liste des images de l'utilisateur
    songs = []

    for link in result.json()['songs']:
        songs.append(requests.get(link).json())

    return songs


def uploadSong(request):
    """
    fonction pour uploader une image
    """
    if request.method == 'POST': 
        form = UploadSongForm(request.POST, request.FILES)
        name = request.FILES['song'].name
        song = request.FILES['song']

        request_link = API_links.songs_link

        data={
            'name': name,
            'owner_id':request.user.id,
        }

        upload = {
            'song': song,
        }
        
        result = requests.post(request_link, data=data, files=upload)

        return redirect('/audiocloud/') 

    return render(request, 'audiocloud/upload_song_form.html', {'form': UploadSongForm()})


def delete_song(request, id):
    """
    function to delete an image
    """

    request_link = API_links.songs_link + id

    result = requests.delete(request_link)
    
    return redirect('/audiocloud/') 