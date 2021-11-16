from django.urls import include, path
from rest_framework import routers
from . import views

from rest_framework.decorators import api_view, permission_classes

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)
router.register(r'users', views.UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]