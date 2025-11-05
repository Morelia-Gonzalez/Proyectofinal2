# conexion.py
import mysql.connector

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",         # cambia si tu usuario MySQL es diferente
            password="",         # coloca tu contraseña si tienes
            database="creative_designs"
        )
        return conexion
    except mysql.connector.Error as e:
        print("Error de conexión:", e)
        return None
