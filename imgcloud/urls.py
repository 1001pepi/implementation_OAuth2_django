from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'signup$', views.signup),
    url(r'signin$', views.signin),
    url(r'signin_for_authorisation$', views.sign_in_for_authorisation),
    url(r'logout$', views.custom_logout),
    url(r'upload_image$', views.uploadImage),
    url(r'delete_image/(?P<id>.*)$', views.delete_image),
    url(r'$', views.home),
]

urlpatterns += staticfiles_urlpatterns()