# file: views/libro_view.py

from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb

class LibroView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.create_widgets()
        
    def create_widgets(self):
        # Frame de botones
        lblframe_botones = tb.LabelFrame(self)
        lblframe_botones.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_nuevo = tb.Button(lblframe_botones, text='Nuevo', width=15, bootstyle='success', command=self.controller.show_add_libro_dialog)
        btn_nuevo.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar = tb.Button(lblframe_botones, text='Modificar', width=15, bootstyle='warning', command=self.controller.show_edit_libro_dialog)
        btn_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar = tb.Button(lblframe_botones, text='Eliminar', width=15, bootstyle='danger', command=self.controller.delete_libro)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=10)
        
        # Frame de búsqueda
        lblframe_busqueda = tb.LabelFrame(self, text="Buscar Libro")
        lblframe_busqueda.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.ent_buscar = tb.Entry(lblframe_busqueda)
        self.ent_buscar.pack(fill="x", padx=10, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.controller.search_libros)

        # Frame de la tabla (Treeview)
        lblframe_tree = tb.LabelFrame(self, text="Listado de Libros")
        lblframe_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lblframe_tree.rowconfigure(0, weight=1)
        lblframe_tree.columnconfigure(0, weight=1)

        columnas = ("id_libro", "titulo", "autor", "isbn", "editorial", "año", "cantidad", "categoria")
        self.tree_libros = tb.Treeview(lblframe_tree, columns=columnas, show='headings', bootstyle='primary')
        self.tree_libros.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        headers = {'ID': 80, 'Título': 250, 'Autor': 250, 'ISBN': 160, 'Editorial': 200, 'Año': 80, 'Cantidad': 80, 'Categoría': 100}
        for i, (header, width) in enumerate(headers.items()):
            self.tree_libros.heading(columnas[i], text=header, anchor=W)
            self.tree_libros.column(columnas[i], width=width)

        scrollbar = tb.Scrollbar(lblframe_tree, orient="vertical", command=self.tree_libros.yview, bootstyle="primary-round")
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,10), pady=10)
        self.tree_libros.configure(yscrollcommand=scrollbar.set)

    def update_treeview(self, libros_data):
        self.tree_libros.delete(*self.tree_libros.get_children())
        for libro in libros_data:
            self.tree_libros.insert("", END, values=libro)
            
    def get_search_term(self):
        return self.ent_buscar.get()

    def get_selected_libro_id(self):
        selection = self.tree_libros.focus()
        if selection:
            return self.tree_libros.item(selection)['values'][0]
        return None