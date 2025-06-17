from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify
import os
from functools import wraps

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)


# Decorador para verificar API Key
def require_api_key():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Claves válidas
            VALID_API_KEYS = {os.getenv("FRONTEND_API_KEY"), "otra-key"}
            api_key = request.headers.get('X-API-KEY')
            if api_key not in VALID_API_KEYS:
                return jsonify({"error": "API Key inválida"}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator