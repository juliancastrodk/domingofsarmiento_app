# file: views/login_view.py

from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk

class LoginView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Centrar el contenido
        self.pack(expand=True)
        
        lblframe_login = tb.LabelFrame(self, text="Iniciar Sesión", bootstyle="primary")
        lblframe_login.pack(padx=20, pady=20)
        
        # Logo
        try:
            logo_img = Image.open("imagenes/logo.png").resize((120, 120))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            lbl_logo = tb.Label(lblframe_login, image=self.logo_photo)
            lbl_logo.pack(pady=10)
        except FileNotFoundError:
            lbl_logo = tb.Label(lblframe_login, text="Logo no encontrado")
            lbl_logo.pack(pady=10)

        # Entries
        self.ent_usuario = tb.Entry(lblframe_login, width=40, font=("Calibri", 12))
        self.ent_usuario.pack(padx=20, pady=10)
        self.ent_usuario.insert(0, "Ingrese su correo")
        
        self.ent_clave = tb.Entry(lblframe_login, width=40, font=("Calibri", 12))
        self.ent_clave.pack(padx=20, pady=10)
        self.ent_clave.insert(0, "Ingrese su contraseña")

        self.setup_placeholders()

        # Botón
        btn_acceso = tb.Button(lblframe_login, text='Ingresar', bootstyle='primary-outline', command=self.on_login_click)
        btn_acceso.pack(pady=20, ipady=5, fill='x', padx=20)

    def on_login_click(self):
        user = self.ent_usuario.get()
        pwd = self.ent_clave.get()
        self.controller.login(user, pwd)

    def setup_placeholders(self):
        # Lógica de placeholder para usuario
        def user_focus_in(e):
            if self.ent_usuario.get() == "Ingrese su correo":
                self.ent_usuario.delete(0, "end")
        def user_focus_out(e):
            if not self.ent_usuario.get():
                self.ent_usuario.insert(0, "Ingrese su correo")
        self.ent_usuario.bind("<FocusIn>", user_focus_in)
        self.ent_usuario.bind("<FocusOut>", user_focus_out)

        # Lógica de placeholder para clave
        def pass_focus_in(e):
            if self.ent_clave.get() == "Ingrese su contraseña":
                self.ent_clave.delete(0, "end")
                self.ent_clave.config(show="*")
        def pass_focus_out(e):
            if not self.ent_clave.get():
                self.ent_clave.config(show="")
                self.ent_clave.insert(0, "Ingrese su contraseña")
        self.ent_clave.bind("<FocusIn>", pass_focus_in)
        self.ent_clave.bind("<FocusOut>", pass_focus_out)