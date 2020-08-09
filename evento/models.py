from django.db import models
from usuario.models import Usuario
import uuid

# Create your models here.
class Evento(models.Model):
    # Subclases para los enums
    class Categorias(models.TextChoices):        
        CONFERENCIA = 'CONFERENCE'
        CONGRESO = 'CONGRESS'
        SEMINARIO = 'SEMINAR'
        CURSO = 'COURSE'
    class Tipo(models.TextChoices):
        PRESENCIAL = 'PRESENCIAL'
        VIRTUAL = 'VIRTUAL'
    
    usuario = models.ForeignKey(Usuario, related_name='events', on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=256, null=False)
    event_category = models.CharField(max_length=20, null=False, choices=Categorias.choices)
    event_place = models.CharField(max_length=256, null=False)
    event_address = models.URLField(max_length=256)
    event_initial_date = models.DateTimeField()
    event_final_date = models.DateTimeField()
    event_type = models.CharField(max_length=20, null=False, choices=Tipo.choices)
    thumbnail = models.ImageField(upload_to='event_thumbnails/')    