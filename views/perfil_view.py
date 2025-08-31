# file: views/perfil_view.py

from tkinter import *
import ttkbootstrap as tb

class PerfilView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        main_frame = tb.Frame(self)
        main_frame.pack(expand=True)

        lbl_frame = tb.LabelFrame(main_frame, text="Mis Datos", padding=(20, 15))
        lbl_frame.pack()
        
        # Diccionario para guardar los widgets de entrada
        self.entries = {}
        fields = ["Correo", "Apellidos", "Nombres", "Clave", "Rol"]

        for i, field in enumerate(fields):
            label = tb.Label(lbl_frame, text=f"{field}:", font=("Calibri", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            entry = tb.Entry(lbl_frame, width=40, font=("Calibri", 12))
            entry.grid(row=i, column=1, padx=10, pady=10)
            
            if field == "Clave":
                entry.config(show="*")
            
            # La clave del diccionario será en minúsculas y sin espacios
            self.entries[field.lower()] = entry
        
        # Hacemos que el campo 'Rol' no sea editable
        self.entries['rol'].config(state="readonly")

        # Botón para guardar los cambios
        save_button = tb.Button(
            lbl_frame, 
            text="Guardar Cambios", 
            bootstyle="success", 
            command=self.controller.save_profile
        )
        save_button.grid(row=len(fields), column=1, padx=10, pady=20, sticky="e")

    def populate_data(self, user_data):
        """ Rellena los campos del formulario con los datos del usuario. """
        # user_data es una tupla: (Codigo, Correo, Apellidos, Nombres, Clave, Rol)
        self.entries['correo'].insert(0, user_data[1])
        self.entries['apellidos'].insert(0, user_data[2])
        self.entries['nombres'].insert(0, user_data[3])
        self.entries['clave'].insert(0, user_data[4])
        self.entries['rol'].insert(0, user_data[5])

    def get_data(self):
        """ Recoge los datos de los campos del formulario y los devuelve en un diccionario. """
        return {key: entry.get() for key, entry in self.entries.items()}