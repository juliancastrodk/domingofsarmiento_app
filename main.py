from tkinter import *
from tkinter import ttk,messagebox,StringVar,END,W,Toplevel
import ttkbootstrap as tb
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime, timedelta

#Ventana principal
class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        #self.ventana_login()
        self.ventana_menu()
        self.socio_seleccionado = None
        self.libro_seleccionado = None
        
#Login    
    def ventana_login(self):
        self.grid_columnconfigure(1,weight=1)
        
        self.frame_login=tb.Frame(master=self)
        self.frame_login.grid(row=0, column=1, sticky=NSEW)
        
        lblframe_login=tb.LabelFrame(master=self.frame_login)
        lblframe_login.pack(padx=10,pady=35)
        
        # ----- Logo -----
        logo_img = Image.open("imagenes/logo.png")  # Cambia por la ruta de tu logo
        logo_img = logo_img.resize((120, 120))  # Ajusta tamaño si quieres
        self.logo_photo = ImageTk.PhotoImage(logo_img)  # Guardar en self para evitar que se borre de memoria
        lbl_logo = tb.Label(master=lblframe_login, image=self.logo_photo)
        lbl_logo.pack(pady=(10, 5))  # Un poco de espacio abajo del logo
        
        lbl_titulo=tb.Label(master=lblframe_login,text='Iniciar sesión',font=('Calibri',18))
        lbl_titulo.pack(padx=10,pady=35)
        
        # ----- Entry Usuario + placeholder -----
        self.ent_usuario=tb.Entry(master=lblframe_login,width=40,justify=CENTER)
        self.ent_usuario.pack(padx=10,pady=10)
        _ph_user = "Ingrese su correo"
        self.ent_usuario.insert(0, _ph_user)
        self.ent_usuario.config(foreground="grey")
        def _user_focus_in(e):
            if self.ent_usuario.get() == _ph_user:
                self.ent_usuario.delete(0,"end")
                self.ent_usuario.config(foreground="black")
        def _user_focus_out(e):
            if self.ent_usuario.get() == "":
                self.ent_usuario.insert(0, _ph_user)
                self.ent_usuario.config(foreground="grey")
        self.ent_usuario.bind("<FocusIn>", _user_focus_in)
        self.ent_usuario.bind("<FocusOut>", _user_focus_out)

        # ----- Entry Clave + placeholder -----
        self.ent_clave=tb.Entry(master=lblframe_login,width=40,justify=CENTER)
        self.ent_clave.pack(padx=10,pady=10)
        _ph_pass = "Ingrese su contraseña"
        self.ent_clave.insert(0, _ph_pass)
        self.ent_clave.config(foreground="grey")
        def _pass_focus_in(e):
            if self.ent_clave.get() == _ph_pass:
                self.ent_clave.delete(0,"end")
                self.ent_clave.config(foreground="black")
                self.ent_clave.config(show="*")
        def _pass_focus_out(e):
            if self.ent_clave.get() == "":
                self.ent_clave.config(show="")
                self.ent_clave.insert(0, _ph_pass)
                self.ent_clave.config(foreground="grey")
        self.ent_clave.bind("<FocusIn>", _pass_focus_in)
        self.ent_clave.bind("<FocusOut>", _pass_focus_out)

        btn_acceso=tb.Button(master=lblframe_login,width=38,text='Ingresar',bootstyle='primary-outline',command=self.logueo_usuarios)
        btn_acceso.pack(padx=10,pady=10)
        
#Menu
    def ventana_menu(self):
        # ==================
        # CONFIGURACIÓN GRID PRINCIPAL
        # ==================
        self.rowconfigure(0, weight=0)   # fila superior (logout)
        self.rowconfigure(1, weight=1)   # fila central
        self.columnconfigure(0, weight=0)  # menú lateral
        self.columnconfigure(1, weight=1)  # contenido central

        # ------------------
        # 🔹 Frame superior (botón logout)
        # ------------------
        frame_top = Frame(master=self)
        frame_top.grid(row=0, column=0, columnspan=2, sticky="ew")
        frame_top.columnconfigure(0, weight=1)  # espacio expansible

        btn_logout = tb.Button(frame_top,text="Cerrar Sesión",bootstyle="danger-outline",command=self.cerrar_sesion)
        btn_logout.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # ------------------
        # 🔹 Menú lateral
        # ------------------
        self.frame_left = Frame(master=self, width=200)
        self.frame_left.grid(row=1, column=0, sticky=NSEW)

        btn_principal = Button(self.frame_left, text='Mi Perfil', width=15, height=2,command=self.ventana_mi_perfil)
        btn_principal.grid(row=0, column=0, padx=10, pady=10)

        btn_socios = Button(self.frame_left, text='Socios', width=15, height=2,command=self.ventana_lista_socios)
        btn_socios.grid(row=1, column=0, padx=10, pady=10)

        btn_libros = Button(self.frame_left, text='Libros', width=15, height=2,command=self.ventana_lista_libros)
        btn_libros.grid(row=2, column=0, padx=10, pady=10)

        btn_prestamos = Button(self.frame_left, text='Préstamos', width=15, height=2,command=self.ventana_lista_prestamos)
        btn_prestamos.grid(row=3, column=0, padx=10, pady=10)

        btn_reportes = Button(self.frame_left, text='Reportes', width=15, height=2)
        btn_reportes.grid(row=4, column=0, padx=10, pady=10)

        btn_usuarios = Button(self.frame_left, text='Usuarios', width=15, height=2,command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=5, column=0, padx=10, pady=10)

        # ------------------
        # 🔹 Contenido central
        # ------------------
        self.frame_center = Frame(master=self)
        self.frame_center.grid(row=1, column=1, sticky=NSEW)
        
        # Configurar el frame center para centrar contenido
        self.frame_center.rowconfigure(0, weight=0)  # Fila de bienvenida
        self.frame_center.rowconfigure(1, weight=1)  # Fila expansible para logos
        self.frame_center.columnconfigure(0, weight=1)  # Columna expansible
        
        # Frame contenedor para los textos de bienvenida
        frame_bienvenida = Frame(self.frame_center)
        frame_bienvenida.grid(row=0, column=0, pady=(50, 30))
        
        # Texto de bienvenida centrado
        lbl_bienvenida = Label(
            frame_bienvenida, 
            text="¡Bienvenido!",
            font=("Montserrat", 25, "bold"),
            fg="#2c3e50"
        )
        lbl_bienvenida.grid(row=0, column=0, pady=(0, 10))
        
        lbl_descripcion = Label(
            frame_bienvenida,
            text="Selecciona una opción del menú lateral para comenzar",
            font=("Calibri", 14),
            fg="#7f8c8d"
        )
        lbl_descripcion.grid(row=1, column=0, pady=(0, 0))
        
        # Frame para los logos (centrado en la parte inferior)
        frame_logos = Frame(self.frame_center)
        frame_logos.grid(row=1, column=0, sticky="s", pady=(0, 30))
        
        # Cargar y mostrar las imágenes redimensionadas
        try:
            imagen_a = Image.open("./imagenes/logo_sgsycl.png")
            # Redimensionar imagen a tamaño pequeño (ajusta según necesites)
            imagen_a = imagen_a.resize((216, 95), Image.Resampling.LANCZOS)
            self.logo1 = ImageTk.PhotoImage(imagen_a)
            lbl_logo1 = Label(frame_logos, image=self.logo1)
            lbl_logo1.grid(row=0, column=0, padx=15)
        except Exception as e:
            print(f"Error cargando logo_sgsycl.png: {e}")
            lbl_logo1 = Label(frame_logos, text="Logo 1", width=10, height=4, relief="solid")
            lbl_logo1.grid(row=0, column=0, padx=15)

        try:
            imagen_b = Image.open("./imagenes/logo_bdfs.png")
            # Redimensionar imagen a tamaño pequeño (ajusta según necesites)
            imagen_b = imagen_b.resize((216, 95), Image.Resampling.LANCZOS)
            self.logo2 = ImageTk.PhotoImage(imagen_b)
            lbl_logo2 = Label(frame_logos, image=self.logo2)
            lbl_logo2.grid(row=0, column=1, padx=15)
        except Exception as e:
            print(f"Error cargando logo_bdfs.png: {e}")
            lbl_logo2 = Label(frame_logos, text="Logo 2", width=10, height=4, relief="solid")
            lbl_logo2.grid(row=0, column=1, padx=15)

    def ventana_mi_perfil(self):
        self.borrar_frames()
        self.frame_mi_perfil=Frame(master=self.frame_center)
        self.frame_mi_perfil.grid(row=0,column=1,columnspan=2,sticky=NSEW)
        
        lblframe_titulo_mi_perfil=tb.LabelFrame(master=self.frame_mi_perfil)
        lblframe_titulo_mi_perfil.grid(row=0,column=0,padx=10,pady=0,sticky=NSEW)    

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de cerrar sesión?")
        if respuesta:
            self.destroy()  # destruye la ventana principal
            nueva_raiz = Ventana()   # crea una nueva ventana desde cero
            nueva_raiz.mainloop()
           
