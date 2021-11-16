from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'signup$', views.signup),
    url(r'signin$', views.signin),
    url(r'signin_for_authorisation$', views.sign_in_for_authorisation),
    url(r'logout$', views.custom_logout),
    url(r'upload_song$', views.uploadSong),
    url(r'delete_song/(?P<id>.*)$', views.delete_song),
    url(r'$', views.home),
]

urlpatterns += staticfiles_urlpatterns()