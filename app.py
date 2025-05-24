from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
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
from rutes.paises_rutes import pais_bp
from rutes.post_categoria_rutes import post_cat_bp
from rutes.multimedia_rutes import multimedia_bp
import json
from sqlite_config import enable_sqlite_foreign_keys 
from datetime import timedelta

def create_app(testing=True):
    app = Flask(__name__)
    load_dotenv()

    # detectar el entorno desde .FLASKENV
    env = os.getenv("FLASK_ENV", "development")

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


    api = Api(app)

    # Iniciando las extensiones
    init_extensions(app)
    migrate = Migrate(app, db)

    # Blueprints     (en esta parte es donde agrego las rutas de los Endpoints con el prefijo api)
    api.register_blueprint(usuario_bp,  url_prefix='/api')
    api.register_blueprint(post_bp,     url_prefix='/api')
    api.register_blueprint(favorito_bp, url_prefix='/api')
    api.register_blueprint(categorias_bp, url_prefix='/api')
    api.register_blueprint(pais_bp, url_prefix='/api')
    api.register_blueprint(post_cat_bp, url_prefix='/api')
    api.register_blueprint(multimedia_bp, url_prefix='/api')


    from auth.jwt_callbacks import jwt
    jwt.init_app(app)

    from cli_comands import register_commands
    register_commands(app)

    return app

app = create_app()

if __name__ == '__main__':
    # with app.app_context():
    #     from seeds.init_data import seed_categorias, seed_roles, seed_paises
    #     db.create_all()         # crea las tablas si no existen
    #     seed_categorias()       # inserta las categorías base si no existen
    #     seed_roles()            # inserta los roles de usuario
    #     seed_paises()           # insertar los paises y sus detalles

    app.run()



    
