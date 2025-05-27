from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    result = db.session.execute(text("SELECT NOW();"))
    print("✅ Conexión exitosa. Tiempo actual en la base de datos:", list(result))
