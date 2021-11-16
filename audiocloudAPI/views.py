from django.db.models.query import QuerySet
from django.shortcuts import render

from rest_framework import viewsets

from .serializers import SongSerializer, UserSerializer 
from .models import Song
from django.contrib.auth.models import User 

from rest_framework import filters
from django.db.models import Q
from rest_framework.response import Response

from rest_framework import permissions

# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('name')
    serializer_class = SongSerializer

    def create(self, request):
        permission_classes = [permissions.IsAuthenticated]

        new_song = Song.objects.create(name=request.data['name'], owner=User.objects.get(id=request.data['owner_id']), song=request.data['song'])
        
        return Response(status=200)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = Song.objects.all()
        
        else:
            queryset = request.user.songs

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    filterset_fields = ["username", "password"]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def list(self, request, *args, **kwargs):
        username = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        query = Q()

        if username is not None:
            query.add(Q(username__exact = username), Q.AND)
        
        if password is not None:
            query.add(Q(password__exact = password), Q.AND)

        queryset = self.filter_queryset(self.get_queryset())

        if username or password:
            queryset = queryset.filter(query)
        
        if not request.user.is_staff:
            query = Q()
            query.add(Q(username__exact = request.user.username), Q.AND)

            queryset = self.filter_queryset(self.get_queryset())

            queryset = queryset.filter(query)
        
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)