import jwt
from backend.settings import SECRET_KEY
from django.http import JsonResponse

# Permite validar el token del usuario para consumir los servicios del backend de acuerdo a sus 
# permisos. En caso de ser satisfactorio retorna el ID del usuario.
# Header: Bearer - Token

def authenticate(*args):    
    def decorator(function):
        def wrap(request, *args):
            print("Authentication Decorator")   
            print("Request Header", request.headers)                 
            token = request.headers.get('Authorization')
            print("Token", token)        
            if token is None:
                print("Token no suministrado")
                msg = 'Invalid token header. No credentials provided.'
                return JsonResponse({'Error': msg}, status=401)
            try:
                token.encode('utf-8')
            except UnicodeError:
                print("Error de caracteres en el token")
                msg = 'Invalid token header. Token string should not contain invalid characters.'
                return JsonResponse({'Error': msg}, status=401)
            else:
                username = None
                try: 
                    token = token.strip().split(' ')[1]          
                    payload = jwt.decode(token, SECRET_KEY)
                    username = payload['username']                    
                except jwt.DecodeError:            
                    msg = 'Invalid token provided'
                    print(msg)
                    return JsonResponse({'Error': msg}, status=401)
                except jwt.ExpiredSignatureError:
                    msg = 'Invalid token provided. The token has expired'
                    print(msg)
                    return JsonResponse({'Error': msg}, status=401)

                #Token Valido - Devolver el cuerpo    
                #El único elemento en la tupla es el nombre de usuario
                else:
                    args = (username)
                    return function(request, *args)                                
        return wrap
    return decorator
