# main.py
from colorama import Fore, Style, init
from productos_manager import ProductoManager
from pedidos import Pedido
from conexion import crear_conexion

init(autoreset=True)
convert = True

def menu_cliente():
    manager = ProductoManager()
    while True:
        print(Fore.CYAN + "\n--- MENÚ CLIENTE ---")
        print("1. Ver productos")
        print("2. Buscar producto")
        print("3. Cotizar pedido")
        print("4. Realizar pedido")
        print("5. Salir")
        opcion = input(Fore.YELLOW + "Seleccione una opción: ")

        if opcion == "1":
            manager.mostrar_productos()
        elif opcion == "2":
            termino = input("Ingrese nombre del producto: ")
            manager.buscar_producto(termino)
        elif opcion == "3":
            productos = manager.obtener_productos_para_pedido()
            if productos:
                pedido = Pedido("Cliente genérico", productos)
                pedido.mostrar_detalle()
        elif opcion == "4":
            productos = manager.obtener_productos_para_pedido()
            if productos:
                pedido = Pedido("Cliente genérico", productos)
                pedido.mostrar_detalle()
                pedido.guardar_pedido()
        elif opcion == "5":
            print("Saliendo del menú cliente...")
            break
        else:
            print(Fore.RED + "Opción inválida.")


def menu_admin():
    manager = ProductoManager()
    while True:
        print(Fore.BLUE + "\n--- MENÚ ADMINISTRADOR ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Consultar productos")
        print("4. Ver conteo de ventas")
        print("5. Salir")
        opcion = input(Fore.YELLOW + "Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            precio = float(input("Precio: "))
            manager.agregar_producto(nombre, precio)
        elif opcion == "2":
            id_producto = int(input("ID del producto: "))
            manager.eliminar_producto(id_producto)
        elif opcion == "3":
            manager.mostrar_productos()
        elif opcion == "4":
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            total = cursor.fetchone()[0]
            print(f"\nTotal de ventas registradas: {total}")
            conexion.close()
        elif opcion == "5":
            print("Saliendo del menú administrador...")
            break
        else:
            print(Fore.RED + "Opción inválida.")


def main():
    print(Fore.WHITE + Style.BRIGHT + "\nSISTEMA DE VENTAS - CREATIVE DESIGNS")
    while True:
        print(Fore.WHITE + "\n1. Cliente")
        print("2. Administrador")
        print("3. Salir")
        opcion = input(Fore.YELLOW + "Seleccione una opción: ")

        if opcion == "1":
            menu_cliente()
        elif opcion == "2":
            menu_admin()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print(Fore.RED + "Opción no válida.")


if __name__ == "__main__":
    main()
