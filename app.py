from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from extensions import init_extensions, db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config import TestingConfig, ProductionConfig, DevelopmentConfig
from rutes.user_rutes import usuario_bp
from rutes.post_rutes import post_bp
from rutes.favorito_rutes import favorito_bp
from rutes.categoria_rutes import categorias_bp
from rutes.paises_rutes import pais_bp
from rutes.post_categoria_rutes import post_cat_bp
from rutes.multimedia_rutes import multimedia_bp
from limiter import limiter



def create_app(testing=False):
    app = Flask(__name__)
    load_dotenv()

    # Cargar configuración por entorno
    env = os.getenv("FLASK_ENV", "production")

    app.config['SQLALCHEMY_ECHO'] = True  # Para que muestre los Querys que se ejecutan.

    if testing:
        app.config.from_object(TestingConfig)
    elif env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)


    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise ValueError(f"SQLALCHEMY_DATABASE_URI no está configurado para el entorno: {env}")
    
    # CORS dinámico desde config
    CORS(app, resources={
        r"/v1/*": {
            "origins": app.config["FRONTEND_URL"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    def schema_name_resolver(schema):
        return schema.__class__.__name__


    init_extensions(app)
    limiter.init_app(app)

    app.config.update({
        'API_TITLE': 'API Noticias',
        'API_VERSION': 'v1',
        'OPENAPI_VERSION': '3.0.2',
    })

    
    api = Api(app)
    
    Migrate(app, db)

    # Registrar blueprints
    api.register_blueprint(usuario_bp, url_prefix='/api/v1')
    api.register_blueprint(post_bp, url_prefix='/api/v1')
    api.register_blueprint(favorito_bp, url_prefix='/api/v1')
    api.register_blueprint(categorias_bp, url_prefix='/api/v1')
    api.register_blueprint(pais_bp, url_prefix='/api/v1')
    api.register_blueprint(post_cat_bp, url_prefix='/api/v1')
    api.register_blueprint(multimedia_bp, url_prefix='/api/v1')   

    # JWT & comandos CLI
    from auth.jwt_callbacks import jwt
    jwt.init_app(app)

    from cli_comands import register_commands
    register_commands(app)

    return app

app = create_app(testing=False)

if __name__ == '__main__':
    app.run()



    
