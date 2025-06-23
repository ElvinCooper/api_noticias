from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify
import os
from functools import wraps

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)

# Obtener la API key desde la variable de entorno
FRONTEND_API_KEY = os.getenv("FRONTEND_API_KEY")

# Claves válidas
VALID_API_KEYS = set()
if FRONTEND_API_KEY:
    VALID_API_KEYS.add(FRONTEND_API_KEY)
VALID_API_KEYS.add("otra-key")

# Decorador para verificar API Key
def require_api_key():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-KEY')
            # print("HEADERS:", dict(request.headers))
            # print("API_KEY RECIBIDA:", api_key)
            # print("VALID_KEYS:", VALID_API_KEYS)
            if not api_key or api_key not in VALID_API_KEYS:
                return jsonify({"error": "API Key inválida o no proporcionada"}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator