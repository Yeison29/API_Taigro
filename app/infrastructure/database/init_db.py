from sqlalchemy import text
from app.domain.models.country_model import Country, Base
from app.domain.models.department_model import Department
from app.domain.models.municipality import Municipality
from app.domain.models.user_model import User
from app.domain.models.auth_model import Auth
from app.domain.models.gender_model import Gender
from . import engine, get_db


def init_db():
    Base.metadata.create_all(engine)
    execute_sql_file(r'INSERT.sql')


def execute_sql_file(file_path):
    # Leer el archivo SQL
    with open(file_path, 'r', encoding='utf-8') as file:
        queries = file.read().split(';')  # Divide por punto y coma para obtener las consultas

    # Obtener una sesión manualmente fuera del contexto de FastAPI
    db_gen = get_db()
    conn = next(db_gen)  # Obtiene la sesión

    try:
        # Comenzar la transacción
        conn.begin()
        for query in queries:
            if query.strip():  # Evitar consultas vacías
                conn.execute(text(query))  # Ejecutar la consulta
        conn.commit()  # Confirmar la transacción
    except Exception as e:
        conn.rollback()  # Deshacer la transacción si ocurre un error
        print(f"Error: {e}")
    finally:
        db_gen.close()  # Asegurarse de cerrar la sesión
