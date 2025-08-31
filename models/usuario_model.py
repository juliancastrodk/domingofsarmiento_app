# file: models/usuario_model.py

from database.database_manager import DatabaseManager

class UsuarioModel:
    def verify_credentials(self, correo, clave):
        """Verifica si el correo y la clave son correctos."""
        query = "SELECT * FROM Usuarios WHERE Correo = ? AND Clave = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (correo, clave))
                return cursor.fetchone()
        return None

    def get_all_usuarios(self, search_term=""):
        """Obtiene todos los usuarios. La clave se devuelve ofuscada."""
        query = """
            SELECT Codigo, Correo, Apellidos, Nombres, '********' as Clave_Ofuscada, Rol 
            FROM Usuarios
            WHERE Apellidos LIKE ? OR Nombres LIKE ? OR Correo LIKE ?
            ORDER BY Apellidos
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term, like_term))
                return cursor.fetchall()
        return []

    def get_user_by_id(self, user_id):
        """Obtiene todos los datos de un usuario por su ID, incluyendo la clave real."""
        query = "SELECT * FROM Usuarios WHERE Codigo = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
        return None

    def add_usuario(self, user_data):
        """Agrega un nuevo usuario a la base de datos."""
        query = "INSERT INTO Usuarios (Codigo, Correo, Apellidos, Nombres, Clave, Rol) VALUES (?, ?, ?, ?, ?, ?)"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, user_data)
                return True
        return False

    def update_usuario(self, user_data):
        """Actualiza un usuario existente."""
        query = "UPDATE Usuarios SET Correo=?, Apellidos=?, Nombres=?, Clave=?, Rol=? WHERE Codigo=?"
        data_for_update = (
            user_data['correo'], user_data['apellidos'], user_data['nombres'],
            user_data['clave'], user_data['rol'], user_data['codigo']
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False

    def delete_usuario(self, user_id):
        """Elimina un usuario por su ID."""
        query = "DELETE FROM Usuarios WHERE Codigo = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (user_id,))
                return True
        return False

    def get_next_id(self):
        """Obtiene el siguiente ID correlativo para un nuevo usuario."""
        query = "SELECT MAX(Codigo) FROM Usuarios"
        with DatabaseManager() as cursor:
            if cursor:
                result = cursor.execute(query).fetchone()
                return (result[0] or 0) + 1
        return 1
    
    def update_profile(self, user_data):
        """
        Actualiza los datos del perfil de un usuario.
        Importante: Esta consulta NO permite modificar el Rol.
        """
        query = "UPDATE Usuarios SET Correo=?, Apellidos=?, Nombres=?, Clave=? WHERE Codigo=?"
        data_for_update = (
            user_data['correo'], user_data['apellidos'], user_data['nombres'],
            user_data['clave'], user_data['codigo']
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False