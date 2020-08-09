from rest_framework import serializers
from usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'events')