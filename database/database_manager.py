# file: database/database_manager.py

import sqlite3
from tkinter import messagebox

class DatabaseManager:
    def __init__(self, db_name="biblioteca.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()