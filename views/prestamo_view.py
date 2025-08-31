# file: views/prestamo_view.py

from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb

class PrestamoView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.create_widgets()
        
    def create_widgets(self):
        lblframe_botones = tb.LabelFrame(self)
        lblframe_botones.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_nuevo = tb.Button(lblframe_botones, text='Crear Préstamo', width=17, bootstyle='success', command=self.controller.show_create_prestamo_dialog)
        btn_nuevo.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar = tb.Button(lblframe_botones, text='Modificar Préstamo', width=17, bootstyle='warning', command=self.controller.show_edit_prestamo_dialog)
        btn_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        btn_devolver = tb.Button(lblframe_botones, text='Devolver Préstamo', width=17, bootstyle='info', command=self.controller.devolver_prestamo)
        btn_devolver.grid(row=0, column=2, padx=10, pady=10)
        
        lblframe_busqueda = tb.LabelFrame(self, text="Buscar Préstamo (por socio, libro o estado)")
        lblframe_busqueda.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.ent_buscar = tb.Entry(lblframe_busqueda)
        self.ent_buscar.pack(fill="x", padx=10, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.controller.search_prestamos)

        lblframe_tree = tb.LabelFrame(self, text="Listado de Préstamos")
        lblframe_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lblframe_tree.rowconfigure(0, weight=1)
        lblframe_tree.columnconfigure(0, weight=1)

        columnas = ("id", "fecha_retiro", "fecha_devolucion", "socio", "libros", "estado")
        self.tree_prestamos = tb.Treeview(lblframe_tree, columns=columnas, show='headings', bootstyle='primary')
        self.tree_prestamos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        headers = {'ID': 80, 'Fecha Retiro': 160, 'Fecha Devolución': 160, 'Socio': 250, 'Libros': 450, 'Estado': 100}
        for i, (header, width) in enumerate(headers.items()):
            self.tree_prestamos.heading(columnas[i], text=header, anchor=W)
            self.tree_prestamos.column(columnas[i], width=width)

        scrollbar = tb.Scrollbar(lblframe_tree, orient="vertical", command=self.tree_prestamos.yview, bootstyle="primary-round")
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,10), pady=10)
        self.tree_prestamos.configure(yscrollcommand=scrollbar.set)

    def update_treeview(self, prestamos_data):
        self.tree_prestamos.delete(*self.tree_prestamos.get_children())
        for prestamo in prestamos_data:
            self.tree_prestamos.insert("", END, values=prestamo)
            
    def get_search_term(self):
        return self.ent_buscar.get()

    def get_selected_prestamo(self):
        selection = self.tree_prestamos.focus()
        if selection:
            item = self.tree_prestamos.item(selection)
            return {'id': item['values'][0], 'estado': item['values'][5]}
        return None