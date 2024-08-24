from psycopg2.extras import RealDictCursor
import psycopg2

# Conexão com o PostgreSQL
def get_db():
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        yield conn
    finally:
        conn.close()