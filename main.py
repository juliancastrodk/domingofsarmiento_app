from tkinter import *
from tkinter import ttk,messagebox,StringVar
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
        btn_acceso=tb.Button(master=lblframe_login,width=38,text='Registrar usuario',bootstyle='secondary-outline',command=self.ventana_nuevo_usuario)
        btn_acceso.pack(padx=10,pady=10)

#Principal
    #def ventana_principal(self):

        
#Menu
    def ventana_menu(self):
        
        self.frame_left=Frame(master=self,width=200)
        self.frame_left.grid(row=0, column=0, sticky=NSEW)
        
        self.frame_center=Frame(master=self)
        self.frame_center.grid(row=0, column=1, sticky=NSEW)
        
        btn_principal=Button(master=self.frame_left,text='Principal',width=15, height=2)
        btn_principal.grid(row=0, column=0, padx=10, pady=10)
               
        btn_socios=Button(master=self.frame_left,text='Socios',width=15, height=2,command=self.ventana_lista_socios)
        btn_socios.grid(row=1, column=0, padx=10, pady=10)
        
        btn_libros=Button(master=self.frame_left,text='Libros',width=15, height=2,command=self.ventana_lista_libros)
        btn_libros.grid(row=2, column=0, padx=10, pady=10)
        
        btn_prestamos=Button(master=self.frame_left,text='Préstamos',width=15, height=2,command=self.ventana_lista_prestamos)
        btn_prestamos.grid(row=3, column=0, padx=10, pady=10)
        
        btn_usuarios=Button(master=self.frame_left,text='Usuarios',width=15, height=2,command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=4, column=0, padx=10, pady=10)
        
        btn_reportes=Button(master=self.frame_left,text='Reportes',width=15, height=2)
        btn_reportes.grid(row=5, column=0, padx=10, pady=10)
           
