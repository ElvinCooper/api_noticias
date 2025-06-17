from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify
import os
from functools import wraps

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)


# Decorador para verificar API Key
from functools import wraps
from flask import request, jsonify
import os

def require_api_key():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            valid_keys = {os.getenv("FRONTEND_API_KEY"), "otra-key"}
            api_key = request.headers.get('X-API-KEY')
            print("HEADERS:", dict(request.headers))
            print("API_KEY RECIBIDA:", api_key)  # ← log crítico
            print("VALID_KEYS:", valid_keys)     # ← log crítico
            if api_key not in valid_keys:
                return jsonify({"error": "API Key inválida"}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator
