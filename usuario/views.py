from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from usuario.serializers import UsuarioSerializer
from usuario.models import Usuario
from backend.settings import SECRET_KEY
from backend.auth import authenticate
import jwt
import datetime

# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def create_user(request):            
    print(request.data)
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid(): #Valida que los datos dados por el request sean validos
        serializer.save() #Guarda el objeto dado
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@parser_classes([FormParser])
@csrf_exempt
def api_auth(request):    
    try:
        usuario = Usuario.objects.get(pk=request.data['username'], password=request.data['password'])
    except Usuario.DoesNotExist:
        return JsonResponse({"message": "User not found or password is not valid"}, status=404)
    
    payload = {
        'username': request.data['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }    
    token = jwt.encode(payload, SECRET_KEY).decode('utf-8')
    return JsonResponse({'token': token}, status=200)


@api_view(['GET'])
@csrf_exempt
@authenticate()
def get_users(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return JsonResponse(serializer.data, safe=False)
    