# conexion.py
import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",         # usuario de MySQL
            password="",         # deja vacío si no tienes contraseña
            database="creative_designs"
        )
        print(" Conexión exitosa.")
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None
