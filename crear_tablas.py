from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Todas las tablas han sido creadas en la base de datos.")
