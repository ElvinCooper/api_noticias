# from app import create_app
# from extensions import db

# app = create_app(testing=False)

# with app.app_context():
#     db.create_all()
#     print("✅ Todas las tablas han sido creadas en la base de datos.")


import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Testing_infonovax",
        user="postgres",
        password="KYEpostgres301020",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print(f"Error: {e}")