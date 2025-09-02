# file: controllers/prestamo_controller.py

from tkinter import Toplevel,messagebox,END,W,StringVar,CENTER
import ttkbootstrap as tb
from datetime import datetime,timedelta
from models.prestamo_model import PrestamoModel
from models.socio_model import SocioModel
from models.libro_model import LibroModel

class PrestamoController:
    def __init__(self, view):
        self.view = view
        self.model = PrestamoModel()
        self.socio_model = SocioModel()
        self.libro_model = LibroModel()

    def load_initial_data(self):
        prestamos = self.model.get_all_prestamos()
        self.view.update_treeview(prestamos)

    def search_prestamos(self, event=None):
        search_term = self.view.get_search_term()
        prestamos = self.model.get_all_prestamos(search_term)
        self.view.update_treeview(prestamos)

    def devolver_prestamo(self):
        selected = self.view.get_selected_prestamo()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, seleccione un préstamo para devolver.")
            return
            
        if selected['estado'] == 'Devuelto':
            messagebox.showinfo("Información", "Este préstamo ya ha sido devuelto.")
            return

        prestamo_id = selected['id']
        if messagebox.askyesno("Confirmar Devolución", f"¿Confirma la devolución del préstamo ID {prestamo_id}?"):
            if self.model.devolver_prestamo(prestamo_id):
                messagebox.showinfo("Éxito", "Préstamo devuelto correctamente.")
                self.search_prestamos()
            else:
                messagebox.showerror("Error", "Ocurrió un error al procesar la devolución.")

    def show_create_prestamo_dialog(self):
        dialog = self._create_prestamo_dialog("Nuevo Préstamo")
        dialog.save_button.config(command=lambda: self._save_new_prestamo(dialog))
        
    def _center_window(self, window, width, height):
        """Centra una ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def refresh_table(self):
        """Recarga los préstamos en la vista."""
        prestamos = self.model.get_all_prestamos()
        self.view.update_treeview(prestamos)

    def _create_prestamo_dialog(self, title, data=None):
        dialog = Toplevel(self.view)
        dialog.title(title)
        dialog.transient(self.view)
        dialog.grab_set()
        
        # Centrar la ventana
        self._center_window(dialog, 530, 340)
        
        lbl_frame = tb.LabelFrame(dialog, text=title, padding=(15, 10))
        lbl_frame.pack(padx=15, pady=15, fill="both", expand=True)

        dialog.entries = {}
        
        # Determinar si es edición
        is_edit = data is not None
        
        # ==========================
        # Fecha Retiro
        # ==========================
        if is_edit:
            fecha_retiro = data['fecha_retiro']  # Usar fecha del préstamo existente
        else:
            fecha_retiro = datetime.now().date().strftime("%Y-%m-%d")
            
        label_retiro = tb.Label(lbl_frame, text="Fecha Retiro:")
        label_retiro.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_retiro = tb.Entry(lbl_frame, width=38)
        entry_retiro.grid(row=0, column=1, padx=5, pady=5)
        entry_retiro.insert(0, fecha_retiro)
        entry_retiro.config(state="readonly")
        dialog.entries['fecha_retiro'] = entry_retiro

        # ==========================
        # Fecha Devolución
        # ==========================
        if is_edit:
            fecha_devolucion = data['fecha_devolucion']  # Usar fecha del préstamo existente
        else:
            fecha_devolucion = (datetime.now().date() + timedelta(days=10)).strftime("%Y-%m-%d")
            
        label_devolucion = tb.Label(lbl_frame, text="Fecha Devolución:")
        label_devolucion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_devolucion = tb.Entry(lbl_frame, width=38)
        entry_devolucion.grid(row=1, column=1, padx=5, pady=5)
        entry_devolucion.insert(0, fecha_devolucion)
        entry_devolucion.config(state="readonly")
        dialog.entries['fecha_devolucion'] = entry_devolucion

        # ==========================
        # Seleccionar Socio
        # ==========================
        frame_socio = tb.Frame(lbl_frame)
        frame_socio.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        btn_socio = tb.Button(frame_socio, text="Seleccionar Socio", width=15, bootstyle="info",
                            command=lambda: self._select_socio(dialog))
        btn_socio.pack(side="left")
        
        # Deshabilitar botón de socio si es edición
        if is_edit:
            btn_socio.config(state="disabled")
        
        entry_socio = tb.Entry(frame_socio, width=38, state="readonly")
        entry_socio.pack(side="left", padx=5)
        dialog.entries['socio'] = entry_socio

        # ==========================
        # Seleccionar Libros
        # ==========================
        frame_libros = tb.Frame(lbl_frame)
        frame_libros.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        btn_libros = tb.Button(frame_libros, text="Seleccionar Libros", width=15, bootstyle="info",
                            command=lambda: self._select_libros(dialog))
        btn_libros.pack(side="left")
        
        entry_libros = tb.Entry(frame_libros, width=38, state="readonly")
        entry_libros.pack(side="left", padx=5)
        dialog.entries['libros'] = entry_libros

        # ==========================
        # Estado
        # ==========================
        label_estado = tb.Label(lbl_frame, text="Estado:")
        label_estado.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        entry_estado = tb.Entry(lbl_frame, width=38, state="readonly")
        entry_estado.grid(row=4, column=1, padx=5, pady=5)
        entry_estado.config(state="normal")
        entry_estado.insert(0, "Prestado")
        entry_estado.config(state="readonly")
        dialog.entries['estado'] = entry_estado

        # ==========================
        # Cargar datos si es edición
        # ==========================
        if is_edit:
            # Cargar información del socio
            socio_info = self.socio_model.get_socio_by_id(data['id_socio'])
            if socio_info:
                socio_nombre = f"{socio_info[1]} {socio_info[2]}"  # nombres + apellidos
                entry_socio.config(state="normal")
                entry_socio.insert(0, socio_nombre)
                entry_socio.config(state="readonly")
                dialog.selected_socio_id = data['id_socio']
            
            # Cargar libros seleccionados
            if data['libros']:
                libros_nombres = []
                for libro_id in data['libros']:
                    libro_info = self.libro_model.get_libro_by_id(libro_id)
                    if libro_info:
                        libros_nombres.append(libro_info[1])  # título del libro
                
                entry_libros.config(state="normal")
                entry_libros.insert(0, ", ".join(libros_nombres))
                entry_libros.config(state="readonly")
                dialog.selected_libros_ids = data['libros']

        # ==========================
        # Botones
        # ==========================
        button_frame = tb.Frame(lbl_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        dialog.save_button = tb.Button(button_frame, text="Guardar", bootstyle="success")
        dialog.save_button.pack(side="left", padx=5)
        cancel_button = tb.Button(button_frame, text="Cancelar", bootstyle="secondary", command=dialog.destroy)
        cancel_button.pack(side="left", padx=5)

        return dialog

    def _socio_tiene_prestamos_activos(self, socio_id):
        """Verificar si el socio tiene préstamos en estado Prestado o Demorado"""
        try:
            from database.database_manager import DatabaseManager
            with DatabaseManager() as cursor:
                if cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM prestamos 
                        WHERE id_socio = ? AND estado IN ('Prestado', 'Demorado')
                    """, (socio_id,))
                    count = cursor.fetchone()[0]
                    return count > 0
            return True  # En caso de error, asumir que tiene préstamos
        except Exception as e:
            print(f"Error verificando préstamos del socio {socio_id}: {e}")
            return True

    def _select_socio(self, dialog):
        win = Toplevel(self.view)
        win.title("Seleccionar Socio (Solo socios disponibles)")
        win.transient(self.view)
        win.grab_set()
        self._center_window(win, 700, 500)

        # Frame principal
        main_frame = tb.Frame(win)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo de búsqueda
        search_frame = tb.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tb.Label(search_frame, text="Buscar Socio:").pack(side="left", padx=(0, 5))
        search_entry = tb.Entry(search_frame, width=40)
        search_entry.pack(side="left", fill="x", expand=True)

        # Treeview para mostrar socios
        tree_frame = tb.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        tree = tb.Treeview(tree_frame, columns=("id", "dni", "nombre", "estado_prestamo"), show="headings", height=12, bootstyle='primary')
        tree.heading("id", text="ID", anchor=CENTER)
        tree.heading("dni", text="DNI", anchor=CENTER)
        tree.heading("nombre", text="Apellidos y Nombres", anchor=W)
        tree.heading("estado_prestamo", text="Estado", anchor=CENTER)
        
        tree.column("id", width=70, anchor=CENTER)
        tree.column("dni", width=100, anchor=CENTER)
        tree.column("nombre", width=250, anchor=W)
        tree.column("estado_prestamo", width=120, anchor=CENTER)
        
        # Scrollbar
        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=tree.yview, bootstyle='primary-round')
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def load_socios(search_term=""):
            # Limpiar el treeview
            for item in tree.get_children():
                tree.delete(item)
            
            # Obtener todos los socios con filtro de búsqueda
            socios = self.socio_model.get_all_socios(search_term)
            
            # Filtrar solo socios que pueden hacer préstamos
            for socio in socios:
                # socio: (Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos)
                socio_id = socio[0]
                
                # Solo mostrar socios activos
                if socio[6] != 'Activo':  # socio[6] es el estado del socio
                    continue
                
                # Verificar si tiene préstamos activos usando el modelo
                tiene_prestamos = self._socio_tiene_prestamos_activos(socio_id)
                
                nombre_completo = f"{socio[2]}, {socio[3]}"  # apellidos, nombres
                
                if tiene_prestamos:
                    # Mostrar en rojo con estado "Con préstamos"
                    item = tree.insert("", "end", values=(socio[0], socio[1], nombre_completo, "Con préstamos"))
                    tree.set(item, "estado_prestamo", "Con préstamos")
                    # Deshabilitar visualmente (opcional)
                    tree.item(item, tags=("disabled",))
                else:
                    # Mostrar en verde como "Disponible"
                    item = tree.insert("", "end", values=(socio[0], socio[1], nombre_completo, "Disponible"))
                    tree.set(item, "estado_prestamo", "Disponible")
                    tree.item(item, tags=("available",))
            
            # Configurar colores para los tags
            tree.tag_configure("disabled", foreground="red")
            tree.tag_configure("available", foreground="green")

        def on_search(event=None):
            search_term = search_entry.get()
            load_socios(search_term)

        # Vincular búsqueda al Entry
        search_entry.bind("<KeyRelease>", on_search)

        # Cargar todos los socios inicialmente
        load_socios()

        def seleccionar():
            selected = tree.focus()
            if selected:
                values = tree.item(selected)["values"]
                
                # Verificar que sea un socio disponible
                if values[3] == "Con préstamos":
                    messagebox.showwarning("Socio no disponible", 
                        "Este socio tiene préstamos pendientes. Debe devolver antes de solicitar otro préstamo.", 
                        parent=win)
                    return
                
                dialog.entries["socio"].config(state="normal")
                dialog.entries["socio"].delete(0, "end")
                # Mostrar: "DNI - Apellidos, Nombres"
                dialog.entries["socio"].insert(0, f"{values[1]} - {values[2]}")
                dialog.entries["socio"].config(state="readonly")
                
                # Guardar el ID del socio seleccionado
                dialog.socio_id = values[0]
                
                win.destroy()
            else:
                messagebox.showwarning("Selección", "Por favor, seleccione un socio.", parent=win)

        # Botones
        button_frame = tb.Frame(main_frame)
        button_frame.pack(fill="x")
        
        btn_select = tb.Button(button_frame, text="Seleccionar", bootstyle="success", command=seleccionar)
        btn_select.pack(side="right", padx=(5, 0))
        
        btn_cancel = tb.Button(button_frame, text="Cancelar", bootstyle="secondary", command=win.destroy)
        btn_cancel.pack(side="right")

        # Permitir selección con doble clic (solo para disponibles)
        def on_double_click(event):
            selected = tree.focus()
            if selected:
                values = tree.item(selected)["values"]
                if values[3] == "Disponible":
                    seleccionar()
                else:
                    messagebox.showwarning("Socio no disponible", 
                        "Este socio tiene préstamos pendientes.", parent=win)
        
        tree.bind("<Double-1>", on_double_click)
        
        # Focus en el campo de búsqueda
        search_entry.focus()

    def _select_libros(self, dialog):
        win = Toplevel(self.view)
        win.title("Seleccionar Libros (máximo 3)")
        win.transient(self.view)
        win.grab_set()
        self._center_window(win, 800, 520)

        # Frame principal
        main_frame = tb.Frame(win)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo de búsqueda
        search_frame = tb.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tb.Label(search_frame, text="Buscar Libro:").pack(side="left", padx=(0, 5))
        search_entry = tb.Entry(search_frame, width=40)
        search_entry.pack(side="left", fill="x", expand=True)

        # Treeview para mostrar libros disponibles
        tree_frame = tb.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        tree = tb.Treeview(tree_frame, columns=("id", "titulo", "autor", "isbn", "cantidad"), show="headings", height=10, bootstyle='primary')
        tree.heading("id", text="ID", anchor=CENTER)
        tree.heading("titulo", text="Título", anchor=W)
        tree.heading("autor", text="Autor", anchor=W)
        tree.heading("isbn", text="ISBN", anchor=CENTER)
        tree.heading("cantidad", text="Disponibles", anchor=CENTER)
        
        tree.column("id", width=70, anchor=CENTER)
        tree.column("titulo", width=250, anchor=W)
        tree.column("autor", width=200, anchor=W)
        tree.column("isbn", width=120, anchor=CENTER)
        tree.column("cantidad", width=90, anchor=CENTER)
        
        # Scrollbar
        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=tree.yview, bootstyle='primary-round')
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para libros seleccionados
        selected_frame = tb.LabelFrame(main_frame, text="Libros Seleccionados", padding=10)
        selected_frame.pack(fill="x", pady=(10, 0))

        # Lista para mostrar libros seleccionados
        selected_listbox = tb.Treeview(selected_frame, columns=("titulo", "autor"), show="headings", height=3, bootstyle='info')
        selected_listbox.heading("titulo", text="Título", anchor=W)
        selected_listbox.heading("autor", text="Autor", anchor=W)
        selected_listbox.column("titulo", width=300, anchor=W)
        selected_listbox.column("autor", width=200, anchor=W)
        selected_listbox.pack(fill="x")

        # Lista para almacenar libros seleccionados
        libros_seleccionados = []

        def cargar_libros(search_term=""):
            """Cargar libros disponibles en el treeview"""
            tree.delete(*tree.get_children())
            libros = self.libro_model.get_all_libros(search_term)
            
            for libro in libros:
                if libro[6] > 0:  # Solo libros con cantidad disponible > 0
                    tree.insert("", "end", values=(libro[0], libro[1], libro[2], libro[3], libro[6]))

        def buscar_libros(event=None):
            """Filtrar libros por término de búsqueda"""
            search_term = search_entry.get().strip()
            cargar_libros(search_term)

        def agregar_libro():
            """Agregar libro seleccionado a la lista"""
            if len(libros_seleccionados) >= 3:
                messagebox.showwarning("Límite alcanzado", "Solo puede seleccionar máximo 3 libros.")
                return
            
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Sin selección", "Por favor, seleccione un libro.")
                return
            
            item = tree.item(selection[0])
            libro_id = item['values'][0]
            libro_titulo = item['values'][1]
            libro_autor = item['values'][2]
            
            # Verificar si ya está seleccionado
            if libro_id in [lib['id'] for lib in libros_seleccionados]:
                messagebox.showwarning("Libro duplicado", "Este libro ya está seleccionado.")
                return
            
            # Agregar a la lista
            libros_seleccionados.append({
                'id': libro_id,
                'titulo': libro_titulo,
                'autor': libro_autor
            })
            
            # Actualizar la vista de seleccionados
            selected_listbox.insert("", "end", values=(libro_titulo, libro_autor))

        def quitar_libro():
            """Quitar libro de la lista de seleccionados"""
            selection = selected_listbox.selection()
            if not selection:
                messagebox.showwarning("Sin selección", "Por favor, seleccione un libro para quitar.")
                return
            
            # Obtener índice del item seleccionado
            index = selected_listbox.index(selection[0])
            
            # Quitar de la lista
            libros_seleccionados.pop(index)
            
            # Quitar de la vista
            selected_listbox.delete(selection[0])

        def confirmar_seleccion():
            """Confirmar la selección y cerrar ventana"""
            if not libros_seleccionados:
                messagebox.showwarning("Sin libros", "Debe seleccionar al menos un libro.")
                return
            
            # Actualizar el entry de libros en el diálogo principal
            entry_libros = dialog.entries['libros']
            libros_nombres = [libro['titulo'] for libro in libros_seleccionados]
            
            entry_libros.config(state="normal")
            entry_libros.delete(0, "end")
            entry_libros.insert(0, ", ".join(libros_nombres))
            entry_libros.config(state="readonly")
            
            # ✅ Guardar los IDs en el diálogo principal (usando libros_ids)
            dialog.libros_ids = [libro['id'] for libro in libros_seleccionados]
            
            win.destroy()

        # Botones
        buttons_frame = tb.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        tb.Button(buttons_frame, text="Agregar ➤", command=agregar_libro, bootstyle="success").pack(side="left", padx=(0, 5))
        tb.Button(buttons_frame, text="⟵ Quitar", command=quitar_libro, bootstyle="warning").pack(side="left", padx=(0, 5))
        tb.Button(buttons_frame, text="Confirmar", command=confirmar_seleccion, bootstyle="info").pack(side="right", padx=(5, 0))
        tb.Button(buttons_frame, text="Cancelar", command=win.destroy, bootstyle="secondary").pack(side="right")

        # Eventos
        search_entry.bind('<KeyRelease>', buscar_libros)
        tree.bind('<Double-1>', lambda e: agregar_libro())

        # Si es edición, cargar libros ya seleccionados
        if hasattr(dialog, 'libros_ids') and dialog.libros_ids:
            for libro_id in dialog.libros_ids:
                libro_info = self.libro_model.get_libro_by_id(libro_id)
                if libro_info:
                    libros_seleccionados.append({
                        'id': libro_info[0],
                        'titulo': libro_info[1],
                        'autor': libro_info[2]
                    })
                    selected_listbox.insert("", "end", values=(libro_info[1], libro_info[2]))

        # Cargar libros inicialmente
        cargar_libros()

    def _save_new_prestamo(self, dialog):
        # recoger valores de los entries
        fecha_retiro = dialog.entries['fecha_retiro'].get()
        fecha_devolucion = dialog.entries['fecha_devolucion'].get()
        estado = "Prestado"  # Asegurar que use el mismo formato que tu BD

        # validar socio y libros
        if not hasattr(dialog, "socio_id"):
            messagebox.showwarning("Atención", "Debe seleccionar un socio.")
            return
        if not hasattr(dialog, "libros_ids") or not dialog.libros_ids:
            messagebox.showwarning("Atención", "Debe seleccionar al menos un libro.")
            return

        socio_id = dialog.socio_id
        libros_ids = dialog.libros_ids

        # guardar en la base de datos
        resultado = self.model.add_prestamo(
            fecha_retiro, fecha_devolucion, socio_id, libros_ids, estado
        )

        # Manejar la nueva respuesta del modelo
        if isinstance(resultado, dict):
            if resultado["success"]:
                messagebox.showinfo("Éxito", f"Préstamo registrado correctamente con ID: {resultado['prestamo_id']}")
                dialog.destroy()
                self.refresh_table()
            else:
                messagebox.showerror("Error", resultado["error"])
        else:
            if resultado:
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
                dialog.destroy()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "No se pudo registrar el préstamo.")
    
    def show_edit_prestamo_dialog(self):
        prestamo_seleccionado = self.view.get_selected_prestamo()
        
        if not prestamo_seleccionado:
            messagebox.showwarning("Atención", "Por favor, seleccione un préstamo para modificar.")
            return

        print(f"Préstamo seleccionado: {prestamo_seleccionado}")
        print(f"Tipo: {type(prestamo_seleccionado)}")
        
        try:
            # Extraer el ID del diccionario
            if isinstance(prestamo_seleccionado, dict) and 'id' in prestamo_seleccionado:
                prestamo_id = prestamo_seleccionado['id']  # Cambio aquí
            else:
                messagebox.showerror("Error", "Formato de préstamo seleccionado no válido.")
                return
                
            print(f"ID del préstamo extraído: {prestamo_id}")
            
        except (KeyError, TypeError) as e:
            messagebox.showerror("Error", f"Error al obtener el ID del préstamo: {e}")
            return

        prestamo_data = self.model.get_prestamo_by_id(prestamo_id)
        if not prestamo_data:
            messagebox.showerror("Error", f"No se encontraron datos para el préstamo con ID {prestamo_id}.")
            return

        dialog = self._create_prestamo_dialog("Editar Préstamo", prestamo_data)
        dialog.save_button.config(command=lambda: self._save_updated_prestamo(dialog, prestamo_id))
        
    def _save_updated_prestamo(self, dialog, prestamo_id):
        try:
            # Obtener los nuevos libros seleccionados desde el atributo del diálogo
            if hasattr(dialog, 'libros_ids') and dialog.libros_ids:
                nuevos_libros = dialog.libros_ids
            else:
                messagebox.showwarning("Atención", "Debe seleccionar al menos un libro.")
                return
            
            # Validar disponibilidad de los nuevos libros
            libros_no_disponibles = []
            for libro_id in nuevos_libros:
                libro_info = self.libro_model.get_libro_by_id(libro_id)
                if libro_info and libro_info[6] <= 0:  # Asumiendo que la cantidad está en el índice 6
                    titulo = libro_info[1]  # Asumiendo que el título está en el índice 1
                    libros_no_disponibles.append(titulo)
            
            if libros_no_disponibles:
                mensaje = "Los siguientes libros no están disponibles:\n" + "\n".join(libros_no_disponibles)
                messagebox.showerror("Error", mensaje)
                return
            
            # Actualizar los libros del préstamo
            if self.model.update_prestamo_libros(prestamo_id, nuevos_libros):
                messagebox.showinfo("Éxito", "Préstamo actualizado exitosamente.")
                dialog.destroy()
                self.load_prestamos()  # Recargar la lista de préstamos
            else:
                messagebox.showerror("Error", "Ocurrió un error al actualizar el préstamo.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def load_prestamos(self):
        prestamos = self.model.get_all_prestamos()  # consulta a la BD
        self.view.update_treeview(prestamos)