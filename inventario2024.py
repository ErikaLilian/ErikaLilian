import sqlite3
import os

# Nombre de la base de datos
DATABASE = 'inventario.db'

def conectar_db():
    """Conecta a la base de datos SQLite."""
    try:
      conn = sqlite3.connect(DATABASE)
      return conn
    except sqlite3.Error as e:
      print(f"Error al conectar a la base de datos: {e}")
      return None

def crear_tabla():
    """Crea la tabla 'productos' si no existe."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      cursor = conn.cursor()
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS productos (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              descripcion TEXT,
              cantidad INTEGER NOT NULL,
              precio REAL NOT NULL,
              categoria TEXT
          )
      ''')
      conn.commit()
    except sqlite3.Error as e:
      print(f"Error al crear la tabla: {e}")
    finally:
      conn.close()

def registrar_producto():
    """Registra un nuevo producto en el inventario."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      nombre = input("Nombre del producto: ")
      descripcion = input("Descripción: ")
      cantidad = int(input("Cantidad: "))
      precio = float(input("Precio: "))
      categoria = input("Categoría: ")

      cursor = conn.cursor()
      cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                     (nombre, descripcion, cantidad, precio, categoria))
      conn.commit()
      print("Producto registrado con éxito.")
    except ValueError:
      print("Error: Ingrese valores numéricos válidos para cantidad y precio.")
    except sqlite3.Error as e:
      print(f"Error al registrar el producto: {e}")
    finally:
      conn.close()

def mostrar_productos():
    """Muestra todos los productos en el inventario."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM productos")
      productos = cursor.fetchall()

      if not productos:
          print("No hay productos registrados.")
          return

      print("-" * 50)
      print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<15}".format("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
      print("-" * 50)
      for producto in productos:
          print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<15}".format(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5]))
      print("-" * 50)
    except sqlite3.Error as e:
      print(f"Error al mostrar los productos: {e}")
    finally:
      conn.close()

def actualizar_cantidad():
    """Actualiza la cantidad de un producto."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      id_producto = int(input("ID del producto a actualizar: "))
      nueva_cantidad = int(input("Nueva cantidad: "))

      cursor = conn.cursor()
      cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
      conn.commit()

      if cursor.rowcount == 0: #verifica si se actualizo algun registro
          print(f"No existe un producto con el ID {id_producto}")
      else:
          print("Cantidad actualizada con éxito.")
    except ValueError:
      print("Error: Ingrese valores numéricos válidos para ID y cantidad.")
    except sqlite3.Error as e:
      print(f"Error al actualizar la cantidad: {e}")
    finally:
      conn.close()

def eliminar_producto():
    """Elimina un producto del inventario."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      id_producto = int(input("ID del producto a eliminar: "))

      cursor = conn.cursor()
      cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
      conn.commit()
      if cursor.rowcount == 0: #verifica si se borro algun registro
          print(f"No existe un producto con el ID {id_producto}")
      else:
          print("Producto eliminado con éxito.")

    except ValueError:
      print("Error: Ingrese un valor numérico válido para el ID.")
    except sqlite3.Error as e:
      print(f"Error al eliminar el producto: {e}")
    finally:
      conn.close()

def buscar_producto():
    """Busca un producto por ID."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      id_producto = int(input("ID del producto a buscar: "))

      cursor = conn.cursor()
      cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
      producto = cursor.fetchone()

      if producto:
          print("-" * 50)
          print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<15}".format("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
          print("-" * 50)
          print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<15}".format(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5]))
          print("-" * 50)
      else:
          print(f"No se encontró ningún producto con el ID {id_producto}.")
    except ValueError:
      print("Error: Ingrese un valor numérico válido para el ID.")
    except sqlite3.Error as e:
      print(f"Error al buscar el producto: {e}")
    finally:
      conn.close()

def reporte_bajo_stock():
    """Genera un reporte de productos con bajo stock."""
    conn = conectar_db()
    if conn is None:
      return
    try:
      limite = int(input("Ingrese el límite de stock: "))

      cursor = conn.cursor()
      cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
      productos_bajo_stock = cursor.fetchall()

      if productos_bajo_stock:
          print("Productos con bajo stock:")
          print("-" * 50)
          print("{:<5} {:<20} {:<10}".format("ID", "Nombre", "Cantidad"))
          print("-" * 50)
          for producto in productos_bajo_stock:
              print("{:<5} {:<20} {:<10}".format(producto[0], producto[1], producto[3]))
          print("-" * 50)
      else:
          print("No hay productos con bajo stock.")
    except ValueError:
      print("Error: Ingrese un valor numérico válido para el límite.")
    except sqlite3.Error as e:
      print(f"Error al generar el reporte: {e}")
    finally:
      conn.close()

def menu():
    """Muestra el menú principal y gestiona las opciones."""
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Actualizar cantidad")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte de bajo stock")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            mostrar_productos()
        elif opcion == '3':
            actualizar_cantidad()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            buscar_producto()
        elif opcion == '6':
            reporte_bajo_stock()
        elif opcion == '7':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    crear_tabla()  # Crea la tabla al iniciar el programa
