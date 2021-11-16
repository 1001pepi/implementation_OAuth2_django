from django.db import models

from django.contrib.auth.models import User
import uuid

# Create your models here.
class Authorisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    owner = models.ForeignKey(
        User, 
        related_name='authorisations',
        on_delete=models.CASCADE,
        verbose_name="autorisations relatives à l'utilisateur",
        null=False,
    )
    application = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")