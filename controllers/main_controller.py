# file: controllers/main_controller.py

from tkinter import messagebox
from views.main_view import MainView
from views.login_view import LoginView
from views.socio_view import SocioView
from views.libro_view import LibroView
from views.prestamo_view import PrestamoView
from views.usuario_view import UsuarioView # << 1. Importar la nueva vista
from views.perfil_view import PerfilView           # << 1. Importar nueva vista
from controllers.perfil_controller import PerfilController # << 2. Importar nuevo controlador
from controllers.socio_controller import SocioController
from controllers.libro_controller import LibroController
from controllers.prestamo_controller import PrestamoController
from controllers.usuario_controller import UsuarioController # << 2. Importar el nuevo controlador
from views.reportes_view import ReportesView         # << 1. Importar nueva vista
from controllers.reportes_controller import ReportesController # << 2. Importar nuevo controlador
from models.usuario_model import UsuarioModel

class MainController:
    # ... (el __init__, run, login, logout permanecen igual) ...
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.usuario_model = UsuarioModel()
        self.logged_in_user_data = None

    def run(self):
        self.show_login_view()

    def show_login_view(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginView(self.root, self)

    def login(self, correo, clave):
        user_data = self.usuario_model.verify_credentials(correo, clave)
        if user_data:
            self.logged_in_user_data = user_data
            self.current_view.destroy()
            self.setup_main_interface()
        else:
            messagebox.showerror("Error de Acceso", "Correo o contraseña incorrectos.")

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar la sesión?"):
            self.logged_in_user_data = None
            self.current_view.destroy()
            self.show_login_view()

    def setup_main_interface(self):
        self.current_view = MainView(self.root, self)
        
        if self.logged_in_user_data:
            nombres = self.logged_in_user_data[3]
            apellidos = self.logged_in_user_data[2]
            full_name = f"{nombres} {apellidos}"
            self.current_view.set_user_name(full_name)

        # Añadimos los botones del menú
        self.current_view.add_menu_button("Socios", self.show_socios_view)
        self.current_view.add_menu_button("Libros", self.show_libros_view)
        self.current_view.add_menu_button("Préstamos", self.show_prestamos_view)
        self.current_view.add_menu_button("Reportes", self.show_reportes_view)
        
        # << 3. LÓGICA DE ROL >>
        # Solo muestra el botón "Usuarios" si el rol es "Administrador"
        if self.logged_in_user_data and self.logged_in_user_data[5] == 'Administrador':
            self.current_view.add_menu_button("Usuarios", self.show_usuarios_view)
        
        self.show_welcome_view()

    # ... (show_socios_view, show_libros_view, show_prestamos_view sin cambios) ...
    def show_socios_view(self):
        socio_controller = SocioController(None)
        socio_view = self.current_view.set_central_view(SocioView, socio_controller)
        socio_controller.view = socio_view
        socio_controller.load_initial_data()
        
    def show_libros_view(self):
        libro_controller = LibroController(None)
        libro_view = self.current_view.set_central_view(LibroView, libro_controller)
        libro_controller.view = libro_view
        libro_controller.load_initial_data()

    def show_prestamos_view(self):
        prestamo_controller = PrestamoController(None)
        prestamo_view = self.current_view.set_central_view(PrestamoView, prestamo_controller)
        prestamo_controller.view = prestamo_view
        prestamo_controller.load_initial_data()

    # << 3. NUEVO MÉTODO PARA MOSTRAR LA VISTA DE PERFIL >>
    def show_perfil_view(self):
        user_id = self.logged_in_user_data[0] # Obtenemos el ID del usuario logueado
        
        perfil_controller = PerfilController(None, self, user_id)
        perfil_view = self.current_view.set_central_view(PerfilView, perfil_controller)
        perfil_controller.view = perfil_view
        perfil_controller.load_user_data()

    # << 4. NUEVO MÉTODO PARA ACTUALIZAR EL HEADER >>
    def refresh_user_header(self):
        """ Vuelve a cargar los datos del usuario y actualiza el nombre en el header. """
        user_id = self.logged_in_user_data[0]
        self.logged_in_user_data = self.usuario_model.get_user_by_id(user_id)
        
        if self.logged_in_user_data:
            nombres = self.logged_in_user_data[3]
            apellidos = self.logged_in_user_data[2]
            full_name = f"{nombres} {apellidos}"
            # self.current_view es MainView, que tiene el método set_user_name
            self.current_view.set_user_name(full_name)

    # << 4. MÉTODO PARA MOSTRAR LA VISTA DE USUARIOS >>
    def show_usuarios_view(self):
        usuario_controller = UsuarioController(None)
        usuario_view = self.current_view.set_central_view(UsuarioView, usuario_controller)
        usuario_controller.view = usuario_view
        usuario_controller.load_initial_data()

    # << 4. MÉTODO PARA MOSTRAR LA VISTA DE REPORTES >>
    def show_reportes_view(self):
        reportes_controller = ReportesController(None)
        reportes_view = self.current_view.set_central_view(ReportesView, reportes_controller)
        reportes_controller.view = reportes_view
        reportes_controller.load_initial_report() 

    def show_welcome_view(self):
        self.current_view.show_welcome()