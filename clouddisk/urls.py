from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'signup$', views.signup),
    url(r'signin$', views.signin),
    url(r'handle_authorisation$', views.handle_authorisation_code),
    url(r'handle_audiocloud_authorisation$', views.handle_audio_cloud_authorisation_code),
    url(r'songs$', views.home_songs),
    url(r'logout$', views.custom_logout),
    url(r'$', views.home), 
]

urlpatterns += staticfiles_urlpatterns()