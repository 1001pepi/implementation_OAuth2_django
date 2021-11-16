from django.db import models

from django.contrib.auth.models import User
import uuid

# Create your models here.
class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, 
        related_name='songs',
        on_delete=models.CASCADE,
        verbose_name="musiques de l'utilisateur",
        null=False,
    )
    song = models.ImageField(upload_to='songs/')
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")