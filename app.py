from flask import Flask
from flask_cors import CORS
from extensions import init_extensions, db, migrate
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flasgger import Swagger
from config import TestingConfig, ProductionConfig, DevelopmentConfig




def create_app(testing=True):
    app = Flask(__name__)
    load_dotenv()

    # detectar el entorno desde .FLASKENV
    env = os.getenv("FLASK_ENV", "development")

    # detectar el entorno desde .FLASKENV
    env = os.getenv("FLASK_ENV", "development")

    if testing:
        app.config.from_object(TestingConfig)
    elif env == "production":    
        app.config.from_object(ProductionConfig)
        
    else:
        app.config.from_object(DevelopmentConfig) 


    # Inicializar CORS para permitir solicitudes desde el frontend
    frontend_url = app.config.get('FRONTEND_URL', 'http://localhost:3000')  # Valor por defecto
    if not frontend_url:
        raise ValueError("FRONTEND_URL debe estar definido en la configuración.")    


    # Inicializar CORS para permitir solicitudes desde el frontend
    CORS(app, resources={r"/api/*": {"origins": frontend_url,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }})


    # Iniciando las extensiones
    init_extensions(app)
    migrate = Migrate(app, db)


    # Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API REST InfoNovaX",
            "description": "Documentación Swagger de la API de InfoNovaX en Flask",
            "version": "1.0"
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token JWT usando el esquema Bearer. Ejemplo: 'Bearer {token}'"
            }
        }
    }

    Swagger(app, template=swagger_template)  


    # Blueprints     (en esta parte es donde agrego las rutas de los Endpoints)



    return app

app = create_app()



    
