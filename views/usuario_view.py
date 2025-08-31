# file: views/usuario_view.py

from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb

class UsuarioView(tb.Frame):
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

        btn_nuevo = tb.Button(lblframe_botones, text='Nuevo Usuario', width=17, bootstyle='success', command=self.controller.show_add_usuario_dialog)
        btn_nuevo.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar = tb.Button(lblframe_botones, text='Modificar Usuario', width=17, bootstyle='warning', command=self.controller.show_edit_usuario_dialog)
        btn_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar = tb.Button(lblframe_botones, text='Eliminar Usuario', width=17, bootstyle='danger', command=self.controller.delete_usuario)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=10)

        # Frame de búsqueda
        lblframe_busqueda = tb.LabelFrame(self, text="Buscar Usuario")
        lblframe_busqueda.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.ent_buscar = tb.Entry(lblframe_busqueda)
        self.ent_buscar.pack(fill="x", padx=10, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.controller.search_usuarios)

        # Frame de la tabla (Treeview)
        lblframe_tree = tb.LabelFrame(self, text="Listado de Usuarios")
        lblframe_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lblframe_tree.rowconfigure(0, weight=1)
        lblframe_tree.columnconfigure(0, weight=1)

        columnas = ("codigo", "correo", "apellidos", "nombres", "clave", "rol")
        self.tree_usuarios = tb.Treeview(lblframe_tree, columns=columnas, show='headings', bootstyle='primary')
        self.tree_usuarios.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        headers = {'Código': 100, 'Correo': 300, 'Apellidos': 250, 'Nombres': 250, 'Clave': 150, 'Rol': 150}
        for i, (header, width) in enumerate(headers.items()):
            self.tree_usuarios.heading(columnas[i], text=header, anchor=W)
            self.tree_usuarios.column(columnas[i], width=width)

        scrollbar = tb.Scrollbar(lblframe_tree, orient="vertical", command=self.tree_usuarios.yview, bootstyle="primary-round")
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,10), pady=10)
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)

    def update_treeview(self, usuarios_data):
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())
        for usuario in usuarios_data:
            self.tree_usuarios.insert("", END, values=usuario)
            
    def get_search_term(self):
        return self.ent_buscar.get()

    def get_selected_user_id(self):
        selection = self.tree_usuarios.focus()
        if selection:
            return self.tree_usuarios.item(selection)['values'][0]
        return None