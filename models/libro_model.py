# file: models/libro_model.py

import sqlite3
from database.database_manager import DatabaseManager

class LibroModel:
    def get_all_libros(self, search_term=""):
        """ Obtiene todos los libros o los filtra por título o autor. """
        query = """
            SELECT Id_libro, titulo, autor, isbn, editorial, año, cantidad, categoria 
            FROM Libros 
            WHERE titulo LIKE ? OR autor LIKE ?
            ORDER BY titulo
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term))
                return cursor.fetchall()
        return []

    def add_libro(self, libro_data):
        """ Agrega un nuevo libro a la base de datos. """
        query = "INSERT INTO Libros (Id_libro, titulo, autor, isbn, editorial, año, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, libro_data)
                return True
        return False
    
    def get_libro_by_id(self, libro_id):
        """Obtiene un libro por su ID"""
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT Id_libro, Titulo, Autor, ISBN, Editorial, Año, Cantidad, Categoria
                    FROM Libros 
                    WHERE Id_libro = ?
                """, (libro_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener libro por ID: {e}")
            return None
    
    def get_libro_by_isbn(self, libro_id):
        """ Obtiene un libro por su ID. """
        query = "SELECT Id_libro, titulo, autor, isbn, editorial, año, cantidad, categoria FROM Libros WHERE Id_libro = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (libro_id,))
                return cursor.fetchone()
        return None

    def update_libro(self, libro_data):
        """ Actualiza un libro existente. """
        query = """
            UPDATE Libros 
            SET titulo=?, autor=?, isbn=?, editorial=?, año=?, cantidad=?, categoria=? 
            WHERE Id_libro=?
        """
        # libro_data is a tuple: (id, titulo, autor, isbn, editorial, año, cantidad, categoria)
        data_for_update = (
            libro_data[1], libro_data[2], libro_data[3],  # titulo, autor, isbn
            libro_data[4], libro_data[5], libro_data[6],  # editorial, año, cantidad
            libro_data[7], libro_data[0]                  # categoria, id (WHERE clause)
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False

    def delete_libro(self, libro_id):
        """ Elimina un libro por su ID. """
        query = "DELETE FROM Libros WHERE Id_libro = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (libro_id,))
                return True
        return False

    def get_next_id(self):
        """ Obtiene el siguiente ID correlativo para un nuevo libro. """
        query = "SELECT MAX(Id_libro) FROM Libros"
        with DatabaseManager() as cursor:
            if cursor:
                result = cursor.execute(query).fetchone()
                return (result[0] or 0) + 1
        return 1