#Lista de socios
    def ventana_lista_socios(self):
        
        self.borrar_frames()
        self.frame_lista_socios=Frame(master=self.frame_center)
        self.frame_lista_socios.grid(row=0,column=1,columnspan=2,sticky=NSEW)
        
        lblframe_botones_lista_socios=tb.LabelFrame(master=self.frame_lista_socios)
        lblframe_botones_lista_socios.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
        
        btn_nuevo_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Nuevo',width=15,bootstyle='success',command=self.ventana_nuevo_socio)
        btn_nuevo_lista_socios.grid(row=0,column=0,padx=10,pady=10)
        
        btn_modificar_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_socio)
        btn_modificar_lista_socios.grid(row=0,column=1,padx=10,pady=10)
        
        btn_eliminar_lista_socios=tb.Button(master=lblframe_botones_lista_socios,text='Eliminar',width=15,bootstyle='danger',command=self.eliminar_socio)
        btn_eliminar_lista_socios.grid(row=0,column=2,padx=10,pady=10)
        
        lblframe_busqueda_socios=tb.LabelFrame(master=self.frame_lista_socios)
        lblframe_busqueda_socios.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_socios=tb.Entry(master=lblframe_busqueda_socios,width=136,)
        self.ent_buscar_socios.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_socios.bind("<KeyRelease>", self.buscar_socios)
        
        lblframe_tree_lista_socios=LabelFrame(master=self.frame_lista_socios)
        lblframe_tree_lista_socios.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("id_socio","dni","apellidos","nombres","telefono","direccion","estado")
        
        #Crear el treeeview
        self.tree_lista_socios=tb.Treeview(master=lblframe_tree_lista_socios,height=17,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_socios.grid(row=0,column=0,padx=10,pady=10)
        
        #Crear las cabeceras
        self.tree_lista_socios.heading('id_socio',text='ID',anchor=W)
        self.tree_lista_socios.heading('dni',text='D.N.I',anchor=W)
        self.tree_lista_socios.heading('apellidos',text='Apellidos',anchor=W)
        self.tree_lista_socios.heading('nombres',text='Nombres',anchor=W)
        self.tree_lista_socios.heading('telefono',text='Teléfono',anchor=W)
        self.tree_lista_socios.heading('direccion',text='Dirección',anchor=W)
        self.tree_lista_socios.heading('estado',text='Estado',anchor=W)
        
        #Tamaño de las columnas
        self.tree_lista_socios.column('id_socio',width=80)
        self.tree_lista_socios.column('dni',width=100)
        self.tree_lista_socios.column('apellidos',width=250)
        self.tree_lista_socios.column('nombres',width=250)
        self.tree_lista_socios.column('telefono',width=150)
        self.tree_lista_socios.column('direccion',width=200)
        self.tree_lista_socios.column('estado',width=150)
        
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
        cur.execute("SELECT Id_socio,dni,apellidos,nombres,telefono,direccion,estado FROM Socios WHERE apellidos LIKE ? OR nombres LIKE ?",
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
        self.centrar_ventana_nuevo_socio(600,500)
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
        
        btn_guardar_socio=tb.Button(master=lblframen_nuevo_socio,text='Guardar',width=49,bootstyle='success',command=self.guardar_socio)
        btn_guardar_socio.grid(row=7,column=1,padx=10,pady=10)
        self.correlativo_socios()
        self.ent_dni_nuevo_socio.focus()

#Ventana de guardar socio
    def guardar_socio(self):
        if(self.ent_id_nuevo_socio.get()==''or self.ent_dni_nuevo_socio.get()==''or self.ent_apellidos_nuevo_socio.get()==''or self.ent_nombres_nuevo_socio.get()==''or self.ent_telefono_nuevo_socio.get()==''or self.ent_direccion_nuevo_socio.get()==''or self.cbo_estado_nuevo_socio.get()==''):
            messagebox.showerror('Guardando Socios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            guardar_datos_socios=(self.ent_id_nuevo_socio.get(),self.ent_dni_nuevo_socio.get(),self.ent_apellidos_nuevo_socio.get(),self.ent_nombres_nuevo_socio.get(),self.ent_telefono_nuevo_socio.get(),self.ent_direccion_nuevo_socio.get(),self.cbo_estado_nuevo_socio.get())
        
            #Creamos la consulta
            mi_cursor.execute("INSERT INTO Socios VALUES(?,?,?,?,?,?,?)",(guardar_datos_socios))
            
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
            self.centrar_ventana_modificar_socio(600,500)
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
            
            btn_modificar_socio=tb.Button(master=lblframen_modificar_socio,text='Modificar',width=49,bootstyle='warning',command=self.modificar_socio)
            btn_modificar_socio.grid(row=7,column=1,padx=10,pady=10)
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
        
        self.ent_id_modificar_socio.config(state=NORMAL)
        self.ent_id_modificar_socio.insert(0,self.valor_socio_seleccionado[0])
        self.ent_id_modificar_socio.config(state='readonly')
        self.ent_dni_modificar_socio.insert(0,self.valor_socio_seleccionado[1])
        self.ent_apellidos_modificar_socio.insert(0,self.valor_socio_seleccionado[2])
        self.ent_nombres_modificar_socio.insert(0,self.valor_socio_seleccionado[3])
        self.ent_telefono_modificar_socio.insert(0,self.valor_socio_seleccionado[4])
        self.ent_direccion_modificar_socio.insert(0,self.valor_socio_seleccionado[5])
        self.cbo_estado_modificar_socio.insert(0,self.valor_socio_seleccionado[6])

#Modificar socio
    def modificar_socio(self):
        if(self.ent_id_modificar_socio.get()==''or self.ent_dni_modificar_socio.get()==''or self.ent_apellidos_modificar_socio.get()==''or self.ent_nombres_modificar_socio.get()==''or self.ent_telefono_modificar_socio.get()==''or self.ent_direccion_modificar_socio.get()==''or self.cbo_estado_modificar_socio.get()==''):
            messagebox.showerror('Modificando Socios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            modificar_datos_socios=(self.ent_dni_modificar_socio.get(),self.ent_apellidos_modificar_socio.get(),self.ent_nombres_modificar_socio.get(),self.ent_telefono_modificar_socio.get(),self.ent_direccion_modificar_socio.get(),self.cbo_estado_modificar_socio.get())
        
            #Creamos la consulta
            mi_cursor.execute("UPDATE Socios SET dni=?,apellidos=?,nombres=?,telefono=?,direccion=?,estado=? WHERE dni="+self.ent_dni_modificar_socio.get(),(modificar_datos_socios))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Modificando Socios','Registro modificado correctamente')
                        
            self.valor_socio_seleccionado=self.tree_lista_socios.item(self.socio_seleccionado,text='',values=(self.ent_id_modificar_socio.get(),self.ent_dni_modificar_socio.get(),self.ent_apellidos_modificar_socio.get(),self.ent_nombres_modificar_socio.get(),self.ent_telefono_modificar_socio.get(),self.ent_direccion_modificar_socio.get(),self.cbo_estado_modificar_socio.get()))
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
        lblframe_botones_lista_libros.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
        
        btn_nuevo_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Nuevo',width=15,bootstyle='success',command=self.ventana_nuevo_libro)
        btn_nuevo_lista_libros.grid(row=0,column=0,padx=10,pady=10)
        
        btn_modificar_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_libro)
        btn_modificar_lista_libros.grid(row=0,column=1,padx=10,pady=10)
        
        btn_eliminar_lista_libros=tb.Button(master=lblframe_botones_lista_libros,text='Eliminar',width=15,bootstyle='danger',command=self.eliminar_libro)
        btn_eliminar_lista_libros.grid(row=0,column=2,padx=10,pady=10)
        
        lblframe_busqueda_lista_libros=tb.LabelFrame(master=self.frame_lista_libros)
        lblframe_busqueda_lista_libros.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_libro=tb.Entry(master=lblframe_busqueda_lista_libros,width=147,)
        self.ent_buscar_libro.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_libro.bind('<Key>',self.buscar_libros_lista)
        
        lblframe_tree_lista_libros=LabelFrame(master=self.frame_lista_libros)
        lblframe_tree_lista_libros.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("id_libro","titulo","autor","isbn","editorial","año","cantidad","categoria")
        
        #Crear el treeeview
        self.tree_lista_libros=tb.Treeview(master=lblframe_tree_lista_libros,height=17,columns=columnas,show='headings',bootstyle='primary')
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
        self.tree_lista_libros.column('isbn',width=150)
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
        lblframe_botones_lista_prestamos.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
        
        btn_crear_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Crear Préstamo',width=17,bootstyle='success',command=self.ventana_crear_prestamo)
        btn_crear_prestamos.grid(row=0,column=0,padx=10,pady=10)
        
        btn_ver_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Ver Préstamo',width=17,bootstyle='info')
        btn_ver_prestamos.grid(row=0,column=1,padx=10,pady=10)
        
        btn_modificar_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Modificar Préstamo',width=17,bootstyle='warning')
        btn_modificar_prestamos.grid(row=0,column=2,padx=10,pady=10)
        
        btn_borrar_prestamos=tb.Button(master=lblframe_botones_lista_prestamos,text='Borrar Préstamo',width=17,bootstyle='danger')
        btn_borrar_prestamos.grid(row=0,column=3,padx=10,pady=10)
        
        lblframe_busqueda_lista_prestamos=tb.LabelFrame(master=self.frame_lista_prestamos)
        lblframe_busqueda_lista_prestamos.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_lista_prestamos=tb.Entry(master=lblframe_busqueda_lista_prestamos,width=90)
        self.ent_buscar_lista_prestamos.grid(row=0,column=0,padx=10,pady=10)
        
        lblframe_tree_lista_prestamos=LabelFrame(master=self.frame_lista_prestamos)
        lblframe_tree_lista_prestamos.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        
        # 👉 PRIMERO definir columnas
        columnas=("id_prestamo","retiro","devolucion","socio","estado")
        
        # 👉 AHORA usar columnas en el Treeview
        self.tree_lista_prestamos=tb.Treeview(
            master=lblframe_tree_lista_prestamos,
            height=17,
            columns=columnas,
            show='headings',
            bootstyle='primary'
        )
        self.tree_lista_prestamos.grid(row=0,column=0,padx=10,pady=10)

        # Cabeceras
        self.tree_lista_prestamos.heading('id_prestamo',text='ID',anchor=W)
        self.tree_lista_prestamos.heading('retiro',text='Fecha Retiro',anchor=W)
        self.tree_lista_prestamos.heading('devolucion',text='Fecha Devolución',anchor=W)
        self.tree_lista_prestamos.heading('socio',text='Socio',anchor=W)
        self.tree_lista_prestamos.heading('estado',text='Estado',anchor=W)

        # Tamaños de columnas
        self.tree_lista_prestamos.column('id_prestamo',width=70)
        self.tree_lista_prestamos.column('retiro',width=150)
        self.tree_lista_prestamos.column('devolucion',width=150)
        self.tree_lista_prestamos.column('socio',width=250)
        self.tree_lista_prestamos.column('estado',width=100)

        # Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_prestamos,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=10,sticky="ns")
        self.tree_lista_prestamos.config(yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree_lista_prestamos.yview)

        # 👉 Cargar préstamos automáticamente al abrir ventana
        self.cargar_prestamos()

    def cargar_prestamos(self):
        try:
            # Limpiar treeview antes de cargar
            for row in self.tree_lista_prestamos.get_children():
                self.tree_lista_prestamos.delete(row)

            conexion = sqlite3.connect("biblioteca.db")
            cursor = conexion.cursor()

            # Traer préstamos con datos del socio y libro
            cursor.execute("""
                SELECT 
                    p.id_prestamo, 
                    p.fecha_retiro, 
                    p.fecha_devolucion, 
                    s.nombres || ' ' || s.apellidos AS socio,
                    l.titulo AS libro,
                    p.estado
                FROM prestamos p
                INNER JOIN socios s ON p.id_socio = s.id_socio
                INNER JOIN libros l ON p.id_libro = l.id_libro
                ORDER BY p.id_prestamo DESC
            """)

            prestamos = cursor.fetchall()

            for prestamo in prestamos:
                # prestamo = (id, retiro, devolucion, socio, libro, estado)
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
            id_socio = getattr(self, "socio_seleccionado", None)
            id_libro = getattr(self, "libro_seleccionado", None)

            if not id_socio or not id_libro:
                messagebox.showwarning("Atención", "Debes seleccionar un socio y un libro antes de guardar.")
                return

            fecha_retiro = datetime.now().strftime("%Y-%m-%d")
            fecha_devolucion = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            conexion = sqlite3.connect("biblioteca.db")
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO prestamos (id_socio, id_libro, fecha_retiro, fecha_devolucion)
                VALUES (?, ?, ?, ?)
            """, (id_socio, id_libro, fecha_retiro, fecha_devolucion))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Préstamo guardado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el préstamo: {e}")

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

    def ventana_seleccionar_socio(self):
        self.frame_seleccionar_socio=Toplevel(master=self)
        self.frame_seleccionar_socio.title('Seleccionar Socio')
        self.centrar_ventana_seleccionar_socio(610,515)
        self.frame_seleccionar_socio.grab_set()
        
        lblframe_busqueda_seleccionar_socio=tb.LabelFrame(master=self.frame_seleccionar_socio)
        lblframe_busqueda_seleccionar_socio.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_seleccionar_socio=tb.Entry(master=lblframe_busqueda_seleccionar_socio,width=67)
        self.ent_buscar_seleccionar_socio.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_seleccionar_socio.bind('<KeyRelease>', self.buscar_seleccionar_socios)
        
        lblframe_tree_lista_seleccionar_socio=LabelFrame(master=self.frame_seleccionar_socio)
        lblframe_tree_lista_seleccionar_socio.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
    
        #Columnas
        columnas=("id","dni","nombres","apellidos")
        self.tree_lista_seleccionar_socio=tb.Treeview(master=lblframe_tree_lista_seleccionar_socio,height=15,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_seleccionar_socio.grid(row=0,column=0,padx=10,pady=10)
        
        # Cabeceras
        self.tree_lista_seleccionar_socio.heading("id",text="ID",anchor=W)
        self.tree_lista_seleccionar_socio.heading("dni",text="D.N.I",anchor=W)
        self.tree_lista_seleccionar_socio.heading("nombres",text="Nombres",anchor=W)
        self.tree_lista_seleccionar_socio.heading("apellidos",text="Apellidos",anchor=W)
        
        # Anchos
        self.tree_lista_seleccionar_socio.column("id",width=50)
        self.tree_lista_seleccionar_socio.column("dni",width=100)
        self.tree_lista_seleccionar_socio.column("nombres",width=200)
        self.tree_lista_seleccionar_socio.column("apellidos",width=200)
        
        # Scrollbar
        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_seleccionar_socio,bootstyle='primary-round')
        tree_scroll.grid(row=0,column=1,padx=5,pady=5)
        tree_scroll.config(command=self.tree_lista_seleccionar_socio.yview)

        # Cargar socios desde BD
        mi_conexion=sqlite3.connect("biblioteca.db")
        mi_cursor=mi_conexion.cursor()
        mi_cursor.execute("SELECT Id_socio,dni,apellidos,nombres FROM Socios")
        for row in mi_cursor.fetchall():
            self.tree_lista_seleccionar_socio.insert("",END,values=row)
        mi_conexion.close()
        
        def guardar_seleccionar_socio():
            try:
                item = self.tree_lista_seleccionar_socio.selection()[0]  # CORRECTO
                socio = self.tree_lista_seleccionar_socio.item(item, "values")
                
                id_socio_seleccionado = socio[0]
                self.ent_socio_crear_prestamo.delete(0, END)
                self.ent_socio_crear_prestamo.insert(0, f"{socio[0]} - {socio[1]} {socio[2]}")
                
                self.frame_seleccionar_socio.destroy()  # CORRECTO
            except:
                messagebox.showerror("Error", "Debes seleccionar un socio")

        # Botón guardar con la función vinculada
        btn_guardar_seleccion_socio = tb.Button(master=lblframe_tree_lista_seleccionar_socio,text='Guardar Selección', width=25, bootstyle='success',command=guardar_seleccionar_socio)
        btn_guardar_seleccion_socio.grid(row=3,column=0,padx=10,pady=10)
        
        btn_sel_socio = ttk.Button(ventana_socios, text="Seleccionar Socio", command=self.seleccionar_socio)
        btn_sel_socio.pack(pady=5)
    
    def seleccionar_socio(self):
        item = self.tree_socios.selection()
        if item:
            valores = self.tree_socios.item(item, "values")
            self.socio_seleccionado = valores[0]  # ID del socio
            messagebox.showinfo("Socio seleccionado", f"Socio ID {self.socio_seleccionado} seleccionado.")

    def seleccionar_libro(self):
        item = self.tree_libros.selection()
        if item:
            valores = self.tree_libros.item(item, "values")
            self.libro_seleccionado = valores[0]  # ID del libro
            messagebox.showinfo("Libro seleccionado", f"Libro ID {self.libro_seleccionado} seleccionado.")
        
    # --- NUEVAS FUNCIONES AUXILIARES ---
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
        self.frame_seleccionar_libro = Toplevel(master=self)
        self.frame_seleccionar_libro.title(f"Seleccionar Libro {nro}")
        self.centrar_ventana_seleccionar_libro(620, 515)
        self.frame_seleccionar_libro.grab_set()
        
        # Frame búsqueda
        lblframe_busqueda = tb.LabelFrame(master=self.frame_seleccionar_libro)
        lblframe_busqueda.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        
        self.ent_buscar_seleccionar_libro = tb.Entry(master=lblframe_busqueda, width=69)
        self.ent_buscar_seleccionar_libro.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_seleccionar_libro.bind('<KeyRelease>', self.buscar_libros)  # función para filtrar

        # Frame listado
        lblframe_tree_lista_seleccionar_libro = LabelFrame(master=self.frame_seleccionar_libro)
        lblframe_tree_lista_seleccionar_libro.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        columnas = ("id", "titulo", "autor", "cantidad")
        self.tree_lista_seleccionar_libro = tb.Treeview(lblframe_tree_lista_seleccionar_libro, height=15, columns=columnas, show="headings", bootstyle="primary"
        )
        self.tree_lista_seleccionar_libro.grid(row=0, column=0, padx=10, pady=10)

        # Cabeceras
        self.tree_lista_seleccionar_libro.heading("id", text="ID", anchor=W)
        self.tree_lista_seleccionar_libro.heading("titulo", text="Título", anchor=W)
        self.tree_lista_seleccionar_libro.heading("autor", text="Autor", anchor=W)
        self.tree_lista_seleccionar_libro.heading("cantidad", text="Cantidad", anchor=W)
        
        # Ancho de columnas
        self.tree_lista_seleccionar_libro.column("id", width=80)
        self.tree_lista_seleccionar_libro.column("titulo", width=200)
        self.tree_lista_seleccionar_libro.column("autor", width=200)
        self.tree_lista_seleccionar_libro.column("cantidad", width=80)
        
        # Scrollbar
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_seleccionar_libro, bootstyle='primary-round')
        tree_scroll.grid(row=0, column=1, padx=5, pady=5, sticky=NS)
        self.tree_lista_seleccionar_libro.config(yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree_lista_seleccionar_libro.yview)

        # Cargar libros
        conn = sqlite3.connect("biblioteca.db")
        cur = conn.cursor()
        cur.execute("SELECT Id_libro, titulo, autor, cantidad FROM Libros WHERE cantidad > 0")
        for row in cur.fetchall():
            self.tree_lista_seleccionar_libro.insert("", END, values=row)
        conn.close()
        
        # Función guardar
        def guardar_libro():
            try:
                item = self.tree_lista_seleccionar_libro.selection()[0]
                libro = self.tree_lista_seleccionar_libro.item(item, "values")
                if nro == 1:
                    self.ent_seleccionar_libro1_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro1_crear_prestamo.insert(0, f"{libro[0]} - {libro[1]}")
                elif nro == 2:
                    self.ent_seleccionar_libro2_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro2_crear_prestamo.insert(0, f"{libro[0]} - {libro[1]}")
                else:
                    self.ent_seleccionar_libro3_crear_prestamo.delete(0, END)
                    self.ent_seleccionar_libro3_crear_prestamo.insert(0, f"{libro[0]} - {libro[1]}")
                
                self.frame_seleccionar_libro.destroy()
            except:
                messagebox.showerror("Error","Debes seleccionar un libro")

        btn_guardar=tb.Button(master=lblframe_tree_lista_seleccionar_libro,text="Guardar Selección",bootstyle="success",width=30,command=guardar_libro)
        btn_guardar.grid(row=2,column=0,padx=10,pady=10)
        
        btn_sel_libro = ttk.Button(ventana_libros, text="Seleccionar Libro", command=self.seleccionar_libro)
        btn_sel_libro.pack(pady=5)

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

#============================USUARIOS============================================
    def ventana_lista_usuarios(self):
        
        self.borrar_frames()
        self.frame_lista_usuarios=Frame(master=self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=1,columnspan=2,sticky=NSEW)
        
        lblframe_botones_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_botones_lista_usuarios.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
               
        btn_modificar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Modificar Usuario',width=15,bootstyle='warning',command=self.ventana_modificar_usuario)
        btn_modificar_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        
        btn_eliminar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Eliminar Usuario',width=15,bootstyle='danger',command=self.eliminar_usuario)
        btn_eliminar_lista_usuarios.grid(row=0,column=1,padx=10,pady=10)
        
        lblframe_busqueda_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_busqueda_lista_usuarios.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)
        
        self.ent_buscar_lista_usuarios=tb.Entry(master=lblframe_busqueda_lista_usuarios,width=100,)
        self.ent_buscar_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_lista_usuarios.bind('<Key>',self.buscar_usuarios)
        
        lblframe_tree_lista_usuarios=LabelFrame(master=self.frame_lista_usuarios)
        lblframe_tree_lista_usuarios.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        
        #Crear columnas
        columnas=("codigo","correo","apellidos","nombres","clave")
        
        #Crear el treeeview
        self.tree_lista_usuarios=tb.Treeview(master=lblframe_tree_lista_usuarios,height=17,columns=columnas,show='headings',bootstyle='primary')
        self.tree_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        
        #Crear las cabeceras
        self.tree_lista_usuarios.heading('codigo',text='Código',anchor=W)
        self.tree_lista_usuarios.heading('correo',text='Correo',anchor=W)
        self.tree_lista_usuarios.heading('apellidos',text='Apellidos',anchor=W)
        self.tree_lista_usuarios.heading('nombres',text='Nombres',anchor=W) 
        self.tree_lista_usuarios.heading('clave',text='Clave',anchor=W)
        
        #Configurar las columnas que se muestren
        self.tree_lista_usuarios['displaycolumns']=('codigo','correo','apellidos','nombres')
        
        #Tamaño de las columnas
        self.tree_lista_usuarios.column('codigo',width=80)
        self.tree_lista_usuarios.column('correo',width=270)
        self.tree_lista_usuarios.column('apellidos',width=230)
        self.tree_lista_usuarios.column('nombres',width=230)
        self.tree_lista_usuarios.column('clave',width=150)
        
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
            #Insertar las filas en el treeviex
            for fila in datos_usuarios:
                self.tree_lista_usuarios.insert('',0,fila[0],values=(fila[0],fila[1],fila[2],fila[3],fila[4]))
            
            #Aplicar cambios
            mi_conexion.commit()
            #Cerrar la conexión
            mi_conexion.close()
        except:
            messagebox.showerror('Buscar Usuarios','Ocurrió un error')

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
        self.centrar_ventana_nuevo_usuario(500,400)
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
        
        btn_guardar_usuario=tb.Button(master=lblframen_nuevo_usuario,text='Guardar',width=38,bootstyle='success',command=self.guardar_usuario)
        btn_guardar_usuario.grid(row=5,column=1,padx=10,pady=10)
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
        if(self.ent_codigo_nuevo_usuario.get()==''or self.ent_correo_nuevo_usuario.get()==''or self.ent_apellidos_nuevo_usuario.get()==''or self.ent_nombres_nuevo_usuario.get()==''or self.ent_clave_nuevo_usuario.get()==''):
            messagebox.showerror('Guardando Usuarios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            guardar_datos_usuarios=(self.ent_codigo_nuevo_usuario.get(),self.ent_correo_nuevo_usuario.get(),self.ent_apellidos_nuevo_usuario.get(),self.ent_nombres_nuevo_usuario.get(),self.ent_clave_nuevo_usuario.get())
        
            #Creamos la consulta
            mi_cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?)",(guardar_datos_usuarios))
            
            #Aplicar cambios
            mi_conexion.commit()
            
            messagebox.showinfo('Guardando Usuarios','Registro guardado correctamente')
            self.frame_nuevo_usuario.destroy()
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
            self.centrar_ventana_modificar_usuario(500,400)
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
            
            btn_modificar_usuario=tb.Button(master=lblframen_modificar_usuario,text='Modificar',width=38,bootstyle='warning',command=self.modificar_usuario)
            btn_modificar_usuario.grid(row=8,column=1,padx=10,pady=10)
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
        
        self.ent_codigo_modificar_usuario.config(state=NORMAL)
        self.ent_codigo_modificar_usuario.insert(0,self.valor_usuario_seleccionado[0])
        self.ent_codigo_modificar_usuario.config(state='readonly')
        self.ent_correo_modificar_usuario.insert(0,self.valor_usuario_seleccionado[1])
        self.ent_apellidos_modificar_usuario.insert(0,self.valor_usuario_seleccionado[2])
        self.ent_nombres_modificar_usuario.insert(0,self.valor_usuario_seleccionado[3])
        self.ent_clave_modificar_usuario.insert(0,self.valor_usuario_seleccionado[4])

    def modificar_usuario(self):
        if(self.ent_codigo_modificar_usuario.get()==''or self.ent_correo_modificar_usuario.get()==''or self.ent_apellidos_modificar_usuario.get()==''or self.ent_nombres_modificar_usuario.get()==''or self.ent_clave_modificar_usuario.get()==''):
            messagebox.showerror('Modificando Usuarios','Completar todos los campos')
            return
        try:
            #Conexion a la BD
            mi_conexion=sqlite3.connect('biblioteca.db')
            #Crear el cursor
            mi_cursor=mi_conexion.cursor()
            
            modificar_datos_usuarios=(self.ent_codigo_modificar_usuario.get(),self.ent_correo_modificar_usuario.get(),self.ent_apellidos_modificar_usuario.get(),self.ent_nombres_modificar_usuario.get(),self.ent_clave_modificar_usuario.get())
        
            #Creamos la consulta
            mi_cursor.execute("UPDATE Usuarios SET correo=?,apellidos=?,nombres=?,clave=? WHERE Codigo="+self.ent_codigo_modificar_usuario.get(),(modificar_datos_usuarios))
            
            #Aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Modificando Usuarios','Registro modificado correctamente')
                        
            self.valor_usuario_seleccionado=self.tree_lista_usuarios.item(self.usuario_seleccionado,text='',values=(self.ent_codigo_modificar_usuario.get(),self.ent_correo_modificar_usuario.get(),self.ent_apellidos_modificar_usuario.get(),self.ent_nombres_modificar_usuario.get(),self.ent_clave_modificar_usuario.get()))
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
        except:
            messagebox.showerror('Eliminando Usuarios','Ocurrió un error')

def main():
    app=Ventana()
    app.title('Sistema de Gestión de Socios y Control de Libros')
    app.iconbitmap("./imagenes/logo.ico")
    app.state('zoomed')
    tb.Style('yeti')
    app.mainloop()
       
if __name__=='__main__':
    main()