import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="infonovax",
        password="info12345",
        database="midb"
    )
    print("✅ Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print("❌ Error de conexión:", e)
