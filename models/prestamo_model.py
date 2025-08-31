# file: models/prestamo_model.py

from database.database_manager import DatabaseManager
import sqlite3
from datetime import datetime

class PrestamoModel:
    def get_all_prestamos(self, search_term=""):
        """ Obtiene todos los préstamos con información del socio y los libros. """
        query = """
            SELECT 
                p.Id_prestamo, 
                p.Fecha_retiro, 
                p.Fecha_devolucion,
                (s.nombres || ' ' || s.apellidos) AS socio,
                GROUP_CONCAT(l.Titulo, ', ') AS libros,
                p.Estado
            FROM Prestamos p
            JOIN socios s ON p.Id_socio = s.id_socio
            JOIN Prestamos_Libros pl ON p.Id_prestamo = pl.Id_prestamo
            JOIN Libros l ON pl.Id_libro = l.Id_libro
            GROUP BY p.Id_prestamo, p.Fecha_retiro, p.Fecha_devolucion, s.nombres, s.apellidos, p.Estado
            HAVING socio LIKE ? OR libros LIKE ? OR p.Estado LIKE ?
            ORDER BY p.Id_prestamo DESC
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term, like_term))
                return cursor.fetchall()
        return []

    def add_prestamo(self, fecha_retiro, fecha_devolucion, socio_id, libros_ids, estado="Prestado"):
        try:
            with DatabaseManager() as cursor:
                # VALIDACIÓN 1: Verificar que el socio exista y esté activo
                cursor.execute("""
                    SELECT id_socio, nombres, apellidos, estado FROM socios WHERE id_socio = ?
                """, (socio_id,))
                socio_result = cursor.fetchone()
                
                if not socio_result:
                    print(f"Error: No existe el socio con ID {socio_id}")
                    return {"success": False, "error": f"No existe el socio con ID {socio_id}"}
                
                # Debug: mostrar el estado actual del socio
                print(f"Socio encontrado: ID={socio_result[0]}, Nombre={socio_result[1]} {socio_result[2]}, Estado={socio_result[3]}")
                
                # Verificar estado - tu BD usa "Activo"/"Inactivo"
                estado_socio = socio_result[3]
                estados_validos = [1, '1', 'A', 'Activo', 'activo', 'ACTIVO']
                
                if estado_socio not in estados_validos:
                    print(f"Error: El socio {socio_result[1]} {socio_result[2]} no está activo (estado: {estado_socio})")
                    return {"success": False, "error": f"El socio no está activo. Estado actual: {estado_socio}"}
                
                print(f"✓ Socio activo validado: {socio_result[1]} {socio_result[2]} (estado: {estado_socio})")
                
                # VALIDACIÓN 2: Verificar que el socio no tenga préstamos activos
                # Solo puede hacer préstamo si NO tiene préstamos en estado "Prestado" o "Demorado"
                cursor.execute("""
                    SELECT COUNT(*) FROM prestamos 
                    WHERE id_socio = ? AND estado IN ('Prestado', 'Demorado')
                """, (socio_id,))
                prestamos_activos = cursor.fetchone()[0]
                
                # Debug: mostrar préstamos activos encontrados
                print(f"Préstamos activos/demorados encontrados para socio {socio_id}: {prestamos_activos}")
                
                # Debug adicional: mostrar detalles de los préstamos del socio
                cursor.execute("""
                    SELECT id_prestamo, fecha_retiro, fecha_devolucion, estado 
                    FROM prestamos 
                    WHERE id_socio = ?
                    ORDER BY id_prestamo DESC
                    LIMIT 3
                """, (socio_id,))
                prestamos_socio = cursor.fetchall()
                print(f"Últimos préstamos del socio {socio_id}:")
                for prestamo in prestamos_socio:
                    print(f"  - ID: {prestamo[0]}, Estado: '{prestamo[3]}'")
                
                if prestamos_activos > 0:
                    print(f"Error: El socio tiene {prestamos_activos} préstamo(s) pendiente(s)")
                    return {"success": False, "error": f"El socio tiene {prestamos_activos} préstamo(s) pendiente(s). Debe devolver o regularizar antes de solicitar otro préstamo."}
                
                print(f"✓ Socio sin préstamos pendientes validado")
                
                # VALIDACIÓN 3: Verificar disponibilidad de libros
                for libro_id in libros_ids:
                    cursor.execute("""
                        SELECT titulo, cantidad FROM libros WHERE id_libro = ?
                    """, (libro_id,))
                    libro_result = cursor.fetchone()
                    
                    if not libro_result:
                        return {"success": False, "error": f"No existe el libro con ID {libro_id}"}
                    
                    if libro_result[1] <= 0:
                        return {"success": False, "error": f"El libro '{libro_result[0]}' no tiene stock disponible"}

                # Si todas las validaciones pasan, proceder con el préstamo
                # Insertar préstamo
                cursor.execute("""
                    INSERT INTO Prestamos (Id_socio, Fecha_retiro, Fecha_devolucion, Estado)
                    VALUES (?, ?, ?, ?)
                """, (socio_id, fecha_retiro, fecha_devolucion, estado))

                prestamo_id = cursor.lastrowid

                # Y cuando insertas las relaciones:
                for libro_id in libros_ids:
                    cursor.execute("""
                        INSERT INTO Prestamos_Libros (Id_prestamo, Id_libro)
                        VALUES (?, ?)
                    """, (prestamo_id, libro_id))

                    cursor.execute("""
                        UPDATE Libros
                        SET Cantidad = Cantidad - 1
                        WHERE Id_libro = ? AND Cantidad > 0
                    """, (libro_id,))

                print(f"Préstamo creado exitosamente con ID: {prestamo_id}")
                return {"success": True, "prestamo_id": prestamo_id}

        except Exception as e:
            print("Error en add_prestamo:", e)
            return {"success": False, "error": f"Error interno: {str(e)}"}

    def _validar_socio_activo(self, cursor, socio_id):
        """Método auxiliar para validar que el socio esté activo"""
        cursor.execute("SELECT estado FROM socios WHERE id_socio = ?", (socio_id,))
        result = cursor.fetchone()
        return result and result[0] == "Activo"

    def _tiene_prestamos_activos(self, cursor, socio_id):
        """Método auxiliar para verificar si el socio tiene préstamos activos o demorados"""
        cursor.execute("""
            SELECT COUNT(*) FROM prestamos 
            WHERE id_socio = ? AND estado IN ('Prestado', 'Demorado')
        """, (socio_id,))
        return cursor.fetchone()[0] > 0

    def devolver_prestamo(self, prestamo_id):
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                cursor = conn.cursor()
                
                print(f"Intentando devolver préstamo ID: {prestamo_id}")
                
                # Verificar si el préstamo existe y está en estado 'Prestado'
                cursor.execute("""
                    SELECT Id_prestamo, Estado FROM Prestamos 
                    WHERE Id_prestamo = ?
                """, (prestamo_id,))
                
                prestamo = cursor.fetchone()
                print(f"Préstamo encontrado: {prestamo}")
                
                if not prestamo:
                    print("Préstamo no encontrado")
                    return False
                
                if prestamo[1] != 'Prestado':
                    print(f"Préstamo no está prestado, estado actual: {prestamo[1]}")
                    return False
                
                # Obtener TODOS los Id_libro del préstamo (cambié fetchone() por fetchall())
                cursor.execute("""
                    SELECT Id_libro 
                    FROM Prestamos_Libros 
                    WHERE Id_prestamo = ?
                """, (prestamo_id,))
                
                libros_result = cursor.fetchall()  # fetchall() en lugar de fetchone()
                print(f"Libros encontrados: {libros_result}")
                
                if not libros_result:
                    print("No se encontraron libros asociados al préstamo")
                    return False
                
                # Actualizar el estado del préstamo a 'Devuelto'
                cursor.execute("""
                    UPDATE Prestamos 
                    SET Estado = ?, Fecha_devolucion = ? 
                    WHERE Id_prestamo = ?
                """, ('Devuelto', datetime.now().strftime('%Y-%m-%d'), prestamo_id))
                
                print(f"Préstamo actualizado, filas afectadas: {cursor.rowcount}")
                
                # Incrementar la cantidad de TODOS los libros asociados al préstamo
                for libro_tupla in libros_result:
                    id_libro = libro_tupla[0]
                    print(f"Actualizando libro ID: {id_libro}")
                    
                    cursor.execute("""
                        UPDATE Libros 
                        SET Cantidad = Cantidad + 1 
                        WHERE Id_libro = ?
                    """, (id_libro,))
                    
                    print(f"Libro {id_libro} actualizado, filas afectadas: {cursor.rowcount}")
                
                conn.commit()
                print("Transacción confirmada exitosamente")
                return True
                
        except sqlite3.Error as e:
            print(f"Error SQL específico: {e}")
            return False
        except Exception as e:
            print(f"Error general: {e}")
            return False
        
    def update_prestamo_libros(self, prestamo_id, nuevos_libros):
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                cursor = conn.cursor()
                
                # Obtener los libros actuales del préstamo
                cursor.execute("""
                    SELECT Id_libro FROM Prestamos_Libros 
                    WHERE Id_prestamo = ?
                """, (prestamo_id,))
                
                libros_actuales = [row[0] for row in cursor.fetchall()]
                print(f"Libros actuales del préstamo {prestamo_id}: {libros_actuales}")
                print(f"Nuevos libros seleccionados: {nuevos_libros}")
                
                # Libros que se van a quitar (devolver al inventario)
                libros_a_quitar = set(libros_actuales) - set(nuevos_libros)
                # Libros que se van a agregar (quitar del inventario)
                libros_a_agregar = set(nuevos_libros) - set(libros_actuales)
                
                print(f"Libros a quitar: {libros_a_quitar}")
                print(f"Libros a agregar: {libros_a_agregar}")
                
                # Devolver al inventario los libros que se quitan
                for libro_id in libros_a_quitar:
                    cursor.execute("""
                        UPDATE Libros 
                        SET Cantidad = Cantidad + 1 
                        WHERE Id_libro = ?
                    """, (libro_id,))
                    print(f"Devuelto al inventario libro ID: {libro_id}")
                
                # Quitar del inventario los libros que se agregan
                for libro_id in libros_a_agregar:
                    cursor.execute("""
                        UPDATE Libros 
                        SET Cantidad = Cantidad - 1 
                        WHERE Id_libro = ?
                    """, (libro_id,))
                    print(f"Quitado del inventario libro ID: {libro_id}")
                
                # Eliminar las relaciones actuales
                cursor.execute("""
                    DELETE FROM Prestamos_Libros 
                    WHERE Id_prestamo = ?
                """, (prestamo_id,))
                
                # Insertar las nuevas relaciones
                for libro_id in nuevos_libros:
                    cursor.execute("""
                        INSERT INTO Prestamos_Libros (Id_prestamo, Id_libro) 
                        VALUES (?, ?)
                    """, (prestamo_id, libro_id))
                
                conn.commit()
                print(f"Préstamo {prestamo_id} actualizado exitosamente")
                return True
                
        except sqlite3.Error as e:
            print(f"Error SQL al actualizar préstamo: {e}")
            return False
        except Exception as e:
            print(f"Error general al actualizar préstamo: {e}")
            return False
        
    def get_prestamo_by_id(self, prestamo_id):
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                cursor = conn.cursor()
                
                # Obtener datos del préstamo
                cursor.execute("""
                    SELECT p.Id_prestamo, p.Id_socio, p.Fecha_retiro, p.Fecha_devolucion, p.Estado
                    FROM Prestamos p
                    WHERE p.Id_prestamo = ?
                """, (prestamo_id,))
                
                prestamo = cursor.fetchone()
                if not prestamo:
                    return None
                
                # Obtener los libros asociados al préstamo
                cursor.execute("""
                    SELECT pl.Id_libro 
                    FROM Prestamos_Libros pl
                    WHERE pl.Id_prestamo = ?
                """, (prestamo_id,))
                
                libros = [row[0] for row in cursor.fetchall()]
                
                # Retornar datos del préstamo junto con los libros
                return {
                    'id': prestamo[0],
                    'id_socio': prestamo[1],
                    'fecha_retiro': prestamo[2],
                    'fecha_devolucion': prestamo[3],
                    'estado': prestamo[4],
                    'libros': libros
                }
                
        except sqlite3.Error as e:
            print(f"Error al obtener préstamo: {e}")
            return None