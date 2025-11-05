from conexion import crear_conexion

class ProductoManager:
    def __init__(self):
        self.conexion = crear_conexion()

    def mostrar_productos(self):
        """Muestra todos los productos con su categoría y precio."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    s.id, 
                    s.nombre, 
                    s.precio, 
                    c.nombre AS categoria, 
                    s.medida, 
                    s.especificaciones
                FROM Sticker s
                JOIN CategoriaSticker c ON s.categoria_id = c.id
                ORDER BY c.nombre, s.nombre;
            """)
            productos = cursor.fetchall()
            print("\n--- LISTA DE PRODUCTOS DISPONIBLES ---")
            for p in productos:
                print(f"[{p['id']}] {p['nombre']} | Categoría: {p['categoria']} | "
                      f"Medida: {p['medida']} | Precio: Q{p['precio']:.2f}")
                print(f"  → {p['especificaciones']}\n")
            cursor.close()
        except Exception as e:
            print("Error al mostrar los productos:", e)

    def buscar_producto(self, nombre):
        """Busca un producto por nombre."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            consulta = """
                SELECT 
                    s.id, 
                    s.nombre, 
                    s.precio, 
                    c.nombre AS categoria, 
                    s.medida, 
                    s.especificaciones
                FROM Sticker s
                JOIN CategoriaSticker c ON s.categoria_id = c.id
                WHERE s.nombre LIKE %s;
            """
            cursor.execute(consulta, (f"%{nombre}%",))
            resultados = cursor.fetchall()
            if resultados:
                print(f"\nResultados de búsqueda para '{nombre}':")
                for p in resultados:
                    print(f"[{p['id']}] {p['nombre']} | Categoría: {p['categoria']} | "
                          f"Medida: {p['medida']} | Precio: Q{p['precio']:.2f}")
                    print(f"  → {p['especificaciones']}\n")
            else:
                print(f"No se encontraron productos que coincidan con '{nombre}'.")
            cursor.close()
        except Exception as e:
            print("Error al buscar el producto:", e)

    def cotizar_pedido(self, productos_seleccionados, envio=20.0):
        """Calcula el total de una cotización, incluyendo envío."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            total = 0
            print("\n--- COTIZACIÓN ---")
            for prod_id, cantidad in productos_seleccionados.items():
                cursor.execute("SELECT nombre, precio FROM Sticker WHERE id = %s", (prod_id,))
                producto = cursor.fetchone()
                if producto:
                    subtotal = producto['precio'] * cantidad
                    total += subtotal
                    print(f"{producto['nombre']} x{cantidad} → Q{subtotal:.2f}")
                else:
                    print(f"ID {prod_id} no encontrado.")
            print(f"\nCosto de envío: Q{envio:.2f}")
            total_final = total + envio
            print(f"TOTAL FINAL: Q{total_final:.2f}\n")
            cursor.close()
        except Exception as e:
            print("Error al generar la cotización:", e)
