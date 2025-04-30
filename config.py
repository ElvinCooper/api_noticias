import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False     # Desactiva el seguimiento de modificaciones de objetos para ahorrar recursos
    JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY", "default-secret")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    API_TITLE = "Contacts API"
    API_VERSION = "v1"
    OPENAPI_URL_PREFIX = "/"
 

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Clave secreta para sesiones, JWT etc..
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///mis_contactos.db")  
    FRONTEND_URL = "http://localhost:3000"


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
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"    
    JWT_SECRET_KEY = "test-secret"
    SECRET_KEY = "test"
    FRONTEND_URL = "http://localhost:3000"