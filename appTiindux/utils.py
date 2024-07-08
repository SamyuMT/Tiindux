import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def fetch_data_to_dataframe(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(data, columns=columns)


class Categoria:
    def __init__(self, connection):
        self.df_categorias = self.load_categorias(connection)

    def load_categorias(self, connection):
        query = "SELECT * FROM mdl_course_categories"
        df = fetch_data_to_dataframe(connection, query)
        return df

class Curso:
    def __init__(self, connection):
        self.df_cursos = self.load_cursos(connection)

    def load_cursos(self, connection):
        query = "SELECT * FROM mdl_course"
        df = fetch_data_to_dataframe(connection, query)
        return df

class Consulta:
    def __init__(self, categoria, curso):
        self.categoria = categoria
        self.curso = curso

    def contar_categorias(self):
        df_filtrado = self.categoria.df_categorias[self.categoria.df_categorias['idnumber'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)]
        lista_idnumbers = df_filtrado['idnumber'].tolist()
        return len(lista_idnumbers), lista_idnumbers

    def contar_cursos_en_categoria(self, categoria_id):
        cursos_en_categoria = self.curso.df_cursos[self.curso.df_cursos['category'] == categoria_id]
        return len(cursos_en_categoria), cursos_en_categoria['fullname'].tolist()
    
    def usuarios_por_curso(self, curso_id):
        usuario_curso