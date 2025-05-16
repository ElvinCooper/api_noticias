from flask import current_app
from extensions import db

def register_commands(app):
    @app.cli.command("db_create")
    def db_create():
        with app.app_context():
            db.create_all()
            print("Base de datos creada en:", app.config["SQLALCHEMY_DATABASE_URI"])

    @app.cli.command("db_drop")
    def db_drop():
        with app.app_context():
            db.drop_all()
            print("Base de datos eliminada")

    @app.cli.command("seed_categorias")
    def seed_categorias():
        from seeds.seed_categoria import cargar_categorias
        cargar_categorias()
