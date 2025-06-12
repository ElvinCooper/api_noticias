from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app
from flask import request, jsonify
import os

# Configurar rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]  # Límite general
)

# Claves válidas
VALID_API_KEYS = {os.getenv("FRONTEND_APY_KEY"), "otra-key"}


# Decorador para verificar API Key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "API Key inválida"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Necesario para Flask
    return wrapper