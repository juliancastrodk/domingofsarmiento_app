# file: models/socio_model.py

from database.database_manager import DatabaseManager

class SocioModel:
    def get_all_socios(self, search_term=""):
        """ Obtiene todos los socios o los filtra por un término de búsqueda. """
        query = """
            SELECT Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos 
            FROM Socios 
            WHERE apellidos LIKE ? OR nombres LIKE ?
            ORDER BY apellidos
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term))
                return cursor.fetchall()
        return []

    def add_socio(self, socio_data):
        """ Agrega un nuevo socio a la base de datos. """
        query = "INSERT INTO Socios (Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, socio_data)
                return True
        return False

    def get_socio_by_id(self, socio_id):
        """ Obtiene un socio por su ID. """
        query = "SELECT Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos FROM Socios WHERE Id_socio = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (socio_id,))
                return cursor.fetchone()
        return None
    
    def get_socio_by_dni(self, dni):
            """Devuelve un socio por su DNI o None si no existe."""
            query = """
                SELECT Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos
                FROM Socios 
                WHERE dni = ?
            """
            with DatabaseManager() as cursor:
                if cursor:
                    cursor.execute(query, (dni,))
                    return cursor.fetchone()
            return None

    def update_socio(self, socio_data):
        """ Actualiza un socio existente. """
        query = """
            UPDATE Socios 
            SET dni=?, apellidos=?, nombres=?, telefono=?, direccion=?, estado=?, prestamos_activos=? 
            WHERE Id_socio=?
        """
        # socio_data is a tuple: (id, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos)
        data_for_update = (
            socio_data[1], socio_data[2], socio_data[3],  # dni, apellidos, nombres
            socio_data[4], socio_data[5], socio_data[6],  # telefono, direccion, estado
            socio_data[7], socio_data[0]                  # prestamos_activos, id (WHERE clause)
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False

    def delete_socio(self, socio_id):
        """ Elimina un socio por su ID. """
        query = "DELETE FROM Socios WHERE Id_socio = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (socio_id,))
                return True
        return False

    def get_next_id(self):
        """ Obtiene el siguiente ID correlativo para un nuevo socio. """
        query = "SELECT MAX(Id_socio) FROM Socios"
        with DatabaseManager() as cursor:
            if cursor:
                result = cursor.execute(query).fetchone()
                return (result[0] or 0) + 1
        return 1