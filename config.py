import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class BaseConfig:
    # Configurar tiempos de expiración para los tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    API_TITLE = "API REST InfoNovaX"
    API_VERSION = "v1.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
    # Configuración para PostgreSQL local
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DEV_DATABASE_URI debe estar definido en desarrollo.")
    
class ProductionConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI debe estar definido en producción.")
    
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    if not FRONTEND_URL:
        raise ValueError("FRONTEND_URL debe estar definido en producción.")


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = "test-secret"
    SECRET_KEY = "test"
    FRONTEND_URL = "http://localhost:3000"