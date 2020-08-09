from rest_framework import serializers
from usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password')