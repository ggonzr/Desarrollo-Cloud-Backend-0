from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=256, primary_key=True, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=256)