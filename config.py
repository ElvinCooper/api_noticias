import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

class BaseConfig:

     # Configurar tiempos de expiracion para los token
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS = False     # Desactiva el seguimiento de modificaciones de objetos para ahorrar recursos
    JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY", "default-secret")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    API_TITLE = "API REST InfoNovaX"
    API_VERSION = "v1.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    
    FRONTEND_URL="http://localhost:3000"
 

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Clave secreta para sesiones, JWT etc..

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'infonovax.db')
    
    # Se ejecutará una vez al cargar la configuración.
    os.makedirs(os.path.dirname(db_path), exist_ok=True) 

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    FRONTEND_URL = "http://localhost:3000"


class ProductionConfig(BaseConfig):
    DEBUG = False
    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI debe estar definido en producción.")
    
    #FRONTEND_URL="http://localhost:3000" # ponerme de acuerdo con Jonathan.
    
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    if not FRONTEND_URL:
        raise ValueError("FRONTEND_URL debe estar definido en producción.")
    


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://infonovax_user:5CFyBwyKghRKWoIqhj19hZQAHIp1sRm0@dpg-d0qe6kre5dus739ge4g0-a.ohio-postgres.render.com/infonovax"    
    JWT_SECRET_KEY = "test-secret"
    SECRET_KEY = "test"
    FRONTEND_URL = "http://localhost:3000"