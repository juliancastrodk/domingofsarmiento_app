# file: controllers/socio_controller.py

from tkinter import Toplevel, messagebox
import ttkbootstrap as tb
from models.socio_model import SocioModel

class SocioController:
    def __init__(self, view):
        self.view = view
        self.model = SocioModel()

    def load_initial_data(self):
        """ Carga los datos iniciales en la vista. """
        socios = self.model.get_all_socios()
        self.view.update_treeview(socios)
        
    def search_socios(self, event=None):
        """ Busca socios según el término de búsqueda de la vista. """
        search_term = self.view.get_search_term()
        socios = self.model.get_all_socios(search_term)
        self.view.update_treeview(socios)
        
    def refresh_socios(self):
        socios = self.model.get_all_socios()
        self.view.update_treeview(socios)
        
    def delete_socio(self):
        socio_id = self.view.get_selected_socio_id()
        if not socio_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un socio para eliminar.")
            return

        socio_data = self.model.get_socio_by_id(socio_id)
        if socio_data and int(socio_data[7]) > 0:  # prestamos_activos
            messagebox.showwarning("Atención", "No se puede eliminar un socio con préstamos activos.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al socio con ID {socio_id}?"):
            if self.model.delete_socio(socio_id):
                messagebox.showinfo("Éxito", "Socio eliminado correctamente.")
                self.search_socios()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el socio.")
                
    def show_add_socio_dialog(self):
        dialog = self._create_socio_dialog("Nuevo Socio")
        dialog.save_button.config(command=lambda: self._save_new_socio(dialog))

    def _center_window(self, window, width, height):
        """Centra una ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def _create_socio_dialog(self, title, data=None):
        dialog = Toplevel(self.view)
        dialog.title(title)
        dialog.transient(self.view)
        dialog.grab_set()
        
        # Centrar la ventana
        self._center_window(dialog, 480, 430)
        
        lbl_frame = tb.LabelFrame(dialog, text=title, padding=(15, 10))
        lbl_frame.pack(padx=15, pady=15, fill="both", expand=True)

        dialog.entries = {}

        # Campos de texto
        campos = [
            ("dni", "D.N.I"),
            ("apellidos", "Apellidos"),
            ("nombres", "Nombres"),
            ("telefono", "Teléfono"),
            ("direccion", "Dirección"),
        ]

        for i, (key, label_text) in enumerate(campos):
            label = tb.Label(lbl_frame, text=label_text + ":")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tb.Entry(lbl_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)

            dialog.entries[key] = entry

        # Combobox Estado
        label_estado = tb.Label(lbl_frame, text="Estado:")
        label_estado.grid(row=len(campos), column=0, padx=5, pady=5, sticky="w")
        dialog.entries['estado'] = tb.Combobox(lbl_frame, values=['Activo', 'Inactivo'], state="readonly", width=38)
        dialog.entries['estado'].grid(row=len(campos), column=1, padx=5, pady=5)

        # Combobox Préstamos
        label_prestamos = tb.Label(lbl_frame, text="Préstamos:")
        label_prestamos.grid(row=len(campos)+1, column=0, padx=5, pady=5, sticky="w")
        dialog.entries['prestamos_activos'] = tb.Combobox(lbl_frame, values=['0', '1'], state="readonly", width=38)
        dialog.entries['prestamos_activos'].grid(row=len(campos)+1, column=1, padx=5, pady=5)

        # Si es para editar, rellenamos los campos
        if data:
            dialog.entries['dni'].insert(0, data[1])
            dialog.entries['apellidos'].insert(0, data[2])
            dialog.entries['nombres'].insert(0, data[3])
            dialog.entries['telefono'].insert(0, data[4])
            dialog.entries['direccion'].insert(0, data[5])
            dialog.entries['estado'].set(data[6])
            dialog.entries['prestamos_activos'].set(data[7])
        else:
            dialog.entries['estado'].current(0)
            dialog.entries['prestamos_activos'].current(0)

        # Botones
        button_frame = tb.Frame(lbl_frame)
        button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=10)
        
        dialog.save_button = tb.Button(button_frame, text="Guardar", bootstyle="success")
        dialog.save_button.pack(side="left", padx=5)
        cancel_button = tb.Button(button_frame, text="Cancelar", bootstyle="secondary", command=dialog.destroy)
        cancel_button.pack(side="left", padx=5)

        return dialog
    
    def _save_new_socio(self, dialog):
        data = {key: entry.get() for key, entry in dialog.entries.items()}

        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        # Validación: DNI ya registrado
        if self.model.get_socio_by_dni(data['dni']):
            messagebox.showerror("Error", "El DNI ingresado ya está registrado.", parent=dialog)
            return

        next_id = self.model.get_next_id()
        socio_tuple = (
            next_id,
            data['dni'],
            data['apellidos'],
            data['nombres'],
            data['telefono'],
            data['direccion'],
            data['estado'],
            data['prestamos_activos']
        )

        if self.model.add_socio(socio_tuple):
            messagebox.showinfo("Éxito", "Socio agregado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo agregar el socio.", parent=dialog)
        
    def show_edit_socio_dialog(self):
        socio_id = self.view.get_selected_socio_id()
        if not socio_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un socio para modificar.")
            return

        socio_data = self.model.get_socio_by_id(socio_id)
        if not socio_data:
            messagebox.showerror("Error", f"No se encontraron datos para el socio con ID {socio_id}.")
            return

        dialog = self._create_socio_dialog("Editar Socio", socio_data)
        dialog.save_button.config(command=lambda: self._save_updated_socio(dialog, socio_id))
        
    def _save_updated_socio(self, dialog, socio_id):
        data = {key: entry.get() for key, entry in dialog.entries.items()}

        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        socio_tuple = (
            socio_id,
            data['dni'],
            data['apellidos'],
            data['nombres'],
            data['telefono'],
            data['direccion'],
            data['estado'],
            data['prestamos_activos']
        )

        if self.model.update_socio(socio_tuple):
            messagebox.showinfo("Éxito", "Socio actualizado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el socio.", parent=dialog)