#Lista de socios
    def ventana_lista_socios(self):     
        self.borrar_frames()
        self.frame_lista_socios=Frame(master=self.frame_center)
        self.frame_lista_socios.grid(row=0,column=1,columnspan=2,sticky=NSEW)
        
        lblframe_botones_lista_socios=tb.LabelFrame(master=self.frame_lista_socios)
        lblframe_botones_lista_socios.grid(row=0,column=0,padx=10,pady=0,sticky=NSEW)
        
        btn_nuevo_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Nuevo',width=15,bootstyle='success',command=self.ventana_nuevo_socio)
        btn_nuevo_lista_socios.grid(row=0,column=0,padx=10,pady=10)
        
        btn_modificar_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_socio)
        btn_modificar_lista_socios.grid(row=0,column=1,padx=10,pady=10)
        
        btn_eliminar_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Eliminar',width=15,bootstyle='danger',command=self.eliminar_socio)
        btn_eliminar_lista_socios.grid(row=0,column=2,padx=10,pady=10)
        
        lblframe_busqueda_socios=tb.LabelFrame(master=self.frame_lista_socios)
        lblframe_busqueda_socios.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)
        
        self.ent_buscar_socios=tb.Entry(master=lblframe_busqueda_socios,width=149)
        self.ent_buscar_socios.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_socios.bind("<KeyRelease>", self.buscar_socios)
        
        lblframe_tree_lista_socios=LabelFrame(master=self.frame_lista_socios)
        lblframe_tree_lista_socios.grid(row=2,column=0,padx=10,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("id_socio","dni","apellidos","nombres","telefono","direccion","estado","prestamos_activos")
        
        #Crear el treeeview
        self.tree_lista_socios=tb.Treeview(master=lblframe_tree_lista_socios,height=22,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_socios.grid(row=0,column=0,padx=10,pady=10)
        
        #Crear las cabeceras
        self.tree_lista_socios.heading('id_socio',text='ID',anchor=W)
        self.tree_lista_socios.heading('dni',text='D.N.I',anchor=W)
        self.tree_lista_socios.heading('apellidos',text='Apellidos',anchor=W)
        self.tree_lista_socios.heading('nombres',text='Nombres',anchor=W)
        self.tree_lista_socios.heading('telefono',text='Teléfono',anchor=W)
        self.tree_lista_socios.heading('direccion',text='Dirección',anchor=W)
        self.tree_lista_socios.heading('estado',text='Estado',anchor=W)
        self.tree_lista_socios.heading('prestamos_activos',text='Préstamos',anchor=W)
        
        #Tamaño de las columnas
        self.tree_lista_socios.column('id_socio',width=80)
        self.tree_lista_socios.column('dni',width=100)
        self.tree_lista_socios.column('apellidos',width=250)
        self.tree_lista_socios.column('nombres',width=250)
        self.tree_lista_socios.column('telefono',width=100)
        self.tree_lista_socios.column('direccion',width=200)
        self.tree_lista_socios.column('estado',width=120)
        self.tree_lista_socios.column('prestamos_activos',width=100)
        
        #Crear el Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_socios,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=10)
        
        #Configurar el Scrollbar
        tree_scroll.config(command=self.tree_lista_socios.yview)
        self.buscar_socios('')
        self.ent_buscar_socios.focus()
           
#Mostrar socios
    def buscar_socios(self, event=None):
        if not hasattr(self, "ent_buscar_socios"):
            return  # Evita errores si todavía no existe el Entry

        texto = self.ent_buscar_socios.get().strip().lower()

        # Limpiamos la tabla
        for row in self.tree_lista_socios.get_children():
            self.tree_lista_socios.delete(row)

        conn = sqlite3.connect("biblioteca.db")
        cur = conn.cursor()
        cur.execute("SELECT Id_socio,dni,apellidos,nombres,telefono,direccion,estado,prestamos_activos FROM Socios WHERE apellidos LIKE ? OR nombres LIKE ?",
                    (f"%{texto}%", f"%{texto}%"))
        for row in cur.fetchall():
            self.tree_lista_socios.insert("", END, values=row)
        conn.close()

    def correlativo_socios(self):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()      
            #Creamos la consulta
            mi_cursor.execute("SELECT MAX(Id_socio) FROM Socios")
            correlativo_socios=mi_cursor.fetchone()
            for datos in correlativo_socios:
                if datos==None:
                    self.nuevo_correlativo_socio=(int(1))
                    self.ent_id_nuevo_socio.config(state=NORMAL)
                    self.ent_id_nuevo_socio.insert(0,self.nuevo_correlativo_socio)
                    self.ent_id_nuevo_socio.config(state='readonly')
                else:
                    self.nuevo_correlativo_socio=(int(datos)+1)
                    self.ent_id_nuevo_socio.config(state=NORMAL)
                    self.ent_id_nuevo_socio.insert(0,self.nuevo_correlativo_socio)
                    self.ent_id_nuevo_socio.config(state='readonly')
            
            #Aplicar cambios
            mi_conexion.commit()
        except:
            messagebox.showerror('Correlativo Libros','Ocurrió un error')

#Ventana de nuevo socio
    def ventana_nuevo_socio(self):
        self.frame_nuevo_socio=Toplevel(master=self)
        self.frame_nuevo_socio.title('Nuevo socio')
        self.centrar_ventana_nuevo_socio(600,550)
        self.frame_nuevo_socio.grab_set()
        
        lblframen_nuevo_socio=tb.LabelFrame(master=self.frame_nuevo_socio,text='Nuevo Socio')
        lblframen_nuevo_socio.pack(padx=15,pady=15)
        
        lbl_id_nuevo_socio=Label(master=lblframen_nuevo_socio,text='ID')
        lbl_id_nuevo_socio.grid(row=0,column=0,padx=10,pady=10)
        self.ent_id_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_id_nuevo_socio.grid(row=0,column=1,padx=10,pady=10)
        
        lbl_dni_nuevo_socio=Label(master=lblframen_nuevo_socio,text='D.N.I')
        lbl_dni_nuevo_socio.grid(row=1,column=0,padx=10,pady=10)
        self.ent_dni_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_dni_nuevo_socio.grid(row=1,column=1,padx=10,pady=10)
        
        lbl_apellidos_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Apellidos')
        lbl_apellidos_nuevo_socio.grid(row=2,column=0,padx=10,pady=10)
        self.ent_apellidos_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_apellidos_nuevo_socio.grid(row=2,column=1,padx=10,pady=10)
        
        lbl_nombres_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Nombres')
        lbl_nombres_nuevo_socio.grid(row=3,column=0,padx=10,pady=10)
        self.ent_nombres_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_nombres_nuevo_socio.grid(row=3,column=1,padx=10,pady=10)
        
        lbl_telefono_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Teléfono')
        lbl_telefono_nuevo_socio.grid(row=4,column=0,padx=10,pady=10)
        self.ent_telefono_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_telefono_nuevo_socio.grid(row=4,column=1,padx=10,pady=10)
        
        lbl_direccion_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Dirección')
        lbl_direccion_nuevo_socio.grid(row=5,column=0,padx=10,pady=10)
        self.ent_direccion_nuevo_socio=tb.Entry(master=lblframen_nuevo_socio,width=50)
        self.ent_direccion_nuevo_socio.grid(row=5,column=1,padx=10,pady=10)
        
        lbl_estado_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Estado')
        lbl_estado_nuevo_socio.grid(row=6,column=0,padx=10,pady=10)
        self.cbo_estado_nuevo_socio=ttk.Combobox(master=lblframen_nuevo_socio,width=50,values=['Activo','Inactivo'])
        self.cbo_estado_nuevo_socio.grid(row=6,column=1,padx=10,pady=10)
        self.cbo_estado_nuevo_socio.current(0)
        self.cbo_estado_nuevo_socio.config(state='readonly')
        
        lbl_prestamos_nuevo_socio=Label(master=lblframen_nuevo_socio,text='Préstamos')
        lbl_prestamos_nuevo_socio.grid(row=7,column=0,padx=10,pady=10)
        self.cbo_prestamos_nuevo_socio=ttk.Combobox(master=lblframen_nuevo_socio,width=50,values=['0','1'])
        self.cbo_prestamos_nuevo_socio.grid(row=7,column=1,padx=10,pady=10)
        self.cbo_prestamos_nuevo_socio.current(0)
        self.cbo_prestamos_nuevo_socio.config(state='readonly')
        
        btn_guardar_socio=tb.Button(master=lblframen_nuevo_socio,text='Guardar',width=49,bootstyle='success',command=self.guardar_socio)
        btn_guardar_socio.grid(row=8,column=1,padx=10,pady=10)
        self.correlativo_socios()
        self.ent_dni_nuevo_socio.focus()

#Ventana de guardar socio
    def guardar_socio(self):
        if(self.ent_id_nuevo_socio.get()==''or self.ent_dni_nuevo_socio.get()==''or self.ent_apellidos_nuevo_socio.get()==''or self.ent_nombres_nuevo_socio.get()==''or self.ent_telefono_nuevo_socio.get()==''or self.ent_direccion_nuevo_socio.get()==''or self.cbo_estado_nuevo_socio.get()==''or self.cbo_prestamos_nuevo_socio.get()==''):
            messagebox.showerror('Guardando Socios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            guardar_datos_socios=(self.ent_id_nuevo_socio.get(),self.ent_dni_nuevo_socio.get(),self.ent_apellidos_nuevo_socio.get(),self.ent_nombres_nuevo_socio.get(),self.ent_telefono_nuevo_socio.get(),self.ent_direccion_nuevo_socio.get(),self.cbo_estado_nuevo_socio.get(),self.cbo_prestamos_nuevo_socio.get())
        
            #Creamos la consulta
            mi_cursor.execute("INSERT INTO Socios VALUES(?,?,?,?,?,?,?,?)",(guardar_datos_socios))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Guardando Socios','Registro guardado correctamente')
            self.frame_nuevo_socio.destroy()
            self.buscar_socios('')
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Guardando Socios','Ocurrió un error')

#Ventana de modificar socio
    def ventana_modificar_socio(self):
        
        self.socio_seleccionado=self.tree_lista_socios.focus()
        self.valor_socio_seleccionado=self.tree_lista_socios.item(self.socio_seleccionado,'values')
        
        if self.valor_socio_seleccionado!='':
        
            self.frame_modificar_socio=Toplevel(master=self)
            self.frame_modificar_socio.title('Modificar Socios')
            self.centrar_ventana_modificar_socio(600,550)
            self.frame_modificar_socio.grab_set()
            
            lblframen_modificar_socio=tb.LabelFrame(master=self.frame_modificar_socio,text='Modificar Socios')
            lblframen_modificar_socio.pack(padx=15,pady=15)
            
            lbl_id_modificar_socio=Label(master=lblframen_modificar_socio,text='ID')
            lbl_id_modificar_socio.grid(row=0,column=0,padx=10,pady=10)
            self.ent_id_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_id_modificar_socio.grid(row=0,column=1,padx=10,pady=10)
            
            lbl_dni_modificar_socio=Label(master=lblframen_modificar_socio,text='D.N.I')
            lbl_dni_modificar_socio.grid(row=1,column=0,padx=10,pady=10)
            self.ent_dni_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_dni_modificar_socio.grid(row=1,column=1,padx=10,pady=10)
            
            lbl_apellidos_modificar_socio=Label(master=lblframen_modificar_socio,text='Apellidos')
            lbl_apellidos_modificar_socio.grid(row=2,column=0,padx=10,pady=10)
            self.ent_apellidos_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_apellidos_modificar_socio.grid(row=2,column=1,padx=10,pady=10)
            
            lbl_nombres_modificar_socio=Label(master=lblframen_modificar_socio,text='Nombres')
            lbl_nombres_modificar_socio.grid(row=3,column=0,padx=10,pady=10)
            self.ent_nombres_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_nombres_modificar_socio.grid(row=3,column=1,padx=10,pady=10)
            
            lbl_telefono_modificar_socio=Label(master=lblframen_modificar_socio,text='Teléfono')
            lbl_telefono_modificar_socio.grid(row=4,column=0,padx=10,pady=10)
            self.ent_telefono_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_telefono_modificar_socio.grid(row=4,column=1,padx=10,pady=10)
            
            lbl_direccion_modificar_socio=Label(master=lblframen_modificar_socio,text='Dirección')
            lbl_direccion_modificar_socio.grid(row=5,column=0,padx=10,pady=10)
            self.ent_direccion_modificar_socio=tb.Entry(master=lblframen_modificar_socio,width=50)
            self.ent_direccion_modificar_socio.grid(row=5,column=1,padx=10,pady=10)
            
            lbl_estado_modificar_socio=Label(master=lblframen_modificar_socio,text='Estado')
            lbl_estado_modificar_socio.grid(row=6,column=0,padx=10,pady=10)
            self.cbo_estado_modificar_socio=ttk.Combobox(master=lblframen_modificar_socio,width=50,values=['Activo','Inactivo'])
            self.cbo_estado_modificar_socio.grid(row=6,column=1,padx=10,pady=10)
            self.cbo_estado_modificar_socio.config(state='readonly')
            
            lbl_prestamos_modificar_socio=Label(master=lblframen_modificar_socio,text='Préstamos')
            lbl_prestamos_modificar_socio.grid(row=7,column=0,padx=10,pady=10)
            self.cbo_prestamos_modificar_socio=ttk.Combobox(master=lblframen_modificar_socio,width=50,values=['0','1'])
            self.cbo_prestamos_modificar_socio.grid(row=7,column=1,padx=10,pady=10)
            self.cbo_prestamos_modificar_socio.config(state='readonly')
            
            btn_modificar_socio=tb.Button(master=lblframen_modificar_socio,text='Modificar',width=49,bootstyle='warning',command=self.modificar_socio)
            btn_modificar_socio.grid(row=8,column=1,padx=10,pady=10)
            self.llenar_entrys_modificar_socio()
            self.ent_dni_modificar_socio.focus()

#Modificar entrys
    def llenar_entrys_modificar_socio(self):
        self.ent_id_modificar_socio.delete(0,END)
        self.ent_dni_modificar_socio.delete(0,END)
        self.ent_apellidos_modificar_socio.delete(0,END)
        self.ent_nombres_modificar_socio.delete(0,END)
        self.ent_telefono_modificar_socio.delete(0,END)
        self.ent_direccion_modificar_socio.delete(0,END)
        self.cbo_estado_modificar_socio.delete(0,END)
        self.cbo_prestamos_modificar_socio.delete(0,END)
        
        self.ent_id_modificar_socio.config(state=NORMAL)
        self.ent_id_modificar_socio.insert(0,self.valor_socio_seleccionado[0])
        self.ent_id_modificar_socio.config(state='readonly')
        self.ent_dni_modificar_socio.insert(0,self.valor_socio_seleccionado[1])
        self.ent_apellidos_modificar_socio.insert(0,self.valor_socio_seleccionado[2])
        self.ent_nombres_modificar_socio.insert(0,self.valor_socio_seleccionado[3])
        self.ent_telefono_modificar_socio.insert(0,self.valor_socio_seleccionado[4])
        self.ent_direccion_modificar_socio.insert(0,self.valor_socio_seleccionado[5])
        self.cbo_estado_modificar_socio.insert(0,self.valor_socio_seleccionado[6])
        self.cbo_prestamos_modificar_socio.insert(0,self.valor_socio_seleccionado[7])

#Modificar socio
    def modificar_socio(self):
        if(self.ent_id_modificar_socio.get()==''or self.ent_dni_modificar_socio.get()==''or self.ent_apellidos_modificar_socio.get()==''or self.ent_nombres_modificar_socio.get()==''or self.ent_telefono_modificar_socio.get()==''or self.ent_direccion_modificar_socio.get()==''or self.cbo_estado_modificar_socio.get()==''or self.cbo_prestamos_modificar_socio.get()==''):
            messagebox.showerror('Modificando Socios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            modificar_datos_socios=(self.ent_dni_modificar_socio.get(),self.ent_apellidos_modificar_socio.get(),self.ent_nombres_modificar_socio.get(),self.ent_telefono_modificar_socio.get(),self.ent_direccion_modificar_socio.get(),self.cbo_estado_modificar_socio.get(),self.cbo_prestamos_modificar_socio.get())
        
            #Creamos la consulta
            mi_cursor.execute("UPDATE Socios SET dni=?,apellidos=?,nombres=?,telefono=?,direccion=?,estado=?,prestamos_activos=? WHERE dni="+self.ent_dni_modificar_socio.get(),(modificar_datos_socios))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Modificando Socios','Registro modificado correctamente')
                        
            self.valor_socio_seleccionado=self.tree_lista_socios.item(self.socio_seleccionado,text='',values=(self.ent_id_modificar_socio.get(),self.ent_dni_modificar_socio.get(),self.ent_apellidos_modificar_socio.get(),self.ent_nombres_modificar_socio.get(),self.ent_telefono_modificar_socio.get(),self.ent_direccion_modificar_socio.get(),self.cbo_estado_modificar_socio.get(),self.cbo_prestamos_modificar_socio.get()))
            self.frame_modificar_socio.destroy()
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando Socios','Ocurrió un error')

#Eliminar socio
    def eliminar_socio(self):
        socio_seleccionado_eliminar=self.tree_lista_socios.focus()
        valor_socio_seleccionado_eliminar=self.tree_lista_socios.item(socio_seleccionado_eliminar,'values')
        
        try:
            if valor_socio_seleccionado_eliminar!='':
                respuesta=messagebox.askquestion('Eliminando Socio','¿Está seguro de eliminar el socio seleccionado?')
                if respuesta=='yes':
                    #Conexion a la BD
                    mi_conexion=sqlite3.connect('biblioteca.db')
                    #Crear el cursor
                    mi_cursor=mi_conexion.cursor()
                        #Creamos la consulta
                    mi_cursor.execute("DELETE FROM Socios WHERE Id_socio="+ str(valor_socio_seleccionado_eliminar[0]))
                    #Aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Socio','Registro eliminado correctamente')
                    self.buscar_socios('')
                    #Cerrar la conexión
                    mi_conexion.close()
                else:
                    messagebox.showerror('Eliminando Socio','Eliminación cancelada')
        except:
            messagebox.showerror('Eliminando Socio','Ocurrió un error')

#Centrar ventanas
    def centrar_ventana_nuevo_socio(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_nuevo_socio.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def centrar_ventana_modificar_socio(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_modificar_socio.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

#===============================LIBROS=========================================
    def ventana_lista_libros(self):
        self.borrar_frames()
        self.frame_lista_libros=Frame(master=self.frame_center)
        self.frame_lista_libros.grid(row=0,column=1,columnspan=2,sticky=NSEW)
        
        lblframe_botones_lista_libros=tb.LabelFrame(master=self.frame_lista_libros)
        lblframe_botones_lista_libros.grid(row=0,column=0,padx=10,pady=0,sticky=NSEW)
        
        btn_nuevo_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Nuevo',width=15,bootstyle='success',command=self.ventana_nuevo_libro)
        btn_nuevo_lista_libros.grid(row=0,column=0,padx=10,pady=10)
        
        btn_modificar_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_libro)
        btn_modificar_lista_libros.grid(row=0,column=1,padx=10,pady=10)
        
        btn_eliminar_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Eliminar',width=15,bootstyle='danger',command=self.eliminar_libro)
        btn_eliminar_lista_libros.grid(row=0,column=2,padx=10,pady=10)
        
        lblframe_busqueda_lista_libros=tb.LabelFrame(master=self.frame_lista_libros)
        lblframe_busqueda_lista_libros.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)
        
        self.ent_buscar_libro=tb.Entry(master=lblframe_busqueda_lista_libros,width=149,)
        self.ent_buscar_libro.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_libro.bind('<Key>',self.buscar_libros_lista)
        
        lblframe_tree_lista_libros=LabelFrame(master=self.frame_lista_libros)
        lblframe_tree_lista_libros.grid(row=2,column=0,padx=10,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("id_libro","titulo","autor","isbn","editorial","año","cantidad","categoria")
        
        #Crear el treeeview
        self.tree_lista_libros=tb.Treeview(master=lblframe_tree_lista_libros,height=22,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_libros.grid(row=0,column=0,padx=10,pady=10)
        
        #Crear las cabeceras
        self.tree_lista_libros.heading('id_libro',text='ID',anchor=W)
        self.tree_lista_libros.heading('titulo',text='Título',anchor=W)
        self.tree_lista_libros.heading('autor',text='Autor',anchor=W)
        self.tree_lista_libros.heading('isbn',text='ISBN',anchor=W)
        self.tree_lista_libros.heading('editorial',text='Editorial',anchor=W)
        self.tree_lista_libros.heading('año',text='Año',anchor=W)
        self.tree_lista_libros.heading('cantidad',text='Cantidad',anchor=W)
        self.tree_lista_libros.heading('categoria',text='Categoría',anchor=W)
        
        #Tamaño de las columnas
        self.tree_lista_libros.column('id_libro',width=80)
        self.tree_lista_libros.column('titulo',width=250)
        self.tree_lista_libros.column('autor',width=250)
        self.tree_lista_libros.column('isbn',width=160)
        self.tree_lista_libros.column('editorial',width=200)
        self.tree_lista_libros.column('año',width=80)
        self.tree_lista_libros.column('cantidad',width=80)
        self.tree_lista_libros.column('categoria',width=100)
        
        #Crear el Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_libros,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=10)
        
        #Configurar el Scrollbar
        tree_scroll.config(command=self.tree_lista_libros.yview)
        self.buscar_libros_lista('')
        self.ent_buscar_libro.focus()

    def ventana_nuevo_libro(self):
        self.frame_nuevo_libro=Toplevel(master=self)
        self.frame_nuevo_libro.title('Nuevo libro')
        self.centrar_ventana_nuevo_libro(600,550)
        self.frame_nuevo_libro.grab_set()
        
        lblframen_nuevo_libro=tb.LabelFrame(master=self.frame_nuevo_libro,text='Nuevo Libro')
        lblframen_nuevo_libro.pack(padx=15,pady=15)
        
        lbl_id_nuevo_libro=Label(master=lblframen_nuevo_libro,text='ID')
        lbl_id_nuevo_libro.grid(row=0,column=0,padx=10,pady=10)
        self.ent_id_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_id_nuevo_libro.grid(row=0,column=1,padx=10,pady=10)
        
        lbl_titulo_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Título')
        lbl_titulo_nuevo_libro.grid(row=1,column=0,padx=10,pady=10)
        self.ent_titulo_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_titulo_nuevo_libro.grid(row=1,column=1,padx=10,pady=10)
        
        lbl_autor_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Autor')
        lbl_autor_nuevo_libro.grid(row=2,column=0,padx=10,pady=10)
        self.ent_autor_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_autor_nuevo_libro.grid(row=2,column=1,padx=10,pady=10)
        
        lbl_isbn_nuevo_libro=Label(master=lblframen_nuevo_libro,text='ISBN')
        lbl_isbn_nuevo_libro.grid(row=3,column=0,padx=10,pady=10)
        self.ent_isbn_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_isbn_nuevo_libro.grid(row=3,column=1,padx=10,pady=10)
        
        lbl_editorial_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Editorial')
        lbl_editorial_nuevo_libro.grid(row=4,column=0,padx=10,pady=10)
        self.ent_editorial_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_editorial_nuevo_libro.grid(row=4,column=1,padx=10,pady=10)
        
        lbl_año_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Año')
        lbl_año_nuevo_libro.grid(row=5,column=0,padx=10,pady=10)
        self.ent_año_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_año_nuevo_libro.grid(row=5,column=1,padx=10,pady=10)
        
        lbl_cantidad_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Cantidad')
        lbl_cantidad_nuevo_libro.grid(row=6,column=0,padx=10,pady=10)
        self.ent_cantidad_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_cantidad_nuevo_libro.grid(row=6,column=1,padx=10,pady=10)
        
        lbl_categoria_nuevo_libro=Label(master=lblframen_nuevo_libro,text='Categoría')
        lbl_categoria_nuevo_libro.grid(row=7,column=0,padx=10,pady=10)
        self.ent_categoria_nuevo_libro=tb.Entry(master=lblframen_nuevo_libro,width=50)
        self.ent_categoria_nuevo_libro.grid(row=7,column=1,padx=10,pady=10)
        
        btn_guardar_libro=tb.Button(master=lblframen_nuevo_libro,text='Guardar',width=49,bootstyle='success',command=self.guardar_libro)
        btn_guardar_libro.grid(row=8,column=1,padx=10,pady=10)
        self.correlativo_libros()
        self.ent_titulo_nuevo_libro.focus()
        
    def centrar_ventana_nuevo_libro(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_nuevo_libro.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def guardar_libro(self):
        if(self.ent_id_nuevo_libro.get()==''or self.ent_titulo_nuevo_libro.get()==''or self.ent_autor_nuevo_libro.get()==''or self.ent_isbn_nuevo_libro.get()==''or self.ent_editorial_nuevo_libro.get()==''or self.ent_año_nuevo_libro.get()==''or self.ent_cantidad_nuevo_libro.get()==''or self.ent_categoria_nuevo_libro.get()==''):
            messagebox.showerror('Guardando Libros','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            guardar_datos_libros=(self.ent_id_nuevo_libro.get(),self.ent_titulo_nuevo_libro.get(),self.ent_autor_nuevo_libro.get(),self.ent_isbn_nuevo_libro.get(),self.ent_editorial_nuevo_libro.get(),self.ent_año_nuevo_libro.get(),self.ent_cantidad_nuevo_libro.get(),self.ent_categoria_nuevo_libro.get())
        
            #Creamos la consulta
            mi_cursor.execute("INSERT INTO Libros VALUES(?,?,?,?,?,?,?,?)",(guardar_datos_libros))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Guardando Libros','Registro guardado correctamente')
            self.frame_nuevo_libro.destroy()
            self.buscar_libros_lista('')
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Guardando Libros','Ocurrió un error')                

    def buscar_libros_lista(self, event=None):
        texto = self.ent_buscar_libro.get().strip().lower()
        for row in self.tree_lista_libros.get_children():
            self.tree_lista_libros.delete(row)

        conn = sqlite3.connect("biblioteca.db")
        cur = conn.cursor()
        cur.execute("SELECT Id_libro,titulo,autor,isbn,editorial,año,cantidad,categoria FROM Libros WHERE titulo LIKE ? OR autor LIKE ?",
                    (f"%{texto}%", f"%{texto}%"))
        for row in cur.fetchall():
            self.tree_lista_libros.insert("", END, values=row)
        conn.close()

    def correlativo_libros(self):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()      
            #Creamos la consulta
            mi_cursor.execute("SELECT MAX(Id_libro) FROM Libros")
            correlativo_libros=mi_cursor.fetchone()
            for datos in correlativo_libros:
                if datos==None:
                    self.nuevo_correlativo_libro=(int(1))
                    self.ent_id_nuevo_libro.config(state=NORMAL)
                    self.ent_id_nuevo_libro.insert(0,self.nuevo_correlativo_libro)
                    self.ent_id_nuevo_libro.config(state='readonly')
                else:
                    self.nuevo_correlativo_libro=(int(datos)+1)
                    self.ent_id_nuevo_libro.config(state=NORMAL)
                    self.ent_id_nuevo_libro.insert(0,self.nuevo_correlativo_libro)
                    self.ent_id_nuevo_libro.config(state='readonly')
            
            #Aplicar cambios
            mi_conexion.commit()
        except:
            messagebox.showerror('Correlativo Libros','Ocurrió un error')

    def ventana_modificar_libro(self):
        self.libro_seleccionado=self.tree_lista_libros.focus()
        self.valor_libro_seleccionado=self.tree_lista_libros.item(self.libro_seleccionado,'values')
        
        if self.valor_libro_seleccionado!='':
            
            self.frame_modificar_libro=Toplevel(master=self)
            self.frame_modificar_libro.title('Modificar libro')
            self.centrar_ventana_modificar_libro(600,550)
            self.frame_modificar_libro.grab_set()
            
            lblframen_modificar_libro=tb.LabelFrame(master=self.frame_modificar_libro,text='Modificar Libro')
            lblframen_modificar_libro.pack(padx=15,pady=15)
            
            lbl_id_modificar_libro=Label(master=lblframen_modificar_libro,text='ID')
            lbl_id_modificar_libro.grid(row=0,column=0,padx=10,pady=10)
            self.ent_id_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_id_modificar_libro.grid(row=0,column=1,padx=10,pady=10)
            
            lbl_titulo_modificar_libro=Label(master=lblframen_modificar_libro,text='Título')
            lbl_titulo_modificar_libro.grid(row=1,column=0,padx=10,pady=10)
            self.ent_titulo_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_titulo_modificar_libro.grid(row=1,column=1,padx=10,pady=10)
            
            lbl_autor_modificar_libro=Label(master=lblframen_modificar_libro,text='Autor')
            lbl_autor_modificar_libro.grid(row=2,column=0,padx=10,pady=10)
            self.ent_autor_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_autor_modificar_libro.grid(row=2,column=1,padx=10,pady=10)
            
            lbl_isbn_modificar_libro=Label(master=lblframen_modificar_libro,text='ISBN')
            lbl_isbn_modificar_libro.grid(row=3,column=0,padx=10,pady=10)
            self.ent_isbn_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_isbn_modificar_libro.grid(row=3,column=1,padx=10,pady=10)
            
            lbl_editorial_modificar_libro=Label(master=lblframen_modificar_libro,text='Editorial')
            lbl_editorial_modificar_libro.grid(row=4,column=0,padx=10,pady=10)
            self.ent_editorial_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_editorial_modificar_libro.grid(row=4,column=1,padx=10,pady=10)
            
            lbl_año_modificar_libro=Label(master=lblframen_modificar_libro,text='Año')
            lbl_año_modificar_libro.grid(row=5,column=0,padx=10,pady=10)
            self.ent_año_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_año_modificar_libro.grid(row=5,column=1,padx=10,pady=10)
            
            lbl_cantidad_modificar_libro=Label(master=lblframen_modificar_libro,text='Cantidad')
            lbl_cantidad_modificar_libro.grid(row=6,column=0,padx=10,pady=10)
            self.ent_cantidad_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_cantidad_modificar_libro.grid(row=6,column=1,padx=10,pady=10)
            
            lbl_categoria_modificar_libro=Label(master=lblframen_modificar_libro,text='Categoría')
            lbl_categoria_modificar_libro.grid(row=7,column=0,padx=10,pady=10)
            self.ent_categoria_modificar_libro=tb.Entry(master=lblframen_modificar_libro,width=50)
            self.ent_categoria_modificar_libro.grid(row=7,column=1,padx=10,pady=10)
            
            btn_modificar_libro=tb.Button(master=lblframen_modificar_libro,text='Modificar',width=49,bootstyle='warning',command=self.modificar_libro)
            btn_modificar_libro.grid(row=8,column=1,padx=10,pady=10)
            self.llenar_entrys_modificar_libro()
            self.ent_titulo_modificar_libro.focus()

    def centrar_ventana_modificar_libro(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_modificar_libro.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def llenar_entrys_modificar_libro(self):
        self.ent_id_modificar_libro.delete(0,END)
        self.ent_titulo_modificar_libro.delete(0,END)
        self.ent_autor_modificar_libro.delete(0,END)
        self.ent_isbn_modificar_libro.delete(0,END)
        self.ent_editorial_modificar_libro.delete(0,END)
        self.ent_año_modificar_libro.delete(0,END)
        self.ent_cantidad_modificar_libro.delete(0,END)
        self.ent_categoria_modificar_libro.delete(0,END)
        
        self.ent_id_modificar_libro.config(state=NORMAL)
        self.ent_id_modificar_libro.insert(0,self.valor_libro_seleccionado[0])
        self.ent_id_modificar_libro.config(state='readonly')
        self.ent_titulo_modificar_libro.insert(0,self.valor_libro_seleccionado[1])
        self.ent_autor_modificar_libro.insert(0,self.valor_libro_seleccionado[2])
        self.ent_isbn_modificar_libro.insert(0,self.valor_libro_seleccionado[3])
        self.ent_editorial_modificar_libro.insert(0,self.valor_libro_seleccionado[4])
        self.ent_año_modificar_libro.insert(0,self.valor_libro_seleccionado[5])
        self.ent_cantidad_modificar_libro.insert(0,self.valor_libro_seleccionado[6])
        self.ent_categoria_modificar_libro.insert(0,self.valor_libro_seleccionado[7])

    def modificar_libro(self):
        if(self.ent_id_modificar_libro.get()==''or self.ent_titulo_modificar_libro.get()==''or self.ent_autor_modificar_libro.get()==''or self.ent_isbn_modificar_libro.get()==''or self.ent_editorial_modificar_libro.get()==''or self.ent_año_modificar_libro.get()==''or self.ent_cantidad_modificar_libro.get()==''or self.ent_categoria_modificar_libro.get()==''):
            messagebox.showerror('Modificando Libros','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            modificar_datos_libros=(self.ent_titulo_modificar_libro.get(),self.ent_autor_modificar_libro.get(),self.ent_isbn_modificar_libro.get(),self.ent_editorial_modificar_libro.get(),self.ent_año_modificar_libro.get(),self.ent_cantidad_modificar_libro.get(),self.ent_categoria_modificar_libro.get())
        
            #Creamos la consulta
            mi_cursor.execute("UPDATE Libros SET titulo=?,autor=?,isbn=?,editorial=?,año=?,cantidad=?,categoria=? WHERE Id_libro="+self.ent_id_modificar_libro.get(),(modificar_datos_libros))
            
            #Aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Modificando Libros','Registro modificado correctamente')
                        
            self.valor_libro_seleccionado=self.tree_lista_libros.item(self.libro_seleccionado,text='',values=(self.ent_id_modificar_libro.get(),self.ent_titulo_modificar_libro.get(),self.ent_autor_modificar_libro.get(),self.ent_isbn_modificar_libro.get(),self.ent_editorial_modificar_libro.get(),self.ent_año_modificar_libro.get(),self.ent_cantidad_modificar_libro.get(),self.ent_categoria_modificar_libro.get()))
            self.frame_modificar_libro.destroy()
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando Libros','Ocurrió un error')

    def eliminar_libro(self):
        libro_seleccionado_eliminar=self.tree_lista_libros.focus()
        valor_libro_seleccionado_eliminar=self.tree_lista_libros.item(libro_seleccionado_eliminar,'values')
        
        try:
            if valor_libro_seleccionado_eliminar!='':
                respuesta=messagebox.askquestion('Eliminando Libros','¿Está seguro de eliminar el libro seleccionado?')
                if respuesta=='yes':
                    #Conexion a la BD
                    mi_conexion=sqlite3.connect('biblioteca.db')
                    #Crear el cursor
                    mi_cursor=mi_conexion.cursor()
                        #Creamos la consulta
                    mi_cursor.execute("DELETE FROM Libros WHERE Id_libro="+ str(valor_libro_seleccionado_eliminar[0]))
                    #Aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Libros','Registro eliminado correctamente')
                    self.buscar_libros_lista('')
                    #Cerrar la conexión
                    mi_conexion.close()
                else:
                    messagebox.showerror('Eliminando Libros','Eliminación cancelada')
        except:
            messagebox.showerror('Eliminando Libros','Ocurrió un error')

#==============================FRAMES==========================================
    def borrar_frames(self):
        for frames in self.frame_center.winfo_children():
            frames.destroy()

#==============================PRESTAMOS========================================
    def ventana_lista_prestamos(self): 
        self.borrar_frames()
        self.frame_lista_prestamos=Frame(master=self.frame_center)
        self.frame_lista_prestamos.grid(row=0,column=1,sticky=NSEW)
        
        lblframe_botones_lista_prestamos=tb.LabelFrame(master=self.frame_lista_prestamos)
        lblframe_botones_lista_prestamos.grid(row=0,column=0,padx=10,pady=0,sticky=NSEW)
        
        btn_crear_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Crear Préstamo',width=17,bootstyle='success',command=self.ventana_crear_prestamo)
        btn_crear_prestamos.grid(row=0,column=0,padx=10,pady=10)
        
        btn_modificar_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Modificar Préstamo',width=17,bootstyle='warning',command=self.ventana_modificar_prestamo)
        btn_modificar_prestamos.grid(row=0,column=1,padx=10,pady=10)
        
        btn_devolver_prestamo_seleccionado=tb.Button(master=lblframe_botones_lista_prestamos,text="Devolver Préstamo",bootstyle="info",width=17,command=self.devolver_prestamo_seleccionado)
        btn_devolver_prestamo_seleccionado.grid(row=0, column=2, padx=10, pady=10)
        
        lblframe_busqueda_lista_prestamos=tb.LabelFrame(master=self.frame_lista_prestamos)
        lblframe_busqueda_lista_prestamos.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)
        
        self.ent_buscar_lista_prestamos=tb.Entry(master=lblframe_busqueda_lista_prestamos,width=149)
        self.ent_buscar_lista_prestamos.grid(row=0,column=0,padx=10,pady=10)
        
        lblframe_tree_lista_prestamos=LabelFrame(master=self.frame_lista_prestamos)
        lblframe_tree_lista_prestamos.grid(row=2,column=0,padx=10,pady=5,sticky=NSEW)
        
        # Columnas (agrego 'libros')
        columnas=("id_prestamo","retiro","devolucion","socio","libros","estado")
        
        self.tree_lista_prestamos=tb.Treeview(master=lblframe_tree_lista_prestamos,height=22,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_prestamos.grid(row=0,column=0,padx=10,pady=10)

        # Cabeceras
        self.tree_lista_prestamos.heading('id_prestamo',text='ID',anchor=W)
        self.tree_lista_prestamos.heading('retiro',text='Fecha Retiro',anchor=W)
        self.tree_lista_prestamos.heading('devolucion',text='Fecha Devolución',anchor=W)
        self.tree_lista_prestamos.heading('socio',text='Socio',anchor=W)
        self.tree_lista_prestamos.heading('libros',text='Libros',anchor=W)
        self.tree_lista_prestamos.heading('estado',text='Estado',anchor=W)

        # Tamaños de columnas
        self.tree_lista_prestamos.column('id_prestamo',width=80)
        self.tree_lista_prestamos.column('retiro',width=160)
        self.tree_lista_prestamos.column('devolucion',width=160)
        self.tree_lista_prestamos.column('socio',width=250)
        self.tree_lista_prestamos.column('libros',width=450)
        self.tree_lista_prestamos.column('estado',width=100)

        # Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_prestamos,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=10,sticky="ns")
        self.tree_lista_prestamos.config(yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree_lista_prestamos.yview)

        # Cargar préstamos automáticamente
        self.cargar_prestamos()
        #self.ent_buscar_lista_prestamos()

    def cargar_prestamos(self):
        try:
            # Limpiar treeview antes de cargar
            for row in self.tree_lista_prestamos.get_children():
                self.tree_lista_prestamos.delete(row)

            conexion = sqlite3.connect("biblioteca.db")
            cursor = conexion.cursor()

            # Traer préstamos con datos del socio y los libros asociados
            cursor.execute("""
                SELECT 
                    p.id_prestamo, 
                    p.fecha_retiro, 
                    p.fecha_devolucion, 
                    s.nombres || ' ' || s.apellidos AS socio,
                    GROUP_CONCAT(l.titulo, ', ') AS libros,
                    p.estado
                FROM prestamos p
                INNER JOIN socios s ON p.id_socio = s.id_socio
                INNER JOIN prestamos_libros pl ON p.id_prestamo = pl.id_prestamo
                INNER JOIN libros l ON pl.id_libro = l.id_libro
                GROUP BY p.id_prestamo, p.fecha_retiro, p.fecha_devolucion, socio, p.estado
                ORDER BY p.id_prestamo DESC
            """)

            prestamos = cursor.fetchall()

            for prestamo in prestamos:
                # prestamo = (id, retiro, devolucion, socio, libros, estado)
                self.tree_lista_prestamos.insert(
                    "", "end", values=prestamo
                )

            conexion.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los préstamos: {e}")

    def ventana_crear_prestamo(self):
        self.frame_crear_prestamo = Toplevel(master=self)
        self.frame_crear_prestamo.title('Crear Préstamo')
        self.centrar_ventana_crear_prestamo(600, 540)
        self.frame_crear_prestamo.grab_set()

        lblframen_crear_prestamo = tb.LabelFrame(master=self.frame_crear_prestamo, text='Crear Préstamo')
        lblframen_crear_prestamo.pack(padx=15, pady=15)

        # ID
        lbl_id_crear_prestamo = Label(master=lblframen_crear_prestamo, text='ID')
        lbl_id_crear_prestamo.grid(row=0, column=0, padx=10, pady=10)
        self.ent_id_crear_prestamo = tb.Entry(master=lblframen_crear_prestamo, width=40)
        self.ent_id_crear_prestamo.grid(row=0, column=1, padx=10, pady=10)

        # Fecha de Retiro
        lbl_retiro_crear_prestamo = Label(master=lblframen_crear_prestamo, text='Fecha de Retiro')
        lbl_retiro_crear_prestamo.grid(row=1, column=0, padx=10, pady=10)
        self.ent_retiro_crear_prestamo = tb.Entry(master=lblframen_crear_prestamo, width=40)
        self.ent_retiro_crear_prestamo.grid(row=1, column=1, padx=10, pady=10)

        # Insertar fecha actual automáticamente
        fecha_retiro = datetime.now().date()
        self.ent_retiro_crear_prestamo.insert(0, fecha_retiro.strftime("%Y-%m-%d"))

        # Fecha de Devolución (automática: +10 días)
        lbl_devolucion_crear_prestamo = Label(master=lblframen_crear_prestamo, text='Fecha de Devolución')
        lbl_devolucion_crear_prestamo.grid(row=2, column=0, padx=10, pady=10)
        self.ent_devolucion_crear_prestamo = tb.Entry(master=lblframen_crear_prestamo, width=40)
        self.ent_devolucion_crear_prestamo.grid(row=2, column=1, padx=10, pady=10)

        fecha_devolucion = fecha_retiro + timedelta(days=10)
        self.ent_devolucion_crear_prestamo.insert(0, fecha_devolucion.strftime("%Y-%m-%d"))

        # Socio
        btn_seleccionar_socio = tb.Button(master=lblframen_crear_prestamo, text='Seleccionar Socio',bootstyle='info', command=self.ventana_seleccionar_socio)
        btn_seleccionar_socio.grid(row=3, column=0, padx=10, pady=10)
        self.ent_socio_crear_prestamo = tb.Entry(master=lblframen_crear_prestamo, width=40)
        self.ent_socio_crear_prestamo.grid(row=3, column=1, padx=10, pady=10)

        # Libros
        for i in range(1, 4):
            btn = tb.Button(master=lblframen_crear_prestamo, text=f'Seleccionar Libro {i}',
                            bootstyle='secondary', command=lambda x=i: self.ventana_seleccionar_libro(x))
            btn.grid(row=3 + i, column=0, padx=10, pady=10)
            entry = tb.Entry(master=lblframen_crear_prestamo, width=40)
            entry.grid(row=3 + i, column=1, padx=10, pady=10)
            setattr(self, f"ent_seleccionar_libro{i}_crear_prestamo", entry)

        # Estado del préstamo
        lbl_estado = Label(master=lblframen_crear_prestamo, text="Estado")
        lbl_estado.grid(row=7, column=0, padx=10, pady=10)

        self.var_estado = StringVar(value="Prestado")
        combo_estado = tb.Combobox(master=lblframen_crear_prestamo, textvariable=self.var_estado,
                                values=["Prestado", "Devuelto", "Demorado"], width=37, state="readonly")
        combo_estado.grid(row=7, column=1, padx=10, pady=10)

        # Botón Guardar
        btn_guardar_prestamo = tb.Button(master=lblframen_crear_prestamo, text='Guardar',width=39, bootstyle='success',command=self.guardar_prestamo)
        btn_guardar_prestamo.grid(row=8, column=1, padx=10, pady=10)

        self.correlativo_prestamos()

    def guardar_prestamo(self):
        try:
            print("=== INICIANDO GUARDADO DE PRÉSTAMO ===")
            
            # Verificar que se haya seleccionado un socio
            if not hasattr(self, 'socio_seleccionado_id') or not self.socio_seleccionado_id:
                messagebox.showwarning("Atención", "Debes seleccionar un socio.")
                return

            # Verificar que se hayan seleccionado exactamente 3 libros
            if not hasattr(self, 'libros_seleccionados') or len(self.libros_seleccionados) != 3:
                seleccionados = len(self.libros_seleccionados) if hasattr(self, 'libros_seleccionados') else 0
                messagebox.showwarning("Atención", f"Debes seleccionar exactamente 3 libros. Actualmente tienes {seleccionados} seleccionados.")
                return

            print(f"Socio seleccionado ID: {self.socio_seleccionado_id}")
            print(f"Libros seleccionados: {self.libros_seleccionados}")

            # Datos del préstamo
            id_socio = self.socio_seleccionado_id
            fecha_retiro = datetime.now().strftime("%Y-%m-%d")
            fecha_devolucion = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
            estado = "Prestado"

            # Conectar a la BD
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()

            # Insertar préstamo
            cur.execute(
                "INSERT INTO prestamos (id_socio, fecha_retiro, fecha_devolucion, estado) VALUES (?, ?, ?, ?)",
                (id_socio, fecha_retiro, fecha_devolucion, estado)
            )
            id_prestamo = cur.lastrowid
            print(f"Préstamo insertado con ID: {id_prestamo}")

            # Insertar los 3 libros y descontar la cantidad
            for numero_libro, datos_libro in self.libros_seleccionados.items():
                id_libro = datos_libro['id']
                print(f"Insertando libro {numero_libro}: ID={id_libro}, Título={datos_libro['titulo']}")

                # Insertar en prestamos_libros
                cur.execute(
                    "INSERT INTO prestamos_libros (id_prestamo, id_libro) VALUES (?, ?)",
                    (id_prestamo, id_libro)
                )

                # Descontar 1 de la cantidad de ese libro
                cur.execute(
                    "UPDATE Libros SET cantidad = cantidad - 1 WHERE Id_libro = ? AND cantidad > 0",
                    (id_libro,)
                )

            conn.commit()
            conn.close()
            print("✅ Préstamo guardado y cantidades actualizadas")

            # Limpiar formulario
            self.limpiar_formulario_prestamo()

            messagebox.showinfo("Éxito", "Préstamo guardado correctamente y libros actualizados.")
            self.buscar_prestamos('')

        except Exception as e:
            print(f"❌ Error al guardar préstamo: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo guardar el préstamo: {e}")

    def devolver_prestamo(self, id_prestamo):
        try:
            print(f"=== DEVOLVIENDO PRÉSTAMO ID {id_prestamo} ===")

            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()

            # Verificar que el préstamo existe y está activo
            cur.execute("SELECT estado, id_socio FROM prestamos WHERE id_prestamo = ?", (id_prestamo,))
            row = cur.fetchone()
            if not row:
                messagebox.showwarning("Atención", "El préstamo no existe.")
                conn.close()
                return
            if row[0] == "Devuelto":
                messagebox.showinfo("Información", "El préstamo ya fue devuelto.")
                conn.close()
                return

            estado_actual, id_socio = row
            print(f"Préstamo encontrado - Estado: {estado_actual}, Socio: {id_socio}")

            # Verificar préstamos activos actuales del socio ANTES del cambio
            cur.execute("SELECT prestamos_activos FROM Socios WHERE id_socio = ?", (id_socio,))
            socio_row = cur.fetchone()
            prestamos_antes = socio_row[0] if socio_row else 0
            print(f"Socio {id_socio} ANTES: {prestamos_antes} préstamos activos")

            # Obtener los libros asociados
            cur.execute("SELECT id_libro FROM prestamos_libros WHERE id_prestamo = ?", (id_prestamo,))
            libros = cur.fetchall()

            # Restaurar cantidades de libros
            for (id_libro,) in libros:
                cur.execute("UPDATE Libros SET cantidad = cantidad + 1 WHERE Id_libro = ?", (id_libro,))
                print(f"Libro {id_libro} devuelto (+1 cantidad)")

            # Cambiar estado del préstamo
            cur.execute("UPDATE prestamos SET estado = ? WHERE id_prestamo = ?", ("Devuelto", id_prestamo))
            print(f"Préstamo {id_prestamo} marcado como Devuelto")

            # ACTUALIZAR préstamos activos del socio - SIEMPRE establecer en 0
            cur.execute("UPDATE Socios SET prestamos_activos = 0 WHERE id_socio = ?", (id_socio,))
            print(f"Socio {id_socio}: préstamos activos establecidos en 0")

            # Verificar el cambio DESPUÉS
            cur.execute("SELECT prestamos_activos FROM Socios WHERE id_socio = ?", (id_socio,))
            socio_row_despues = cur.fetchone()
            prestamos_despues = socio_row_despues[0] if socio_row_despues else 0
            print(f"Socio {id_socio} DESPUÉS: {prestamos_despues} préstamos activos")

            conn.commit()
            print("✅ Cambios guardados en base de datos")
            conn.close()

            # Refrescar listas
            print("🔄 Refrescando vistas...")
            self.cargar_prestamos()
            
            # Refrescar la vista principal de socios que muestra prestamos_activos
            if hasattr(self, 'buscar_socios'):
                # Verificar si existe el entry de búsqueda
                if hasattr(self, 'ent_buscar_socios'):
                    # Limpiar búsqueda y mostrar todos los socios
                    self.ent_buscar_socios.delete(0, 'end')
                    self.buscar_socios()
                    print("✅ Vista de socios actualizada con búsqueda vacía")
                else:
                    print("❌ No se encontró ent_buscar_socios")
            else:
                print("❌ No se encontró función buscar_socios")

            # VERIFICACIÓN FINAL: Consultar directamente y mostrar en consola
            print("=== VERIFICACIÓN FINAL EN BASE DE DATOS ===")
            cur_verify = conn = sqlite3.connect("biblioteca.db")
            cur_verify = conn.cursor()
            cur_verify.execute("SELECT Id_socio, apellidos, nombres, prestamos_activos FROM Socios WHERE Id_socio = ?", (id_socio,))
            resultado_final = cur_verify.fetchone()
            if resultado_final:
                print(f"ID: {resultado_final[0]} | Apellidos: {resultado_final[1]} | Nombres: {resultado_final[2]} | Préstamos: {resultado_final[3]}")
            else:
                print("❌ No se encontró el socio en la base de datos")
            conn.close()

            messagebox.showinfo("Éxito", f"Préstamo devuelto correctamente.\nSocio {id_socio} puede realizar nuevos préstamos.")

        except Exception as e:
            print(f"❌ Error al devolver préstamo: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo devolver el préstamo: {e}")

    def devolver_prestamo_seleccionado(self):
        try:
            seleccionado = self.tree_lista_prestamos.selection()
            if not seleccionado:
                messagebox.showwarning("Atención", "Debes seleccionar un préstamo.")
                return

            # Obtener datos del préstamo seleccionado
            item = self.tree_lista_prestamos.item(seleccionado[0])
            id_prestamo = item["values"][0]
            estado = item["values"][5]

            if estado == "Devuelto":
                messagebox.showinfo("Info", "Este préstamo ya fue devuelto.")
                return

            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()

            # Obtener el id_socio antes de cambiar el estado
            cur.execute("SELECT id_socio FROM prestamos WHERE id_prestamo = ?", (id_prestamo,))
            socio_row = cur.fetchone()
            if not socio_row:
                messagebox.showerror("Error", "No se encontró información del socio.")
                conn.close()
                return
            
            id_socio = socio_row[0]

            # Verificar préstamos activos actuales del socio
            cur.execute("SELECT prestamos_activos FROM Socios WHERE id_socio = ?", (id_socio,))
            prestamos_row = cur.fetchone()
            prestamos_actuales = prestamos_row[0] if prestamos_row else 0

            # Cambiar estado a Devuelto
            cur.execute("UPDATE prestamos SET estado='Devuelto' WHERE id_prestamo=?", (id_prestamo,))

            # Recuperar los libros de ese préstamo
            cur.execute("SELECT id_libro FROM prestamos_libros WHERE id_prestamo=?", (id_prestamo,))
            libros = cur.fetchall()

            # Sumar de nuevo la cantidad a cada libro
            for (id_libro,) in libros:
                cur.execute("UPDATE Libros SET cantidad = cantidad + 1 WHERE Id_libro=?", (id_libro,))

            # CORREGIDO: Solo decrementar si hay préstamos activos (evitar negativos)
            if prestamos_actuales > 0:
                cur.execute("UPDATE Socios SET prestamos_activos = prestamos_activos - 1 WHERE id_socio = ?", (id_socio,))
                print(f"Socio {id_socio}: préstamos activos decrementados (-1) = {prestamos_actuales - 1}")
            else:
                # Si ya está en 0 o negativo, establecer en 0
                cur.execute("UPDATE Socios SET prestamos_activos = 0 WHERE id_socio = ?", (id_socio,))
                print(f"Socio {id_socio}: préstamos activos corregidos a 0")

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Préstamo devuelto correctamente. El socio puede realizar nuevos préstamos.")

            # Recargar las vistas automáticamente
            self.buscar_prestamos()
            # Refrescar la vista principal de socios que muestra prestamos_activos
            if hasattr(self, 'buscar_socios'):
                self.buscar_socios('')

        except Exception as e:
            print(f"❌ Error al devolver préstamo: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo devolver el préstamo: {e}")

    # FUNCIÓN DE DIAGNÓSTICO
    def verificar_estado_socios(self):
        """Función para verificar el estado actual de los socios"""
        try:
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            
            cur.execute("SELECT id_socio, nombres, apellidos, prestamos_activos FROM Socios ORDER BY id_socio")
            socios = cur.fetchall()
            
            print("=== ESTADO ACTUAL DE SOCIOS ===")
            for socio in socios:
                print(f"ID: {socio[0]} | Nombre: {socio[1]} {socio[2]} | Préstamos Activos: {socio[3]}")
            
            conn.close()
            
        except Exception as e:
            print(f"Error al verificar socios: {e}")

    # FUNCIÓN ADICIONAL PARA CORREGIR DATOS EXISTENTES
    def corregir_prestamos_negativos(self):
        """Función auxiliar para corregir socios con préstamos activos negativos"""
        try:
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            
            # Corregir todos los préstamos negativos a 0
            cur.execute("UPDATE Socios SET prestamos_activos = 0 WHERE prestamos_activos < 0")
            filas_afectadas = cur.rowcount
            
            conn.commit()
            conn.close()
            
            if filas_afectadas > 0:
                messagebox.showinfo("Corrección", f"Se corrigieron {filas_afectadas} socios con préstamos negativos.")
            else:
                messagebox.showinfo("Corrección", "No hay préstamos negativos que corregir.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al corregir datos: {e}")
    
    def buscar_prestamos(self, event=None):
        """Buscar préstamos por socio, fecha o estado y actualizar el treeview"""
        texto = self.ent_buscar_lista_prestamos.get().strip().lower()
        
        # Limpiar treeview antes de cargar
        for row in self.tree_lista_prestamos.get_children():
            self.tree_lista_prestamos.delete(row)

        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()

        if texto:
            # Buscar con filtro
            cursor.execute("""
                SELECT 
                    p.id_prestamo, 
                    p.fecha_retiro, 
                    p.fecha_devolucion, 
                    s.nombres || ' ' || s.apellidos AS socio,
                    GROUP_CONCAT(l.titulo, ', ') AS libros,
                    p.estado
                FROM prestamos p
                INNER JOIN socios s ON p.id_socio = s.id_socio
                INNER JOIN prestamos_libros pl ON p.id_prestamo = pl.id_prestamo
                INNER JOIN libros l ON pl.id_libro = l.id_libro
                WHERE lower(s.nombres || ' ' || s.apellidos) LIKE ?
                OR lower(p.estado) LIKE ?
                OR p.fecha_retiro LIKE ?
                OR p.fecha_devolucion LIKE ?
                OR lower(GROUP_CONCAT(l.titulo, ', ')) LIKE ?
                GROUP BY p.id_prestamo, p.fecha_retiro, p.fecha_devolucion, socio, p.estado
                ORDER BY p.id_prestamo DESC
            """, (f"%{texto}%", f"%{texto}%", f"%{texto}%", f"%{texto}%", f"%{texto}%"))
        else:
            # Cargar todos los préstamos
            cursor.execute("""
                SELECT 
                    p.id_prestamo, 
                    p.fecha_retiro, 
                    p.fecha_devolucion, 
                    s.nombres || ' ' || s.apellidos AS socio,
                    GROUP_CONCAT(l.titulo, ', ') AS libros,
                    p.estado
                FROM prestamos p
                INNER JOIN socios s ON p.id_socio = s.id_socio
                INNER JOIN prestamos_libros pl ON p.id_prestamo = pl.id_prestamo
                INNER JOIN libros l ON pl.id_libro = l.id_libro
                GROUP BY p.id_prestamo, p.fecha_retiro, p.fecha_devolucion, socio, p.estado
                ORDER BY p.id_prestamo DESC
            """)

        prestamos = cursor.fetchall()
        
        # Insertar resultados en el treeview
        for prestamo in prestamos:
            self.tree_lista_prestamos.insert("", "end", values=prestamo)

        conn.close()
        print(f"Búsqueda completada. {len(prestamos)} préstamos encontrados.")

    def limpiar_formulario_prestamo(self):
        """Limpiar el formulario después de guardar"""
        # Limpiar variables
        if hasattr(self, 'socio_seleccionado_id'):
            delattr(self, 'socio_seleccionado_id')
        if hasattr(self, 'libros_seleccionados'):
            delattr(self, 'libros_seleccionados')
        
        # Limpiar entries
        self.ent_socio_crear_prestamo.delete(0, 'end')
        for i in range(1, 4):
            entry = getattr(self, f"ent_seleccionar_libro{i}_crear_prestamo")
            entry.delete(0, 'end')
        
        # Actualizar correlativo
        self.correlativo_prestamos()

    def correlativo_prestamos(self):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()      
            #Creamos la consulta
            mi_cursor.execute("SELECT MAX(Id_prestamo) FROM Prestamos")
            correlativo_prestamos=mi_cursor.fetchone()
            for datos in correlativo_prestamos:
                if datos==None:
                    self.crear_correlativo_prestamo=(int(1))
                    self.ent_id_crear_prestamo.config(state=NORMAL)
                    self.ent_id_crear_prestamo.insert(0,self.crear_correlativo_prestamo)
                    self.ent_id_crear_prestamo.config(state='readonly')
                else:
                    self.crear_correlativo_prestamo=(int(datos)+1)
                    self.ent_id_crear_prestamo.config(state=NORMAL)
                    self.ent_id_crear_prestamo.insert(0,self.crear_correlativo_prestamo)
                    self.ent_id_crear_prestamo.config(state='readonly')
            
            #Aplicar cambios
            mi_conexion.commit()
        except:
            messagebox.showerror('Correlativo Préstamos','Ocurrió un error')

    def centrar_ventana_crear_prestamo(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_crear_prestamo.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

#Seleccionar Socios
    def ventana_seleccionar_socio(self):
        # Tu código actual...
        top = Toplevel(self)
        top.title('Seleccionar Socio')
        self.frame_seleccionar_socio = top
        try:
            self.centrar_ventana_seleccionar_socio(620, 580)
        except Exception:
            pass
        top.grab_set()

        # --- Buscador ---
        lf_busq = tb.LabelFrame(master=top, text="Buscar")
        lf_busq.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        self.ent_buscar_seleccionar_socio = tb.Entry(lf_busq, width=67)
        self.ent_buscar_seleccionar_socio.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # --- Lista ---
        lf_lista = tb.LabelFrame(master=top, text="Socios")
        lf_lista.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

        columnas = ("id", "dni", "apellidos", "nombres")
        tree = tb.Treeview(lf_lista, height=15, columns=columnas, show='headings', bootstyle='primary')
        tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tree_lista_seleccionar_socio = tree

        # Cabeceras
        tree.heading("id", text="ID", anchor=W)
        tree.heading("dni", text="D.N.I", anchor=W)
        tree.heading("apellidos", text="Apellidos", anchor=W)
        tree.heading("nombres", text="Nombres", anchor=W)

        # Anchos
        tree.column("id", width=60, anchor=W)
        tree.column("dni", width=110, anchor=W)
        tree.column("apellidos", width=190, anchor=W)
        tree.column("nombres", width=190, anchor=W)

        # Scrollbar
        sb = tb.Scrollbar(master=lf_lista, bootstyle='primary-round')
        sb.grid(row=0, column=1, padx=5, pady=10, sticky="ns")
        tree.configure(yscrollcommand=sb.set)
        sb.configure(command=tree.yview)

        # --- Helpers para cargar / filtrar ---
        def cargar_socios(texto=""):
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            if texto:
                like = f"%{texto}%"
                cur.execute("""
                    SELECT Id_socio, dni, apellidos, nombres
                    FROM Socios
                    WHERE (CAST(dni AS TEXT) LIKE ?
                    OR lower(apellidos) LIKE ?
                    OR lower(nombres) LIKE ?)
                    AND Id_socio NOT IN (SELECT Id_socio FROM Prestamos WHERE Id_socio IS NOT NULL)
                    ORDER BY apellidos, nombres;
                """, (like, like.lower(), like.lower()))
            else:
                cur.execute("""
                    SELECT s.Id_socio, s.dni, s.apellidos, s.nombres
                    FROM Socios s
                    WHERE s.Id_socio NOT IN (SELECT p.Id_socio FROM Prestamos p WHERE p.Id_socio IS NOT NULL)
                    ORDER BY s.Apellidos, s.Nombres;
                """)
            rows = cur.fetchall()
            conn.close()

            tree.delete(*tree.get_children())
            for r in rows:
                tree.insert("", "end", values=r)

        # NUEVA FUNCIÓN: Confirmar selección del socio
        def confirmar_seleccion_socio():
            seleccionado = tree.selection()
            if seleccionado:
                valores = tree.item(seleccionado[0], "values")
                # Guardar los datos del socio seleccionado
                self.socio_seleccionado_id = valores[0]
                self.socio_seleccionado_nombre = f"{valores[2]} {valores[3]}"  # apellidos + nombres
                
                # Mostrar en el entry de la ventana principal
                self.ent_socio_crear_prestamo.delete(0, 'end')
                self.ent_socio_crear_prestamo.insert(0, self.socio_seleccionado_nombre)
                
                # Cerrar ventana de selección
                top.destroy()
            else:
                messagebox.showwarning("Atención", "Debes seleccionar un socio.")

        # NUEVO: Frame para botones
        lf_botones = tb.LabelFrame(master=top)
        lf_botones.grid(row=2, column=0, padx=8, pady=8, sticky="ew")
        
        # NUEVO: Botón confirmar
        btn_confirmar = tb.Button(lf_botones, text="Confirmar Selección", bootstyle='success', command=confirmar_seleccion_socio)
        btn_confirmar.grid(row=0, column=0, padx=10, pady=10)
        
        # NUEVO: Botón cancelar
        btn_cancelar = tb.Button(lf_botones, text="Cancelar", bootstyle='secondary', command=top.destroy)
        btn_cancelar.grid(row=0, column=1, padx=10, pady=10)

        # Bind para buscar cuando escriba
        def on_buscar(event):
            cargar_socios(self.ent_buscar_seleccionar_socio.get())
        
        self.ent_buscar_seleccionar_socio.bind('<KeyRelease>', on_buscar)
        
        # NUEVO: Doble clic para confirmar automáticamente
        def on_doble_clic(event):
            confirmar_seleccion_socio()
        
        tree.bind('<Double-1>', on_doble_clic)

        # Cargar socios inicialmente
        cargar_socios()
        
    def cargar_socios(self):
            """Carga todos los socios al Treeview"""
            for row in self.tree_lista_seleccionar_socio.get_children():
                self.tree_lista_seleccionar_socio.delete(row)

            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            cur.execute("SELECT Id_socio, apellidos, nombres FROM Socios")
            for row in cur.fetchall():
                self.tree_lista_seleccionar_socio.insert("",END,values=row)
            conn.close()

    def buscar_seleccionar_socios(self, event=None):
            """Filtra los socios en base al texto ingresado"""
            texto = self.ent_buscar_seleccionar_socio.get().strip().lower()

            for row in self.tree_lista_seleccionar_socio.get_children():
                self.tree_lista_seleccionar_socio.delete(row)

            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            cur.execute("SELECT Id_socio,dni,apellidos,nombres FROM Socios WHERE apellidos LIKE ? OR nombres LIKE ?",(f"%{texto}%", f"%{texto}%"))
            for row in cur.fetchall():
                self.tree_lista_seleccionar_socio.insert("",END,values=row)
            conn.close()
        
    def centrar_ventana_seleccionar_socio(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_seleccionar_socio.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

#Seleccionar Libros
    def ventana_seleccionar_libro(self, nro):
        # --- Toplevel ---
        top = Toplevel(self)
        top.title(f"Seleccionar Libro {nro}")
        self.frame_seleccionar_libro = top
        try:
            self.centrar_ventana_seleccionar_libro(620, 515)
        except Exception:
            pass
        top.grab_set()

        # --- Buscador ---
        lf_busq = tb.LabelFrame(master=top, text="Buscar")
        lf_busq.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        self.ent_buscar_seleccionar_libro = tb.Entry(lf_busq, width=67)
        self.ent_buscar_seleccionar_libro.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # --- Lista ---
        lf_lista = LabelFrame(master=top, text="Libros")
        lf_lista.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

        columnas = ("id", "titulo", "autor", "cantidad")
        tree = tb.Treeview(lf_lista, height=15, columns=columnas, show='headings', bootstyle='primary')
        tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Cabeceras
        tree.heading("id", text="ID", anchor=W)
        tree.heading("titulo", text="Título", anchor=W)
        tree.heading("autor", text="Autor", anchor=W)
        tree.heading("cantidad", text="Cantidad", anchor=W)

        # Anchos
        tree.column("id", width=60, anchor=W)
        tree.column("titulo", width=210, anchor=W)
        tree.column("autor", width=200, anchor=W)
        tree.column("cantidad", width=80, anchor=W)

        # Scrollbar
        sb = tb.Scrollbar(master=lf_lista, bootstyle='primary-round')
        sb.grid(row=0, column=1, padx=5, pady=10, sticky="ns")
        tree.configure(yscrollcommand=sb.set)
        sb.configure(command=tree.yview)

        # --- Helpers para cargar / filtrar ---
        def cargar_libros(texto=""):
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            if texto:
                like = f"%{texto}%"
                cur.execute("""
                    SELECT Id_libro, titulo, autor, cantidad
                    FROM Libros
                    WHERE (lower(titulo) LIKE ? OR lower(autor) LIKE ?)
                    AND cantidad > 0
                    ORDER BY titulo
                """, (like.lower(), like.lower()))
            else:
                cur.execute("""
                    SELECT Id_libro, titulo, autor, cantidad
                    FROM Libros
                    WHERE cantidad > 0
                    ORDER BY titulo
                """)
            rows = cur.fetchall()
            conn.close()

            tree.delete(*tree.get_children())
            for r in rows:
                tree.insert("", "end", values=r)

        def filtrar(_event=None):
            texto = self.ent_buscar_seleccionar_libro.get().strip().lower()
            cargar_libros(texto)

        self.ent_buscar_seleccionar_libro.bind("<KeyRelease>", filtrar)

        # Carga inicial
        cargar_libros()

        # --- NUEVA función para confirmar selección ---
        def confirmar():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Atención", "Debes seleccionar un libro.")
                return
            
            valores = tree.item(sel[0], "values")  # (id, titulo, autor, cantidad)
            
            # NUEVO: Inicializar el diccionario de libros seleccionados si no existe
            if not hasattr(self, 'libros_seleccionados'):
                self.libros_seleccionados = {}
            
            # NUEVO: Guardar datos del libro en el diccionario
            self.libros_seleccionados[nro] = {
                'id': valores[0],
                'titulo': valores[1],
                'autor': valores[2]
            }
            
            print(f"Libro {nro} seleccionado: ID={valores[0]}, Título={valores[1]}")
            
            # Mostrar en el entry correspondiente (mantener tu lógica actual)
            try:
                if nro == 1 and hasattr(self, "ent_seleccionar_libro1_crear_prestamo"):
                    self.ent_seleccionar_libro1_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro1_crear_prestamo.insert(0, f"{valores[1]} - {valores[2]}")
                elif nro == 2 and hasattr(self, "ent_seleccionar_libro2_crear_prestamo"):
                    self.ent_seleccionar_libro2_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro2_crear_prestamo.insert(0, f"{valores[1]} - {valores[2]}")
                elif nro == 3 and hasattr(self, "ent_seleccionar_libro3_crear_prestamo"):
                    self.ent_seleccionar_libro3_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro3_crear_prestamo.insert(0, f"{valores[1]} - {valores[2]}")
            except Exception as e:
                print(f"Error al actualizar entry: {e}")

            top.destroy()

        # NUEVO: Frame para botones
        lf_botones_lib = tb.LabelFrame(master=top)
        lf_botones_lib.grid(row=2, column=0, padx=8, pady=8, sticky="ew")

        # Botón Guardar selección
        btn_guardar = tb.Button(lf_botones_lib, text="Guardar selección", width=25,
                                bootstyle="success", command=confirmar)
        btn_guardar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # NUEVO: Botón Cancelar
        btn_cancelar = tb.Button(lf_botones_lib, text="Cancelar", width=25,
                            bootstyle="secondary", command=top.destroy)
        btn_cancelar.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="e")

        # Doble click para seleccionar
        tree.bind("<Double-1>", lambda e: confirmar())

        # Expandir correctamente
        top.columnconfigure(0, weight=1)
        top.rowconfigure(1, weight=1)
        lf_lista.columnconfigure(0, weight=1)
        lf_lista.rowconfigure(0, weight=1)
        lf_lista.columnconfigure(1, weight=1)  # NUEVO: Para el botón cancelar

    def buscar_libros(self, event=None):
        texto = self.ent_buscar_seleccionar_libro.get().strip().lower()
        
        for row in self.tree_lista_seleccionar_libro.get_children():
            self.tree_lista_seleccionar_libro.delete(row)

        conn = sqlite3.connect("biblioteca.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT Id_libro, titulo, autor, cantidad FROM Libros WHERE titulo LIKE ? OR autor LIKE ? AND cantidad > 0",
            (f"%{texto}%", f"%{texto}%")
        )
        for row in cur.fetchall():
            self.tree_lista_seleccionar_libro.insert("", END, values=row)
        conn.close()

    def centrar_ventana_seleccionar_libro(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_seleccionar_libro.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

#Modificar Préstamos
    def ventana_modificar_prestamo(self):
        item = self.tree_lista_prestamos.selection()
        if not item:
            messagebox.showwarning("Atención", "Debe seleccionar un préstamo para modificar.")
            return

        # Obtener datos del préstamo seleccionado
        prestamo_seleccionado = self.tree_lista_prestamos.item(item, "values")
        id_prestamo_original = prestamo_seleccionado[0]
        fecha_retiro_original = prestamo_seleccionado[1]
        fecha_devolucion_original = prestamo_seleccionado[2]
        socio = prestamo_seleccionado[3]

        # Crear ventana
        self.frame_modificar_prestamo = Toplevel(master=self)
        self.frame_modificar_prestamo.title('Modificar Préstamo')
        self.centrar_ventana_modificar_prestamo(600, 540)
        self.frame_modificar_prestamo.grab_set()

        lblframen_modificar_prestamo = tb.LabelFrame(master=self.frame_modificar_prestamo, text='Modificar Préstamo')
        lblframen_modificar_prestamo.pack(padx=15, pady=15)

        # ID (mantener el mismo, no editable)
        lbl_id_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='ID Préstamo')
        lbl_id_modificar_prestamo.grid(row=0, column=0, padx=10, pady=10)
        self.ent_id_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_id_modificar_prestamo.grid(row=0, column=1, padx=10, pady=10)
        self.ent_id_modificar_prestamo.insert(0, str(id_prestamo_original))
        self.ent_id_modificar_prestamo.config(state="readonly")

        # Fecha de Retiro (mantener la original, no editable)
        lbl_retiro_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='Fecha de Retiro')
        lbl_retiro_modificar_prestamo.grid(row=1, column=0, padx=10, pady=10)
        self.ent_retiro_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_retiro_modificar_prestamo.grid(row=1, column=1, padx=10, pady=10)
        self.ent_retiro_modificar_prestamo.insert(0, fecha_retiro_original)
        self.ent_retiro_modificar_prestamo.config(state="readonly")

        # Fecha de Devolución (mantener la original, no editable)
        lbl_devolucion_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='Fecha de Devolución')
        lbl_devolucion_modificar_prestamo.grid(row=2, column=0, padx=10, pady=10)
        self.ent_devolucion_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_devolucion_modificar_prestamo.grid(row=2, column=1, padx=10, pady=10)
        self.ent_devolucion_modificar_prestamo.insert(0, fecha_devolucion_original)
        self.ent_devolucion_modificar_prestamo.config(state="readonly")

        # Socio (no editable, solo mostrar)
        lbl_socio = Label(master=lblframen_modificar_prestamo, text="Socio")
        lbl_socio.grid(row=3, column=0, padx=10, pady=10)
        self.ent_socio_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_socio_modificar_prestamo.grid(row=3, column=1, padx=10, pady=10)
        self.ent_socio_modificar_prestamo.insert(0, socio)
        self.ent_socio_modificar_prestamo.config(state="readonly")

        # Selección de libros (solo esto es editable)
        self.entries_libros_modificar = []
        for i in range(1, 4):
            btn = tb.Button(master=lblframen_modificar_prestamo, text=f'Seleccionar Libro {i}',
                            bootstyle='secondary', command=lambda x=i: self.ventana_seleccionar_libro_modificar(x))
            btn.grid(row=3 + i, column=0, padx=10, pady=10)
            entry = tb.Entry(master=lblframen_modificar_prestamo, width=40)
            entry.grid(row=3 + i, column=1, padx=10, pady=10)
            self.entries_libros_modificar.append(entry)

        # Cargar libros actuales del préstamo
        self.cargar_libros_prestamo_actual(id_prestamo_original)

        # Estado fijo en Prestado (no editable)
        lbl_estado = Label(master=lblframen_modificar_prestamo, text="Estado")
        lbl_estado.grid(row=7, column=0, padx=10, pady=10)
        self.var_estado = StringVar(value="Prestado")
        combo_estado = tb.Combobox(master=lblframen_modificar_prestamo, textvariable=self.var_estado,
                                values=["Prestado"], width=37, state="readonly")
        combo_estado.grid(row=7, column=1, padx=10, pady=10)

        # Botón Guardar
        btn_guardar_prestamo = tb.Button(
            master=lblframen_modificar_prestamo, 
            text='Guardar Modificación', width=39, bootstyle='success',
            command=lambda: self.guardar_modificacion_prestamo(id_prestamo_original)
        )
        btn_guardar_prestamo.grid(row=8, column=1, padx=10, pady=10)

    def cargar_libros_prestamo_actual(self, id_prestamo):
        """Carga los libros actuales del préstamo en los entries"""
        try:
            # Conectar a la base de datos y obtener los libros del préstamo
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            # Query para obtener los libros del préstamo usando la tabla de relación
            cur.execute("""
                SELECT l.Titulo
                FROM Prestamos_Libros pl
                INNER JOIN Libros l ON pl.Id_libro = l.Id_libro
                WHERE pl.Id_prestamo = ?
                ORDER BY pl.Id_prestamo_libro
            """, (id_prestamo,))
            
            resultados = cur.fetchall()
            
            # Llenar los entries con los libros actuales
            for i, resultado in enumerate(resultados):
                if i < len(self.entries_libros_modificar):  # No exceder la cantidad de entries
                    self.entries_libros_modificar[i].delete(0, 'end')
                    self.entries_libros_modificar[i].insert(0, resultado[0])  # resultado[0] es el título
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los libros del préstamo: {str(e)}")

    def ventana_seleccionar_libro_modificar(self, numero_libro):
        # Crear ventana de selección
        top = Toplevel(self)
        top.title(f"Seleccionar Libro {numero_libro}")
        top.resizable(False, False)  # Hacer que la ventana no sea redimensionable
        self.frame_seleccionar_libro = top  # Cambiar aquí para que coincida con el resto del código
        try:
            self.centrar_ventana_seleccionar_libro_modificar(620, 570)
        except Exception:
            pass
        top.grab_set()

        # Frame para búsqueda
        frame_busqueda = tb.LabelFrame(master=self.frame_seleccionar_libro, text='Buscar')
        frame_busqueda.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

        # Campo de búsqueda
        self.ent_buscar_libro = tb.Entry(master=frame_busqueda, width=67)
        self.ent_buscar_libro.grid(row=0, column=0, padx=10, pady=10)
        
        # Función local para filtrar libros
        def filtrar_libros(event=None):
            texto = self.ent_buscar_libro.get().strip()
            # Limpiar treeview
            for item in self.tree_seleccionar_libro.get_children():
                self.tree_seleccionar_libro.delete(item)
            
            try:
                conn = sqlite3.connect("biblioteca.db")
                cur = conn.cursor()
                if texto:
                    like = f"%{texto}%"
                    cur.execute("""
                        SELECT Id_libro, Titulo, Autor, Cantidad
                        FROM Libros
                        WHERE (LOWER(Titulo) LIKE ? OR LOWER(Autor) LIKE ?)
                        AND Cantidad > 0
                        ORDER BY Titulo
                    """, (like.lower(), like.lower()))
                else:
                    cur.execute("""
                        SELECT Id_libro, Titulo, Autor, Cantidad
                        FROM Libros
                        WHERE Cantidad > 0
                        ORDER BY Titulo
                    """)
                libros = cur.fetchall()
                conn.close()
                
                # Insertar en treeview
                for libro in libros:
                    estado = "Disponible" if libro[3] > 0 else "No disponible"
                    valores = (libro[0], libro[1], libro[2], estado)
                    self.tree_seleccionar_libro.insert('', 'end', values=valores)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al filtrar libros: {str(e)}")
        
        self.ent_buscar_libro.bind('<KeyRelease>', filtrar_libros)

        # Treeview para mostrar libros
        self.frame_lista = tb.LabelFrame(master=self.frame_seleccionar_libro, text='Libros')
        self.frame_lista.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

        self.tree_seleccionar_libro = tb.Treeview(master=self.frame_lista, columns=('id', 'titulo', 'autor', 'estado'),show='headings', height=15,bootstyle=('primary'))
        
        # Configurar columnas
        self.tree_seleccionar_libro.heading('id', text='ID')
        self.tree_seleccionar_libro.heading('titulo', text='Título')
        self.tree_seleccionar_libro.heading('autor', text='Autor')
        self.tree_seleccionar_libro.heading('estado', text='Estado')
        
        self.tree_seleccionar_libro.column('id', width=50)
        self.tree_seleccionar_libro.column('titulo', width=200)
        self.tree_seleccionar_libro.column('autor', width=150)
        self.tree_seleccionar_libro.column('estado', width=100)
        
        # Usar grid para el treeview y scrollbar
        self.tree_seleccionar_libro.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Scrollbar
        sb = tb.Scrollbar(master=self.frame_lista, bootstyle='primary-round')
        sb.grid(row=0, column=1, padx=5, pady=10, sticky="ns")
        self.tree_seleccionar_libro.configure(yscrollcommand=sb.set)
        sb.configure(command=self.tree_seleccionar_libro.yview)
        
        # Configurar grid para que se expanda correctamente
        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.rowconfigure(0, weight=1)

        # Función para confirmar selección
        def confirmar():
            sel = self.tree_seleccionar_libro.selection()
            if not sel:
                messagebox.showwarning("Atención", "Debes seleccionar un libro.")
                return
            
            valores = self.tree_seleccionar_libro.item(sel[0], "values")  # (id, titulo, autor, estado)
            
            # Mostrar en el entry correspondiente
            entry_index = numero_libro - 1
            if entry_index < len(self.entries_libros_modificar):
                self.entries_libros_modificar[entry_index].delete(0, 'end')
                self.entries_libros_modificar[entry_index].insert(0, f"{valores[1]} - {valores[2]}")
            
            top.destroy()

        # Frame para botones
        lf_botones_lib = tb.LabelFrame(master=self.frame_seleccionar_libro)
        lf_botones_lib.grid(row=2, column=0, padx=8, pady=8, sticky="ew")

        # Botón Guardar selección
        btn_guardar = tb.Button(lf_botones_lib, text="Guardar selección", width=25,
                                bootstyle="success", command=confirmar)
        btn_guardar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Botón Cancelar
        btn_cancelar = tb.Button(lf_botones_lib, text="Cancelar", width=25,
                            bootstyle="secondary", command=top.destroy)
        btn_cancelar.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="e")

        # Doble click para seleccionar
        self.tree_seleccionar_libro.bind("<Double-1>", lambda e: confirmar())

        # Configurar grid de la ventana principal
        self.frame_seleccionar_libro.columnconfigure(0, weight=1)
        self.frame_seleccionar_libro.rowconfigure(1, weight=1)
        lf_botones_lib.columnconfigure(1, weight=1)

        # Cargar libros disponibles
        self.cargar_libros_disponibles_modificar()

    def confirmar_seleccion_libro_modificar(self, numero_libro):
        """Confirma la selección del libro y lo coloca en el entry correspondiente"""
        item = self.tree_seleccionar_libro.selection()
        if not item:
            messagebox.showwarning("Atención", "Debe seleccionar un libro.")
            return
        
        # Obtener datos del libro seleccionado
        libro_seleccionado = self.tree_seleccionar_libro.item(item, "values")
        titulo_libro = libro_seleccionado[1]  # Asumiendo que el título está en la columna 1
        
        # Colocar el libro en el entry correspondiente
        entry_index = numero_libro - 1
        self.entries_libros_modificar[entry_index].delete(0, 'end')
        self.entries_libros_modificar[entry_index].insert(0, titulo_libro)
        
        # Cerrar ventana de selección
        self.frame_seleccionar_libro.destroy()

    def centrar_ventana_seleccionar_libro_modificar(self, ancho, altura):
            ventana_ancho = ancho
            ventana_altura = altura
            
            pantalla_ancho = self.winfo_screenwidth()
            pantalla_alto = self.winfo_screenheight()
            
            coordenadas_x = int((pantalla_ancho/2) - (ventana_ancho/2))
            coordenadas_y = int((pantalla_alto/2) - (ventana_altura/2))
            
            # Usar self.frame_seleccionar_libro en lugar de self.frame_ventana_seleccionar_libro_modificar
            self.frame_seleccionar_libro.geometry('{}x{}+{}+{}'.format(ventana_ancho, ventana_altura, coordenadas_x, coordenadas_y))

    def cargar_libros_disponibles_modificar(self):
        """Carga los libros disponibles en el treeview"""
        try:
            # Limpiar treeview
            for item in self.tree_seleccionar_libro.get_children():
                self.tree_seleccionar_libro.delete(item)
            
            # Conectar a la base de datos
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            
            # Obtener todos los libros con la estructura correcta
            cur.execute("SELECT Id_libro, Titulo, Autor, Cantidad FROM Libros")
            libros = cur.fetchall()
            
            # Insertar en treeview
            for libro in libros:
                # Convertir cantidad a estado (disponible si cantidad > 0)
                estado = "Disponible" if libro[3] > 0 else "No disponible"
                valores = (libro[0], libro[1], libro[2], estado)
                self.tree_seleccionar_libro.insert('', 'end', values=valores)
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar libros: {str(e)}")

    def filtrar_libros_modificar(self, event=None):
        """Filtra los libros según el texto de búsqueda"""
        busqueda = self.ent_buscar_libro.get().lower()
        
        # Limpiar treeview
        for item in self.tree_seleccionar_libro.get_children():
            self.tree_seleccionar_libro.delete(item)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            
            # Query con filtro usando los nombres correctos de columnas
            if busqueda:
                cur.execute("""
                    SELECT Id_libro, Titulo, Autor, Cantidad 
                    FROM Libros 
                    WHERE LOWER(Titulo) LIKE ? OR LOWER(Autor) LIKE ?
                """, (f'%{busqueda}%', f'%{busqueda}%'))  # Solo 2 parámetros, no 3
            else:
                cur.execute("SELECT Id_libro, Titulo, Autor, Cantidad FROM Libros")
            
            libros = cur.fetchall()
            
            # Insertar en treeview
            for libro in libros:
                # Convertir cantidad a estado (disponible si cantidad > 0)
                estado = "Disponible" if libro[3] > 0 else "No disponible"  # libro[3] es la cantidad
                valores = (libro[0], libro[1], libro[2], estado)  # Solo 4 valores: id, titulo, autor, estado
                self.tree_seleccionar_libro.insert('', 'end', values=valores)
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar libros: {str(e)}")

    def centrar_ventana_modificar_prestamo(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_modificar_prestamo.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def guardar_modificacion_prestamo(self, id_prestamo_original):
        """Guarda las modificaciones del préstamo"""
        try:
            # Obtener datos del formulario
            # No usar el ID del campo (que es el mismo del original), generar uno nuevo
            fecha_retiro = self.ent_retiro_modificar_prestamo.get().strip()
            fecha_devolucion = self.ent_devolucion_modificar_prestamo.get().strip()
            socio = self.ent_socio_modificar_prestamo.get().strip()
            estado = self.var_estado.get()
            
            # Obtener libros seleccionados
            libros_seleccionados = []
            for entry in self.entries_libros_modificar:
                libro = entry.get().strip()
                if libro:
                    libros_seleccionados.append(libro)
            
            # Validaciones
            if not fecha_retiro or not fecha_devolucion or not socio:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            if not libros_seleccionados:
                messagebox.showerror("Error", "Debe seleccionar al menos un libro.")
                return
            
            # Conectar a BD y generar nuevo ID
            conn = sqlite3.connect("biblioteca.db")
            cur = conn.cursor()
            
            # Generar nuevo ID automáticamente (obtener el máximo + 1)
            cur.execute("SELECT MAX(Id_prestamo) FROM Prestamos")
            resultado_max = cur.fetchone()
            nuevo_id = 1 if resultado_max[0] is None else resultado_max[0] + 1
            
            # Primero, intentemos obtener el ID del socio del préstamo original
            cur.execute("SELECT Id_socio FROM Prestamos WHERE Id_prestamo = ?", (id_prestamo_original,))
            resultado_socio = cur.fetchone()
            
            if resultado_socio:
                id_socio = resultado_socio[0]
            else:
                # Si no funciona, buscar por nombre (usando la misma lógica que tu cargar_prestamos)
                cur.execute("SELECT Id_socio FROM Socios WHERE (Nombres || ' ' || Apellidos) = ?", (socio,))
                resultado_socio = cur.fetchone()
                
                if not resultado_socio:
                    # Mostrar todos los socios para debug
                    cur.execute("SELECT Id_socio, Nombres, Apellidos FROM Socios LIMIT 5")
                    socios_ejemplo = cur.fetchall()
                    messagebox.showerror("Error", 
                        f"No se encontró el socio: '{socio}'\n\n" +
                        f"Ejemplos de socios en BD: {socios_ejemplo}\n\n" +
                        "Verifica el formato del nombre del socio.")
                    conn.close()
                    return
                
                id_socio = resultado_socio[0]
            
            # Marcar el préstamo anterior como modificado
            cur.execute("UPDATE Prestamos SET Estado = ? WHERE Id_prestamo = ?", 
                        ("Modificado", id_prestamo_original))
            
            # Crear nuevo préstamo
            cur.execute("""
                INSERT INTO Prestamos (Id_prestamo, Id_socio, Fecha_retiro, Fecha_devolucion, Estado)
                VALUES (?, ?, ?, ?, ?)
            """, (nuevo_id, id_socio, fecha_retiro, fecha_devolucion, estado))
            
            # Eliminar libros del préstamo anterior
            cur.execute("DELETE FROM Prestamos_Libros WHERE Id_prestamo = ?", (id_prestamo_original,))
            
            # Agregar libros al nuevo préstamo
            for libro_titulo_formato in libros_seleccionados:
                # Extraer solo el título (antes del " - ")
                titulo_solo = libro_titulo_formato.split(" - ")[0] if " - " in libro_titulo_formato else libro_titulo_formato
                
                # Obtener ID del libro
                cur.execute("SELECT Id_libro FROM Libros WHERE Titulo = ?", (titulo_solo,))
                resultado_libro = cur.fetchone()
                
                if resultado_libro:
                    id_libro = resultado_libro[0]
                    # Insertar en tabla de relación
                    cur.execute("""
                        INSERT INTO Prestamos_Libros (Id_prestamo, Id_libro)
                        VALUES (?, ?)
                    """, (nuevo_id, id_libro))
            
            # Confirmar cambios
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "Préstamo modificado correctamente.")
            
            # Cerrar ventana y actualizar lista
            self.frame_modificar_prestamo.destroy()
            self.cargar_prestamos()  # Método correcto para actualizar la lista
            
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al modificar el préstamo: {str(e)}")
            if 'conn' in locals():
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            if 'conn' in locals():
                conn.close()

    def ventana_modificar_prestamo(self):
        item = self.tree_lista_prestamos.selection()
        if not item:
            messagebox.showwarning("Atención", "Debe seleccionar un préstamo para modificar.")
            return

        # Obtener datos del préstamo seleccionado
        prestamo_seleccionado = self.tree_lista_prestamos.item(item, "values")
        id_prestamo_original = prestamo_seleccionado[0]
        fecha_retiro_original = prestamo_seleccionado[1]
        fecha_devolucion_original = prestamo_seleccionado[2]
        socio = prestamo_seleccionado[3]

        # Crear ventana
        self.frame_modificar_prestamo = Toplevel(master=self)
        self.frame_modificar_prestamo.title('Modificar Préstamo')
        self.centrar_ventana_modificar_prestamo(600, 540)
        self.frame_modificar_prestamo.grab_set()

        lblframen_modificar_prestamo = tb.LabelFrame(master=self.frame_modificar_prestamo, text='Modificar Préstamo')
        lblframen_modificar_prestamo.pack(padx=15, pady=15)

        # ID (mantener el mismo, no editable)
        lbl_id_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='ID Préstamo')
        lbl_id_modificar_prestamo.grid(row=0, column=0, padx=10, pady=10)
        self.ent_id_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_id_modificar_prestamo.grid(row=0, column=1, padx=10, pady=10)
        self.ent_id_modificar_prestamo.insert(0, str(id_prestamo_original))
        self.ent_id_modificar_prestamo.config(state="readonly")

        # Fecha de Retiro (mantener la original, no editable)
        lbl_retiro_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='Fecha de Retiro')
        lbl_retiro_modificar_prestamo.grid(row=1, column=0, padx=10, pady=10)
        self.ent_retiro_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_retiro_modificar_prestamo.grid(row=1, column=1, padx=10, pady=10)
        self.ent_retiro_modificar_prestamo.insert(0, fecha_retiro_original)
        self.ent_retiro_modificar_prestamo.config(state="readonly")

        # Fecha de Devolución (mantener la original, no editable)
        lbl_devolucion_modificar_prestamo = Label(master=lblframen_modificar_prestamo, text='Fecha de Devolución')
        lbl_devolucion_modificar_prestamo.grid(row=2, column=0, padx=10, pady=10)
        self.ent_devolucion_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_devolucion_modificar_prestamo.grid(row=2, column=1, padx=10, pady=10)
        self.ent_devolucion_modificar_prestamo.insert(0, fecha_devolucion_original)
        self.ent_devolucion_modificar_prestamo.config(state="readonly")

        # Socio (no editable, solo mostrar)
        lbl_socio = Label(master=lblframen_modificar_prestamo, text="Socio")
        lbl_socio.grid(row=3, column=0, padx=10, pady=10)
        self.ent_socio_modificar_prestamo = tb.Entry(master=lblframen_modificar_prestamo, width=40)
        self.ent_socio_modificar_prestamo.grid(row=3, column=1, padx=10, pady=10)
        self.ent_socio_modificar_prestamo.insert(0, socio)
        self.ent_socio_modificar_prestamo.config(state="readonly")

        # Selección de libros (solo esto es editable)
        self.entries_libros_modificar = []
        for i in range(1, 4):
            btn = tb.Button(master=lblframen_modificar_prestamo, text=f'Seleccionar Libro {i}',
                            bootstyle='secondary', command=lambda x=i: self.ventana_seleccionar_libro_modificar(x))
            btn.grid(row=3 + i, column=0, padx=10, pady=10)
            entry = tb.Entry(master=lblframen_modificar_prestamo, width=40)
            entry.grid(row=3 + i, column=1, padx=10, pady=10)
            self.entries_libros_modificar.append(entry)

        # Cargar libros actuales del préstamo
        self.cargar_libros_prestamo_actual(id_prestamo_original)

        # Estado fijo en Prestado (no editable)
        lbl_estado = Label(master=lblframen_modificar_prestamo, text="Estado")
        lbl_estado.grid(row=7, column=0, padx=10, pady=10)
        self.var_estado = StringVar(value="Prestado")
        combo_estado = tb.Combobox(master=lblframen_modificar_prestamo, textvariable=self.var_estado,
                                values=["Prestado"], width=37, state="readonly")
        combo_estado.grid(row=7, column=1, padx=10, pady=10)

        # Botón Guardar
        btn_guardar_prestamo = tb.Button(
            master=lblframen_modificar_prestamo, 
            text='Guardar Modificación', width=39, bootstyle='success',
            command=lambda: self.guardar_modificacion_prestamo(id_prestamo_original)
        )
        btn_guardar_prestamo.grid(row=8, column=1, padx=10, pady=10)

#============================USUARIOS============================================
    def ventana_lista_usuarios(self): 
        self.borrar_frames()
        self.frame_lista_usuarios=Frame(master=self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=1,sticky=NSEW)
        
        lblframe_botones_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_botones_lista_usuarios.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
        
        btn_agregar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Agregar Usuario',width=17,bootstyle='success',command=self.ventana_nuevo_usuario)
        btn_agregar_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
            
        btn_modificar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Modificar Usuario',width=17,bootstyle='warning',command=self.ventana_modificar_usuario)
        btn_modificar_lista_usuarios.grid(row=0,column=1,padx=10,pady=10)
        
        btn_eliminar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Eliminar Usuario',width=17,bootstyle='danger',command=self.eliminar_usuario)
        btn_eliminar_lista_usuarios.grid(row=0,column=2,padx=10,pady=10)
        
        lblframe_busqueda_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_busqueda_lista_usuarios.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_lista_usuarios=tb.Entry(master=lblframe_busqueda_lista_usuarios,width=100,)
        self.ent_buscar_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_lista_usuarios.bind('<Key>',self.buscar_usuarios)
        
        lblframe_tree_lista_usuarios=LabelFrame(master=self.frame_lista_usuarios)
        lblframe_tree_lista_usuarios.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("codigo","correo","apellidos","nombres","clave","rol")
        
        #Crear el treeeview
        self.tree_lista_usuarios=tb.Treeview(master=lblframe_tree_lista_usuarios,height=22,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        
        #Crear las cabeceras
        self.tree_lista_usuarios.heading('codigo',text='Código',anchor=W)
        self.tree_lista_usuarios.heading('correo',text='Correo',anchor=W)
        self.tree_lista_usuarios.heading('apellidos',text='Apellidos',anchor=W)
        self.tree_lista_usuarios.heading('nombres',text='Nombres',anchor=W) 
        self.tree_lista_usuarios.heading('clave',text='Clave',anchor=W)
        self.tree_lista_usuarios.heading('rol',text='Rol',anchor=W)
        
        #Configurar las columnas que se muestren
        #self.tree_lista_usuarios['displaycolumns']=('codigo','correo','apellidos','nombres','rol')
        
        #Tamaño de las columnas
        self.tree_lista_usuarios.column('codigo',width=100)
        self.tree_lista_usuarios.column('correo',width=300)
        self.tree_lista_usuarios.column('apellidos',width=250)
        self.tree_lista_usuarios.column('nombres',width=250)
        self.tree_lista_usuarios.column('clave',width=150)
        self.tree_lista_usuarios.column('rol',width=150)
        
        #Crear el Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_usuarios,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=10)
        
        #Configurar el Scrollbar
        tree_scroll.config(command=self.tree_lista_usuarios.yview)
        self.buscar_usuarios('')
        self.ent_buscar_lista_usuarios.focus()

    def buscar_usuarios(self,event):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            #Limpiar nuestro treeview
            registro=self.tree_lista_usuarios.get_children()
            for elementos in registro:
                self.tree_lista_usuarios.delete(elementos)
            #Creamos la consulta
            mi_cursor.execute("SELECT * FROM Usuarios")
            datos_usuarios=mi_cursor.fetchall()
            #Insertar las filas en el treeview
            for fila in datos_usuarios:
                # Ocultar la contraseña con asteriscos (fila[4] es la clave)
                clave_oculta = "*" * len(str(fila[4])) if fila[4] else ""
                
                # Insertar con la contraseña oculta
                self.tree_lista_usuarios.insert('',0,fila[0],values=(fila[0],fila[1],fila[2],fila[3],clave_oculta,fila[5]))
            
            #Aplicar cambios
            mi_conexion.commit()
            #Cerrar la conexión
            mi_conexion.close()
        except Exception as e:
            print(f"Error en buscar_usuarios: {e}")

    # También puedes agregar esta función auxiliar a tu clase para reutilizar:
    def ocultar_clave(self, clave):
        """
        Convierte la contraseña en asteriscos
        """
        if clave:
            return "*" * len(str(clave))
        return ""

    def logueo_usuarios(self):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            con_usuario=self.ent_usuario.get()
            con_clave=self.ent_clave.get()
            
            #Creamos la consulta
            mi_cursor.execute("SELECT * FROM Usuarios WHERE Correo=? AND Clave=?",(con_usuario,con_clave))
            datos_logueo=mi_cursor.fetchall()
            if datos_logueo!='':
                for fila in datos_logueo:
                    correo_usuario_logueado=fila[1]
                    clave_usuario_logueado=fila[4]
                if(correo_usuario_logueado==self.ent_usuario.get() and clave_usuario_logueado==self.ent_clave.get()):
                    self.ventana_menu()
                    self.frame_login.destroy()
            
            #Aplicar cambios
            mi_conexion.commit()
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showwarning('Iniciar Sesión','El Usuario o Clave son incorrectos')      

    def ventana_nuevo_usuario(self):
        self.frame_nuevo_usuario=Toplevel(master=self)
        self.frame_nuevo_usuario.title('Nuevo Usuario')
        self.centrar_ventana_nuevo_usuario(500,420)
        self.frame_nuevo_usuario.grab_set()
        
        lblframen_nuevo_usuario=tb.LabelFrame(master=self.frame_nuevo_usuario,text='Nuevo Usuario')
        lblframen_nuevo_usuario.pack(padx=15,pady=15)
        
        lbl_codigo_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Código')
        lbl_codigo_nuevo_usuario.grid(row=0,column=0,padx=10,pady=10)
        self.ent_codigo_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_codigo_nuevo_usuario.grid(row=0,column=1,padx=10,pady=10)
        
        lbl_correo_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Correo')
        lbl_correo_nuevo_usuario.grid(row=1,column=0,padx=10,pady=10)
        self.ent_correo_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_correo_nuevo_usuario.grid(row=1,column=1,padx=10,pady=10)
        
        lbl_apellidos_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Apellidos')
        lbl_apellidos_nuevo_usuario.grid(row=2,column=0,padx=10,pady=10)
        self.ent_apellidos_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_apellidos_nuevo_usuario.grid(row=2,column=1,padx=10,pady=10)
        
        lbl_nombres_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Nombres')
        lbl_nombres_nuevo_usuario.grid(row=3,column=0,padx=10,pady=10)
        self.ent_nombres_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_nombres_nuevo_usuario.grid(row=3,column=1,padx=10,pady=10)
        
        lbl_clave_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Clave')
        lbl_clave_nuevo_usuario.grid(row=4,column=0,padx=10,pady=10)
        self.ent_clave_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_clave_nuevo_usuario.grid(row=4,column=1,padx=10,pady=10)
        self.ent_clave_nuevo_usuario.config(show='*')
        
        lbl_rol_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Rol')
        lbl_rol_nuevo_usuario.grid(row=5,column=0,padx=10,pady=10)
        self.cbo_rol_nuevo_usuario=tb.Combobox(master=lblframen_nuevo_usuario,width=40,values=['Administrador','Bibliotecario'])
        self.cbo_rol_nuevo_usuario.grid(row=5,column=1,padx=10,pady=10)
        self.cbo_rol_nuevo_usuario.current(0)
        self.cbo_rol_nuevo_usuario.config(state='readonly')
        
        btn_guardar_usuario=tb.Button(master=lblframen_nuevo_usuario,text='Guardar',width=38,bootstyle='success',command=self.guardar_usuario)
        btn_guardar_usuario.grid(row=6,column=1,padx=10,pady=10)
        self.correlativo_usuarios()
        self.ent_correo_nuevo_usuario.focus()        

    def centrar_ventana_nuevo_usuario(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_nuevo_usuario.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def guardar_usuario(self):
        if(self.ent_codigo_nuevo_usuario.get()==''or self.ent_correo_nuevo_usuario.get()==''or self.ent_apellidos_nuevo_usuario.get()==''or self.ent_nombres_nuevo_usuario.get()==''or self.ent_clave_nuevo_usuario.get()==''or self.cbo_rol_nuevo_usuario.get()==''):
            messagebox.showerror('Guardando Usuarios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            guardar_datos_usuarios=(self.ent_codigo_nuevo_usuario.get(),self.ent_correo_nuevo_usuario.get(),self.ent_apellidos_nuevo_usuario.get(),self.ent_nombres_nuevo_usuario.get(),self.ent_clave_nuevo_usuario.get(),self.cbo_rol_nuevo_usuario.get())
        
            #Creamos la consulta
            mi_cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?,?)",(guardar_datos_usuarios))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Guardando Usuarios','Registro guardado correctamente')
            self.frame_nuevo_usuario.destroy()
            self.buscar_usuarios('') 
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Guardando Usuarios','Ocurrió un error')

    def correlativo_usuarios(self):
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()      
            #Creamos la consulta
            mi_cursor.execute("SELECT MAX(Codigo) FROM Usuarios")
            correlativo_usuarios=mi_cursor.fetchone()
            for datos in correlativo_usuarios:
                if datos==None:
                    self.nuevo_correlativo_usuario=(int(1))
                    self.ent_codigo_nuevo_usuario.config(state=NORMAL)
                    self.ent_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    self.ent_codigo_nuevo_usuario.config(state='readonly')
                else:
                    self.nuevo_correlativo_usuario=(int(datos)+1)
                    self.ent_codigo_nuevo_usuario.config(state=NORMAL)
                    self.ent_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    self.ent_codigo_nuevo_usuario.config(state='readonly')
            
            #Aplicar cambios
            mi_conexion.commit()
        except:
            messagebox.showerror('Correlativo Usuarios','Ocurrió un error')

    def ventana_modificar_usuario(self):
        self.usuario_seleccionado=self.tree_lista_usuarios.focus()
        self.valor_usuario_seleccionado=self.tree_lista_usuarios.item(self.usuario_seleccionado,'values')
        
        if self.valor_usuario_seleccionado!='':
            
            self.frame_modificar_usuario=Toplevel(master=self)
            self.frame_modificar_usuario.title('Modificar Usuario')
            self.centrar_ventana_modificar_usuario(500,430)
            self.frame_modificar_usuario.grab_set()
            
            lblframen_modificar_usuario=tb.LabelFrame(master=self.frame_modificar_usuario,text='Modificar Usuario')
            lblframen_modificar_usuario.pack(padx=15,pady=15)
            
            lbl_codigo_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Código')
            lbl_codigo_modificar_usuario.grid(row=0,column=0,padx=10,pady=10)
            self.ent_codigo_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_codigo_modificar_usuario.grid(row=0,column=1,padx=10,pady=10)
            
            lbl_correo_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Correo')
            lbl_correo_modificar_usuario.grid(row=1,column=0,padx=10,pady=10)
            self.ent_correo_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_correo_modificar_usuario.grid(row=1,column=1,padx=10,pady=10)
            
            lbl_apellidos_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Apeliidos')
            lbl_apellidos_modificar_usuario.grid(row=2,column=0,padx=10,pady=10)
            self.ent_apellidos_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_apellidos_modificar_usuario.grid(row=2,column=1,padx=10,pady=10)
            
            lbl_nombres_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Nombres')
            lbl_nombres_modificar_usuario.grid(row=3,column=0,padx=10,pady=10)
            self.ent_nombres_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_nombres_modificar_usuario.grid(row=3,column=1,padx=10,pady=10)
            
            lbl_clave_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Clave')
            lbl_clave_modificar_usuario.grid(row=4,column=0,padx=10,pady=10)
            self.ent_clave_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_clave_modificar_usuario.grid(row=4,column=1,padx=10,pady=10)
            self.ent_clave_modificar_usuario.config(show='*')
            
            lbl_rol_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Rol')
            lbl_rol_modificar_usuario.grid(row=5,column=0,padx=10,pady=10)
            self.cbo_rol_modificar_usuario=tb.Combobox(master=lblframen_modificar_usuario,width=40,values=['Administrador','Bibliotecario'])
            self.cbo_rol_modificar_usuario.grid(row=5,column=1,padx=10,pady=10)
            self.cbo_rol_modificar_usuario.config(state='readonly')
            
            btn_modificar_usuario=tb.Button(master=lblframen_modificar_usuario,text='Modificar',width=38,bootstyle='warning',command=self.modificar_usuario)
            btn_modificar_usuario.grid(row=6,column=1,padx=10,pady=10)
            self.llenar_entrys_modificar_usuario()
            self.ent_correo_modificar_usuario.focus()

    def centrar_ventana_modificar_usuario(self,ancho,altura):
        ventana_ancho=ancho
        ventana_altura=altura
        
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        
        coordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        coordenadas_y=int((pantalla_alto/2)-(ventana_altura/2))
        
        self.frame_modificar_usuario.geometry('{}x{}+{}+{}'.format(ventana_ancho,ventana_altura,coordenadas_x,coordenadas_y))

    def llenar_entrys_modificar_usuario(self):
        self.ent_codigo_modificar_usuario.delete(0,END)
        self.ent_correo_modificar_usuario.delete(0,END)
        self.ent_apellidos_modificar_usuario.delete(0,END)
        self.ent_nombres_modificar_usuario.delete(0,END)
        self.ent_clave_modificar_usuario.delete(0,END)
        self.cbo_rol_modificar_usuario.delete(0,END)
        
        self.ent_codigo_modificar_usuario.config(state=NORMAL)
        self.ent_codigo_modificar_usuario.insert(0,self.valor_usuario_seleccionado[0])
        self.ent_codigo_modificar_usuario.config(state='readonly')
        self.ent_correo_modificar_usuario.insert(0,self.valor_usuario_seleccionado[1])
        self.ent_apellidos_modificar_usuario.insert(0,self.valor_usuario_seleccionado[2])
        self.ent_nombres_modificar_usuario.insert(0,self.valor_usuario_seleccionado[3])
        self.ent_clave_modificar_usuario.insert(0,self.valor_usuario_seleccionado[4])
        self.cbo_rol_modificar_usuario.insert(0,self.valor_usuario_seleccionado[5])

    def modificar_usuario(self):
        if(self.ent_codigo_modificar_usuario.get()==''or self.ent_correo_modificar_usuario.get()==''or self.ent_apellidos_modificar_usuario.get()==''or self.ent_nombres_modificar_usuario.get()==''or self.ent_clave_modificar_usuario.get()==''or self.cbo_rol_modificar_usuario.get()==''):
            messagebox.showerror('Modificando Usuarios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            modificar_datos_usuarios=(self.ent_correo_modificar_usuario.get(),self.ent_apellidos_modificar_usuario.get(),self.ent_nombres_modificar_usuario.get(),self.ent_clave_modificar_usuario.get(),self.cbo_rol_modificar_usuario.get())
        
            #Creamos la consulta
            mi_cursor.execute("UPDATE Usuarios SET correo=?,apellidos=?,nombres=?,clave=?,rol=? WHERE Codigo="+self.ent_codigo_modificar_usuario.get(),(modificar_datos_usuarios))
            
            #Aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Modificando Usuarios','Registro modificado correctamente')
                        
            self.valor_usuario_seleccionado=self.tree_lista_usuarios.item(self.usuario_seleccionado,text='',values=(self.ent_codigo_modificar_usuario.get(),self.ent_correo_modificar_usuario.get(),self.ent_apellidos_modificar_usuario.get(),self.ent_nombres_modificar_usuario.get(),self.ent_clave_modificar_usuario.get(),self.cbo_rol_modificar_usuario.get()))
            self.frame_modificar_usuario.destroy()
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando Usuarios','Ocurrió un error')

    def eliminar_usuario(self):
        usuario_seleccionado_eliminar=self.tree_lista_usuarios.focus()
        valor_usuario_seleccionado_eliminar=self.tree_lista_usuarios.item(usuario_seleccionado_eliminar,'values')
        
        try:
            if valor_usuario_seleccionado_eliminar!='':
                respuesta=messagebox.askquestion('Eliminando Usuarios','¿Está seguro de eliminar el usuario seleccionado?')
                if respuesta=='yes':
                    #Conexion a la BD
                    mi_conexion=sqlite3.connect('biblioteca.db')
                    #Crear el cursor
                    mi_cursor=mi_conexion.cursor()
                        #Creamos la consulta
                    mi_cursor.execute("DELETE FROM Usuarios WHERE Codigo="+ str(valor_usuario_seleccionado_eliminar[0]))
                    #Aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Usuarios','Registro eliminado correctamente')
                    self.buscar_usuarios('')
                    #Cerrar la conexión
                    mi_conexion.close()
                else:
                    messagebox.showerror('Eliminando Usuarios','Eliminación cancelada')
                    self.ventana_lista_usuarios('')
        except:
            messagebox.showerror('Eliminando Usuarios','Ocurrió un error')

def main():
    app=Ventana()
    app.title('Sistema de Gestión de Socios y Control de Libros')
    app.iconbitmap("./imagenes/logo.ico")
    # 🔹 Tamaño fijo
    width, height = 1430,750
    app.geometry(f"{width}x{height}")

    # 🔹 Centrar la ventana en la pantalla
    app.update_idletasks()  # Necesario para calcular bien dimensiones
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

   # 🔹 Desactivar redimensionamiento
    app.resizable(False, False)

    tb.Style('yeti')
    app.mainloop()
       
if __name__=='__main__':
    main()