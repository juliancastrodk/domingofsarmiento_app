# file: controllers/usuario_controller.py

from tkinter import Toplevel, messagebox
import ttkbootstrap as tb
from models.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self, view):
        self.view = view
        self.model = UsuarioModel()

    def load_initial_data(self):
        usuarios = self.model.get_all_usuarios()
        self.view.update_treeview(usuarios)
        
    def search_usuarios(self, event=None):
        search_term = self.view.get_search_term()
        usuarios = self.model.get_all_usuarios(search_term)
        self.view.update_treeview(usuarios)
        
    def delete_usuario(self):
        user_id = self.view.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un usuario para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el usuario con ID {user_id}?"):
            if self.model.delete_usuario(user_id):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                self.search_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def show_add_usuario_dialog(self):
        dialog = self._create_user_dialog("Nuevo Usuario")
        
        # El comando del botón Guardar llamará al método para guardar un nuevo usuario
        dialog.save_button.config(command=lambda: self._save_new_user(dialog))

    def show_edit_usuario_dialog(self):
        user_id = self.view.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un usuario para modificar.")
            return
        
        user_data = self.model.get_user_by_id(user_id) # (Codigo, Correo, Apellidos, Nombres, Clave, Rol)
        if not user_data:
            messagebox.showerror("Error", "No se pudo encontrar los datos del usuario.")
            return

        dialog = self._create_user_dialog("Modificar Usuario", data=user_data)
        
        # El comando del botón Guardar llamará al método para actualizar
        dialog.save_button.config(command=lambda: self._save_updated_user(dialog, user_id))
        
    def _center_window(self, window, width, height):
        """Centra una ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_user_dialog(self, title, data=None):
        dialog = Toplevel(self.view)
        dialog.title(title)
        dialog.transient(self.view)
        dialog.grab_set()
        
        # Centrar la ventana
        self._center_window(dialog, 480, 340)

        lbl_frame = tb.LabelFrame(dialog, text=title, padding=(15, 10))
        lbl_frame.pack(padx=15, pady=15, fill="both", expand=True)

        fields = ["Correo", "Apellidos", "Nombres", "Clave"]
        dialog.entries = {}

        for i, field in enumerate(fields):
            label = tb.Label(lbl_frame, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            entry = tb.Entry(lbl_frame, width=40)
            if field == "Clave":
                entry.config(show="*")
            entry.grid(row=i, column=1, padx=5, pady=5)
            dialog.entries[field.lower()] = entry
        
        # Combobox para el Rol
        label_rol = tb.Label(lbl_frame, text="Rol:")
        label_rol.grid(row=len(fields), column=0, padx=5, pady=5, sticky="w")
        dialog.entries['rol'] = tb.Combobox(lbl_frame, values=['Administrador', 'Bibliotecario'], state="readonly", width=38)
        dialog.entries['rol'].grid(row=len(fields), column=1, padx=5, pady=5)
        
        # Si es para editar, rellenamos los campos
        if data:
            dialog.entries['correo'].insert(0, data[1])
            dialog.entries['apellidos'].insert(0, data[2])
            dialog.entries['nombres'].insert(0, data[3])
            dialog.entries['clave'].insert(0, data[4])
            dialog.entries['rol'].set(data[5])
        else: # Si es nuevo, ponemos un rol por defecto
            dialog.entries['rol'].current(0)
            
        # Botones
        button_frame = tb.Frame(lbl_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
        
        dialog.save_button = tb.Button(button_frame, text="Guardar", bootstyle="success")
        dialog.save_button.pack(side="left", padx=5)
        cancel_button = tb.Button(button_frame, text="Cancelar", bootstyle="secondary", command=dialog.destroy)
        cancel_button.pack(side="left", padx=5)

        return dialog

    def _save_new_user(self, dialog):
        data = {key: entry.get() for key, entry in dialog.entries.items()}
        
        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        next_id = self.model.get_next_id()
        user_tuple = (next_id, data['correo'], data['apellidos'], data['nombres'], data['clave'], data['rol'])

        if self.model.add_usuario(user_tuple):
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo agregar el usuario.", parent=dialog)

    def _save_updated_user(self, dialog, user_id):
        data = {key: entry.get() for key, entry in dialog.entries.items()}
        data['codigo'] = user_id

        if not all(value for key, value in data.items() if key != 'codigo'):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        if self.model.update_usuario(data):
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.", parent=dialog)