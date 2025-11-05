# productos_manager.py
from conexion import crear_conexion
from colorama import Fore

class ProductoManager:
    def __init__(self):
        self.conexion = crear_conexion()

    def mostrar_productos(self):
        """Muestra todos los productos disponibles con su categoría y precio."""
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id, s.nombre, s.precio, c.nombre AS categoria, s.medida
            FROM Sticker s
            JOIN CategoriaSticker c ON s.categoria_id = c.id
            ORDER BY c.nombre, s.nombre;
        """)
        productos = cursor.fetchall()
        if not productos:
            print(Fore.RED + "No hay productos registrados.")
            return
        print(Fore.CYAN + "\n--- LISTA DE PRODUCTOS ---")
        for p in productos:
            print(f"{Fore.WHITE}ID: {p['id']} | {p['nombre']} | "
                  f"Categoría: {p['categoria']} | Precio: Q{p['precio']} | Medida: {p['medida']}")
        cursor.close()

    def buscar_producto(self, termino):
        """Busca productos por nombre."""
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nombre, precio, medida FROM Sticker
            WHERE nombre LIKE %s
        """, (f"%{termino}%",))
        resultados = cursor.fetchall()
        if resultados:
            print(Fore.GREEN + f"\nResultados para '{termino}':")
            for r in resultados:
                print(f"ID {r['id']} | {r['nombre']} | Q{r['precio']} | {r['medida']}")
        else:
            print(Fore.RED + "No se encontraron productos con ese nombre.")
        cursor.close()

    def obtener_productos_para_pedido(self):
        """Permite seleccionar productos para cotización o pedido."""
        productos = []
        while True:
            id_prod = input(Fore.WHITE + "Ingrese ID del producto (0 para finalizar): ")
            if id_prod == "0":
                break
            try:
                id_prod = int(id_prod)
                cursor = self.conexion.cursor(dictionary=True)
                cursor.execute("SELECT id, nombre, precio FROM Sticker WHERE id = %s", (id_prod,))
                producto = cursor.fetchone()
                cursor.close()
                if producto:
                    cantidad = int(input("Cantidad: "))
                    productos.append({
                        "id": producto["id"],
                        "nombre": producto["nombre"],
                        "precio": producto["precio"],
                        "cantidad": cantidad
                    })
                else:
                    print(Fore.RED + "Producto no encontrado.")
            except ValueError:
                print(Fore.RED + "Ingrese un número válido.")
        return productos

    def agregar_producto(self, nombre, precio):
        """Agrega un producto nuevo (simple, sin categoría)."""
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO Sticker (nombre, precio) VALUES (%s, %s)", (nombre, precio))
        self.conexion.commit()
        cursor.close()
        print(Fore.GREEN + "Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """Elimina un producto existente."""
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM Sticker WHERE id = %s", (id_producto,))
        self.conexion.commit()
        if cursor.rowcount > 0:
            print(Fore.GREEN + "Producto eliminado con éxito.")
        else:
            print(Fore.RED + "No se encontró el producto con ese ID.")
        cursor.close()

