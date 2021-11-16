from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import forms, authenticate, login, logout
from django.shortcuts import redirect, render  
from django.contrib import messages  

from .components.forms import CustomUserCreationForm, CustomUserLoginForm, UploadImageForm
from django.contrib.auth.models import User  

import requests
from imgcloudAPI.models import Image
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

            return redirect('/imgcloud/signin')  
        else:
            return render(request, 'imgcloud/signup.html', {'form': form})  

    else:  
        form = CustomUserCreationForm()  
       
    context = {  
        'form':form  
    }  

    return render(request, 'imgcloud/signup.html', context) 


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
            return render(request, 'imgcloud/signin.html', {'form': form, 'message': "Username incorrect!!"})

        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/imgcloud/') 
        
            else:
                return render(request, 'imgcloud/signin.html', {'form': form, 'message': "Password incorrect!!"})
    else:  
        form = CustomUserLoginForm()

    return render(request, 'imgcloud/signin.html', {'form': form}) 

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
            return render(request, 'imgcloud/signin.html', {'form': form, 'message': "Username incorrect!!"})

        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user) 
                return redirect(request.GET['next']) 
        
            else:
                return render(request, 'imgcloud/signin.html', {'form': form, 'message': "Password incorrect!!"})
    else:  
        form = CustomUserLoginForm()

    return render(request, 'imgcloud/signin.html', {'form': form})


def custom_logout(request):
    """
    fonction de déconnexion d'un utilisateur
    """
    
    logout(request)
    print("hie")
    return redirect('/imgcloud/signin') 


def home(request):
    """
    fonction permettant d'accéder à la page d'accueil
    """

    current_user = request.user

    if current_user.is_authenticated:
        images = getUserImages(current_user.id)

        return render(request, 'imgcloud/home.html', {"current_user": current_user, "images": images, "delete_image": delete_image}) 

    else:
        return redirect('/imgcloud/signin')


def getUserImages(userId):
    """
    fonction pour récupérer la liste des images de l'utilisateur
    """

    request_link = API_links.users_link + str(userId) + "/"

    result = requests.get(request_link)

    #construction de la liste des images de l'utilisateur
    images = []

    for link in result.json()['images']:
        images.append(requests.get(link).json())

    return images


def uploadImage(request):
    """
    fonction pour uploader une image
    """
    if request.method == 'POST': 
        form = UploadImageForm(request.POST, request.FILES)
        name = request.FILES['image'].name
        image = request.FILES['image']

        request_link = API_links.images_link

        data={
            'name': name,
            'owner_id':request.user.id,
        }

        upload = {
            'image': image,
        }
        
        result = requests.post(request_link, data=data, files=upload)

        return redirect('/imgcloud/') 

    return render(request, 'imgcloud/upload_image_form.html', {'form': UploadImageForm()})


def delete_image(request, id):
    """
    function to delete an image
    """

    request_link = API_links.images_link + id

    result = requests.delete(request_link)
    
    return redirect('/imgcloud/') 