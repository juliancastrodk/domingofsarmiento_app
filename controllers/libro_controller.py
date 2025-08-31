# file: controllers/libro_controller.py

from tkinter import Toplevel, messagebox
import ttkbootstrap as tb
from models.libro_model import LibroModel

class LibroController:
    def __init__(self, view):
        self.view = view
        self.model = LibroModel()

    def load_initial_data(self):
        libros = self.model.get_all_libros()
        self.view.update_treeview(libros)
        
    def search_libros(self, event=None):
        search_term = self.view.get_search_term()
        libros = self.model.get_all_libros(search_term)
        self.view.update_treeview(libros)
        
    def delete_libro(self):
        libro_id = self.view.get_selected_libro_id()
        if not libro_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un libro para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el libro con ID {libro_id}?"):
            if self.model.delete_libro(libro_id):
                messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
                self.search_libros()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro.")
                
    def show_add_libro_dialog(self):
        dialog = self._create_libro_dialog("Nuevo Libro")
        dialog.save_button.config(command=lambda: self._save_new_libro(dialog))
    
    def _center_window(self, window, width, height):
        """Centra una ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_libro_dialog(self, title, data=None):
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
            ("titulo", "Titulo"),
            ("autor", "Autor"),
            ("isbn", "ISBN"),
            ("editorial", "Editorial"),
            ("año", "Año"),
            ("cantidad", "Cantidad"),
            ("categoria", "Categoría"),
        ]

        for i, (key, label_text) in enumerate(campos):
            label = tb.Label(lbl_frame, text=label_text + ":")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tb.Entry(lbl_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)

            dialog.entries[key] = entry

        # Si es para editar, rellenamos los campos
        if data:
            dialog.entries['titulo'].insert(0, data[1])
            dialog.entries['autor'].insert(0, data[2])
            dialog.entries['isbn'].insert(0, data[3])
            dialog.entries['editorial'].insert(0, data[4])
            dialog.entries['año'].insert(0, data[5])
            dialog.entries['cantidad'].insert(0, str(data[6]))
            dialog.entries['categoria'].insert(0, data[7])

        # Botones
        button_frame = tb.Frame(lbl_frame)
        button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=10)
        
        dialog.save_button = tb.Button(button_frame, text="Guardar", bootstyle="success")
        dialog.save_button.pack(side="left", padx=5)
        cancel_button = tb.Button(button_frame, text="Cancelar", bootstyle="secondary", command=dialog.destroy)
        cancel_button.pack(side="left", padx=5)

        return dialog
    
    def _save_new_libro(self, dialog):
        data = {key: entry.get() for key, entry in dialog.entries.items()}

        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        # Validación: ISBN ya registrado
        if self.model.get_libro_by_isbn(data['isbn']):
            messagebox.showerror("Error", "El ISBN ingresado ya está registrado.", parent=dialog)
            return

        next_id = self.model.get_next_id()
        libro_tuple = (
            next_id,
            data['titulo'],
            data['autor'],
            data['isbn'],
            data['editorial'],
            data['año'],
            data['cantidad'],
            data['categoria']
        )

        if self.model.add_libro(libro_tuple):
            messagebox.showinfo("Éxito", "Libro agregado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro.", parent=dialog)
        
    def show_edit_libro_dialog(self):
        libro_id = self.view.get_selected_libro_id()
        if not libro_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un libro para modificar.")
            return

        libro_data = self.model.get_libro_by_isbn(libro_id)
        if not libro_data:
            messagebox.showerror("Error", f"No se encontraron datos para el libro con ID {libro_id}.")
            return

        dialog = self._create_libro_dialog("Editar Libro", libro_data)
        dialog.save_button.config(command=lambda: self._save_updated_libro(dialog, libro_id))
        
    def _save_updated_libro(self, dialog, libro_id):
        data = {key: entry.get() for key, entry in dialog.entries.items()}

        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.", parent=dialog)
            return

        libro_tuple = (
            libro_id,
            data['titulo'],
            data['autor'],
            data['isbn'],
            data['editorial'],
            data['año'],
            data['cantidad'],
            data['categoria']
        )

        if self.model.update_libro(libro_tuple):
            messagebox.showinfo("Éxito", "Libro actualizado correctamente.", parent=dialog)
            dialog.destroy()
            self.load_initial_data()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el libro.", parent=dialog)