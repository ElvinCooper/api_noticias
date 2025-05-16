from flask import Flask
from flask_cors import CORS
from extensions import init_extensions, db, migrate
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flasgger import Swagger
from config import TestingConfig, ProductionConfig, DevelopmentConfig
from rutes.user_rutes import usuario_bp
from rutes.post_rutes import post_bp
from rutes.favorito_rutes import favorito_bp
from rutes.categoria_rutes import categorias_bp
import json
from sqlite_config import enable_sqlite_foreign_keys 
from datetime import timedelta

def create_app(testing=True):
    app = Flask(__name__)
    load_dotenv()


    # detectar el entorno desde .FLASKENV
    env = os.getenv("FLASK_ENV")

    # Activar soporte de claves foráneas en SQLite
    enable_sqlite_foreign_keys()

    # Configurar tiempos de expiracion para los token
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)


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


    
    CORS(app, resources={r"/api/*": {"origins": frontend_url,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }})



     # Importacion de los modelos para evitar problemas de mapping
    from modelos.user_model import Usuario
    from modelos.rol_model import Rol
    from modelos.post_model import Post
    from modelos.favorito_model import Favorito
    from modelos.pais_model import Pais
    from modelos.multimedia_model import Multimedia
    from modelos.post_categoria_model import PostCategoria
    from modelos.categoria_model import Categoria


    # Iniciando las extensiones
    init_extensions(app)
    migrate = Migrate(app, db)

    with open("docs/swagger_definitions.json") as f:
        definitions = json.load(f)
        if "definitions" not in definitions:
            raise KeyError("El archivo swagger_definitions.json debe tener una clave 'definitions' en la raíz")

        swagger_template = {
            "swagger": "2.0",
            "info": {
                "title": "API REST InfoNovaX",
                "description": "Documentación de la API InfoNovaX hecha con Python y Flask",
                "version": "1.0"
            },
            "securityDefinitions": {
                "BearerAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Token JWT usando el esquema Bearer. Ejemplo: 'Bearer {token}'"
                }
            },
            "definitions": definitions["definitions"]
        }

        Swagger(app, template=swagger_template)



    # Blueprints     (en esta parte es donde agrego las rutas de los Endpoints con el prefijo api)
    app.register_blueprint(usuario_bp,  url_prefix='/api')
    app.register_blueprint(post_bp,     url_prefix='/api')
    app.register_blueprint(favorito_bp, url_prefix='/api')
    app.register_blueprint(categorias_bp, url_prefix='/api')


    from auth.jwt_callbacks import jwt
    jwt.init_app(app)

    from cli_comands import register_commands
    register_commands(app)

    return app



if __name__ == '__main__':
    app = create_app()


with app.app_context():
    from seeds.init_data import seed_categorias, seed_roles, seed_paises
    db.create_all()         # crea las tablas si no existen
    seed_categorias()       # inserta las categorías base si no existen
    seed_roles()            # inserta los roles de usuario
    seed_paises()           # insertar los paises y sus detalles

app.run(debug=True)



    
