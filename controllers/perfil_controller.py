# file: controllers/perfil_controller.py

from tkinter import messagebox
from models.usuario_model import UsuarioModel

class PerfilController:
    def __init__(self, view, main_controller, user_id):
        self.view = view
        self.main_controller = main_controller # Necesario para refrescar el header
        self.user_id = user_id
        self.model = UsuarioModel()

    def load_user_data(self):
        """ Carga los datos del usuario logueado en la vista. """
        user_data = self.model.get_user_by_id(self.user_id)
        if user_data:
            self.view.populate_data(user_data)
        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del perfil.")

    def save_profile(self):
        """ Guarda los datos modificados del perfil. """
        data = self.view.get_data()
        data['codigo'] = self.user_id # Añadimos el ID para la consulta WHERE

        # Validación simple
        if not all(data[key] for key in ['correo', 'apellidos', 'nombres', 'clave']):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos excepto el rol.")
            return

        if messagebox.askyesno("Confirmar", "¿Desea guardar los cambios en su perfil?"):
            if self.model.update_profile(data):
                messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")
                # Notificar al controlador principal para que refresque el header
                self.main_controller.refresh_user_header()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el perfil.")