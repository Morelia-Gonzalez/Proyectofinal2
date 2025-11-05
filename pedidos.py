# pedidos.py
from conexion import crear_conexion
from colorama import Fore

class Pedido:
    def __init__(self, cliente, productos):
        self.cliente = cliente
        self.productos = productos
        self.total = sum(p['precio'] * p['cantidad'] for p in productos)
        self.envio = 15.00  # costo fijo de envío
        self.total_final = self.total + self.envio

    def mostrar_detalle(self):
        print(Fore.CYAN + "\n--- DETALLE DEL PEDIDO ---")
        for p in self.productos:
            print(f"{p['nombre']} x{p['cantidad']} = Q{p['precio'] * p['cantidad']}")
        print(f"\nSubtotal: Q{self.total}")
        print(f"Envío: Q{self.envio}")
        print(Fore.GREEN + f"Total a pagar: Q{self.total_final}")

    def guardar_pedido(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, total) VALUES (%s, %s)", (self.cliente, self.total_final))
        conexion.commit()
        cursor.close()
        conexion.close()
        print(Fore.GREEN + "Pedido registrado correctamente en la base de datos.")
