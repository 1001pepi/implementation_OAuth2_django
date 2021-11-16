from rest_framework import serializers

from .models import Song
from django.contrib.auth.models import User 

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'name', 'owner', 'song', 'created_at', 'update_at')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    songs = serializers.HyperlinkedRelatedField(many=True, view_name='song-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'songs']