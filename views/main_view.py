# file: views/main_view.py

from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.widgets import Menubutton
from PIL import Image, ImageTk

class MainView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill=BOTH, expand=True)
        
        # Guardar la imagen del ícono para que no sea eliminada por el recolector de basura
        self.user_icon = None
        
        self.create_layout()

    def create_layout(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # Diseño del header
        self.header = tb.Frame(self, bootstyle="light")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Frame para alinear los elementos del usuario a la derecha del header
        # 1. ELIMINADO: Eliminar el bootstyle "light" aquí.
        #    Esto permite que el user_frame herede un fondo que permita la transparencia visual del icono.
        user_frame = tb.Frame(self.header) 
        user_frame.pack(side="right", padx=10, pady=5)

        # Creación del menú desplegable
        self.user_menubutton = Menubutton(user_frame, text="Usuario", bootstyle="light")
        self.user_menubutton.pack(side="right", padx=(5, 0))

        # Creamos el menú que se asociará con el Menubutton
        menu = tb.Menu(self.user_menubutton)
        
        # Añadimos opciones al menú
        menu.add_command(label="Mi Perfil", command=self.controller.show_perfil_view)
        menu.add_separator()
        menu.add_command(label="Cerrar Sesión", command=self.controller.logout)

        # Asociamos el menú al botón
        self.user_menubutton["menu"] = menu

        # Carga y muestra del ícono de usuario
        try:
            img = Image.open("imagenes/user_icon_transparente.png").resize((24, 24), Image.Resampling.LANCZOS)
            self.user_icon = ImageTk.PhotoImage(img)
            
            # 2. ELIMINADO: Eliminar el bootstyle "light" del icon_label.
            #    Esto es CRÍTICO para que el Label no imponga un fondo blanco.
            icon_label = tb.Label(user_frame, image=self.user_icon)
            icon_label.pack(side="right")
        except Exception as e:
            # En caso de error, se usa un texto alternativo
            print(f"Error cargando user_icon.png: {e}")
            icon_label = tb.Label(user_frame, text="👤", bootstyle="primary", font=("", 14))
            icon_label.pack(side="right")

        # --- Menú lateral ---
        self.frame_left = tb.Frame(self, width=200, bootstyle="light")
        self.frame_left.grid(row=1, column=0, sticky="ns")

        # --- Contenido central ---
        self.frame_center = tb.Frame(self)
        self.frame_center.grid(row=1, column=1, sticky="nsew")
        self.frame_center.columnconfigure(0, weight=1)
        self.frame_center.rowconfigure(0, weight=1)

    def set_user_name(self, name):
        """
        Actualiza el texto del Menubutton con el nombre del usuario.
        """
        self.user_menubutton.config(text=name)
        
    def add_menu_button(self, text, command):
        btn = tb.Button(self.frame_left, text=text, bootstyle="info-outline", command=command)
        btn.pack(fill="x", padx=10, pady=5, ipady=5)
        
    def set_central_view(self, view_class, controller):
        for widget in self.frame_center.winfo_children():
            widget.destroy()
        
        view_instance = view_class(self.frame_center, controller)
        view_instance.pack(fill=BOTH, expand=True)
        return view_instance

    def show_welcome(self):
        for widget in self.frame_center.winfo_children():
            widget.destroy()
        
        lbl_bienvenida = tb.Label(self.frame_center, text="¡Bienvenido al Sistema!", font=("Montserrat", 25, "bold"), anchor="center")
        lbl_bienvenida.pack(pady=(50, 10))
        
        lbl_descripcion = tb.Label(self.frame_center, text="Selecciona una opción del menú lateral para comenzar", font=("Calibri", 14), anchor="center")
        lbl_descripcion.pack()