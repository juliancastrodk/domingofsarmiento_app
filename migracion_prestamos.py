import sqlite3

def migrar_prestamos():
    try:
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()

        # Script de migración
        sql_script = """
        -- 1. Crear tabla nueva de Prestamos sin Id_libro
        CREATE TABLE IF NOT EXISTS Prestamos_new (
            Id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_socio INTEGER NOT NULL,
            Fecha_retiro TEXT NOT NULL,
            Fecha_devolucion TEXT NOT NULL,
            Estado INTEGER DEFAULT 1,
            FOREIGN KEY(Id_socio) REFERENCES Socios(Id_socio)
        );

        -- 2. Copiar los datos desde la tabla vieja (sin Id_libro)
        INSERT INTO Prestamos_new (Id_prestamo, Id_socio, Fecha_retiro, Fecha_devolucion, Estado)
        SELECT Id_prestamo, Id_socio, Fecha_retiro, Fecha_devolucion, Estado
        FROM Prestamos;

        -- 3. Eliminar tabla Prestamos vieja
        DROP TABLE Prestamos;

        -- 4. Renombrar la tabla nueva a Prestamos
        ALTER TABLE Prestamos_new RENAME TO Prestamos;

        -- 5. Crear tabla intermedia Prestamos_Libros (muchos a muchos)
        CREATE TABLE IF NOT EXISTS Prestamos_Libros (
            Id_prestamo_libro INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_prestamo INTEGER NOT NULL,
            Id_libro INTEGER NOT NULL,
            FOREIGN KEY (Id_prestamo) REFERENCES Prestamos(Id_prestamo),
            FOREIGN KEY (Id_libro) REFERENCES Libros(Id_libro)
        );
        """

        cursor.executescript(sql_script)
        conexion.commit()
        conexion.close()

        print("✅ Migración completada con éxito")

    except Exception as e:
        print(f"❌ Error en la migración: {e}")

# Ejecutar
if __name__ == "__main__":
    migrar_prestamos()
