# file: models/reportes_model.py

from database.database_manager import DatabaseManager
from datetime import date

class ReportesModel:
    def get_resumen_inventario(self):
        """
        Obtiene datos clave del inventario y la comunidad.
        Devuelve: Un diccionario con los totales.
        """
        resumen = {}
        with DatabaseManager() as cursor:
            if not cursor:
                return {}
            
            # Total de títulos de libros distintos y copias totales
            cursor.execute("SELECT COUNT(Id_libro), SUM(cantidad) FROM Libros")
            res_libros = cursor.fetchone()
            resumen['total_titulos'] = res_libros[0] or 0
            resumen['total_copias'] = res_libros[1] or 0

            # Total de socios activos
            cursor.execute("SELECT COUNT(Id_socio) FROM Socios WHERE estado = 'Activo'")
            resumen['socios_activos'] = cursor.fetchone()[0] or 0

            # Total de préstamos activos (no devueltos)
            cursor.execute("SELECT COUNT(id_prestamo) FROM prestamos WHERE estado = 'Prestado'")
            resumen['prestamos_activos'] = cursor.fetchone()[0] or 0
            
            return resumen

    def get_libros_mas_solicitados(self, limit=10):
        """
        Obtiene un ranking de los libros más prestados.
        Devuelve: Una lista de tuplas (Título, Autor, Cantidad de Préstamos).
        """
        query = """
            SELECT l.titulo, l.autor, COUNT(pl.id_libro) AS prestamos_count
            FROM prestamos_libros pl
            JOIN Libros l ON pl.id_libro = l.Id_libro
            GROUP BY pl.id_libro
            ORDER BY prestamos_count DESC
            LIMIT ?
        """
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        return []

    def get_prestamos_vencidos(self):
        """
        Obtiene todos los préstamos activos cuya fecha de devolución ya pasó.
        Devuelve: Una lista de tuplas (ID Préstamo, Nombre Socio, Título Libro, Fecha Devolución).
        """
        hoy = date.today().strftime("%Y-%m-%d")
        query = """
            SELECT p.id_prestamo,
                   (s.nombres || ' ' || s.apellidos) AS socio,
                   GROUP_CONCAT(l.titulo, ', ') AS libros,
                   p.fecha_devolucion
            FROM prestamos p
            JOIN socios s ON p.id_socio = s.id_socio
            JOIN prestamos_libros pl ON p.id_prestamo = pl.id_prestamo
            JOIN libros l ON pl.id_libro = l.id_libro
            WHERE p.estado = 'Prestado' AND p.fecha_devolucion < ?
            GROUP BY p.id_prestamo
            ORDER BY p.fecha_devolucion ASC
        """
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (hoy,))
                return cursor.fetchall()
        return []