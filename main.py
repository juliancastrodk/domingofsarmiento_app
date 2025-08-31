# file: main.py

import ttkbootstrap as tb
from controllers.main_controller import MainController

def main():
    app = tb.Window(themename="yeti")
    app.title('Sistema de Gestión de Socios y Control de Libros')
    app.iconbitmap("./imagenes/logo.ico")

    # Geometría y centrado
    width, height = 1430, 750
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.resizable(False, False)

    controller = MainController(app)
    controller.run() # Inicia la aplicación
    
    app.mainloop()
    
if __name__ == '__main__':
    main()