from rest_framework import serializers

from .models import Image
from django.contrib.auth.models import User 

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'owner', 'image', 'created_at', 'update_at')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.HyperlinkedRelatedField(many=True, view_name='image-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'images']