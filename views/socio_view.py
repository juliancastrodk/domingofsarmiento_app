# file: views/socio_view.py

from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb

class SocioView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configurar grid del frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # --- Widgets ---
        self.create_widgets()
        
    def create_widgets(self):
        # Frame de botones
        lblframe_botones = tb.LabelFrame(self)
        lblframe_botones.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_nuevo = tb.Button(lblframe_botones, text='Nuevo', width=15, bootstyle='success', command=self.controller.show_add_socio_dialog)
        btn_nuevo.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar = tb.Button(lblframe_botones, text='Modificar', width=15, bootstyle='warning', command=self.controller.show_edit_socio_dialog)
        btn_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar = tb.Button(lblframe_botones, text='Eliminar', width=15, bootstyle='danger', command=self.controller.delete_socio)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=10)
        
        # Frame de búsqueda
        lblframe_busqueda = tb.LabelFrame(self, text="Buscar Socio")
        lblframe_busqueda.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.ent_buscar = tb.Entry(lblframe_busqueda)
        self.ent_buscar.pack(fill="x", padx=10, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.controller.search_socios)

        # Frame de la tabla (Treeview)
        lblframe_tree = tb.LabelFrame(self, text="Listado de Socios")
        lblframe_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lblframe_tree.rowconfigure(0, weight=1)
        lblframe_tree.columnconfigure(0, weight=1)

        columnas = ("id_socio", "dni", "apellidos", "nombres", "telefono", "direccion", "estado", "prestamos_activos")
        self.tree_socios = tb.Treeview(lblframe_tree, columns=columnas, show='headings', bootstyle='primary')
        self.tree_socios.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Encabezados y tamaño de columnas
        headers = {'ID': 80, 'D.N.I': 100, 'Apellidos': 250, 'Nombres': 250, 'Teléfono': 100, 'Dirección': 200, 'Estado': 120, 'Préstamos': 100}
        for i, (header, width) in enumerate(headers.items()):
            self.tree_socios.heading(columnas[i], text=header, anchor=W)
            self.tree_socios.column(columnas[i], width=width)

        # Scrollbar
        scrollbar = tb.Scrollbar(lblframe_tree, orient="vertical", command=self.tree_socios.yview, bootstyle="primary-round")
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,10), pady=10)
        self.tree_socios.configure(yscrollcommand=scrollbar.set)

    def update_treeview(self, socios_data):
        """ Limpia y rellena la tabla con nuevos datos. """
        self.tree_socios.delete(*self.tree_socios.get_children())
        for socio in socios_data:
            self.tree_socios.insert("", END, values=socio)
            
    def get_search_term(self):
        """ Devuelve el texto del campo de búsqueda. """
        return self.ent_buscar.get()

    def get_selected_socio_id(self):
        """ Devuelve el ID del socio seleccionado en la tabla. """
        selection = self.tree_socios.focus()
        if selection:
            item = self.tree_socios.item(selection)
            return item['values'][0] # El ID está en la primera columna
        return None