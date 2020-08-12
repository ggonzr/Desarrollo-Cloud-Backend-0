from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from backend.settings import SECRET_KEY
from backend.auth import authenticate
from evento.serializers import EventoSerializer
from evento.models import Evento
from usuario.models import Usuario

@csrf_exempt
def event_list(request, *args, **kwargs):
    if request.method == 'POST':
        return create_event(request, args)
    elif request.method == 'GET':
        return get_user_events(request, args)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
@authenticate()
def create_event(request, *args, **kwargs):
    #Buscar el objeto de usuario para anexarle el evento       
    request_data = request.data.dict()
    request_data['usuario'] = kwargs['username']                            
    serializer = EventoSerializer(data=request_data)
    if serializer.is_valid(): #Valida que los datos dados por el request sean validos
        serializer.save() #Guarda el objeto dado
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@csrf_exempt
@authenticate()
def get_user_events(request, *args, **kwargs):    
    events = Evento.objects.filter(usuario=kwargs['username']).order_by('-event_initial_date')
    serializer = EventoSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False) 

@csrf_exempt
def event_detail(request, pk, *args, **kwargs):
    #Guardar el PK en el diccionario de parametros opcionales
    #Al pasar por el decorador, el parametro se pierde y queda asignado pura basura logica
    kwargs['pk'] = pk     

    if request.method == 'GET':
        return event_detail_get(request, *args, **kwargs)
    elif request.method == 'PUT':
        return event_detail_put(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return event_detail_delete(request, *args, **kwargs)

@api_view(['GET'])
@csrf_exempt
@authenticate()
def event_detail_get(request, *args, **kwargs):        
    try:
        event = Evento.objects.get(usuario=kwargs['username'], pk=kwargs['pk'])        
    except Evento.DoesNotExist:
        return JsonResponse({'message': 'El evento no existe'}, status=404)        
    else:
        print("El evento existe")
        serializer = EventoSerializer(event)
        return JsonResponse(serializer.data)

@api_view(['PUT'])
@parser_classes([MultiPartParser])
@csrf_exempt
@authenticate()
def event_detail_put(request, *args, **kwargs):     
    event = Evento.objects.get(usuario=kwargs['username'], pk=kwargs['pk'])
    serializer = EventoSerializer(event, data=request.data, partial=True)
    if serializer.is_valid(): #Valida que los datos dados por el request sean validos
        serializer.save() #Guarda el objeto dado
        return JsonResponse(serializer.data, status=202)
    return JsonResponse(serializer.errors, status=400)

@api_view(['DELETE'])
@csrf_exempt
@authenticate()
def event_detail_delete(request, *args, **kwargs): 
    try:
        event = Evento.objects.get(usuario=kwargs['username'], pk=kwargs['pk'])
        serializer = EventoSerializer(event)
        copy = serializer.data
        event.delete()
        return JsonResponse(copy, safe=False)
    except Evento.DoesNotExist:
        return JsonResponse({'message': 'El evento no existe'}, status=404)
