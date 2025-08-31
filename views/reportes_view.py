# file: views/reportes_view.py

import ttkbootstrap as tb
from tkinter import *

class ReportesView(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Frame para el menú de selección de reportes
        menu_frame = tb.Frame(self, bootstyle="light", width=250)
        menu_frame.grid(row=0, column=0, sticky="ns", padx=(10,5), pady=10)
        
        lbl_menu = tb.Label(menu_frame, text="Seleccionar Reporte", bootstyle="inverse-light", font=("Calibri", 14, "bold"))
        lbl_menu.pack(pady=15, padx=10)

        # Botones para cada reporte
        btn_resumen = tb.Button(menu_frame, text="Resumen de Inventario", command=self.controller.show_resumen, bootstyle="secondary")
        btn_resumen.pack(fill="x", padx=10, pady=5)
        
        btn_mas_solicitados = tb.Button(menu_frame, text="Libros más Solicitados", command=self.controller.show_mas_solicitados, bootstyle="secondary")
        btn_mas_solicitados.pack(fill="x", padx=10, pady=5)
        
        btn_vencidos = tb.Button(menu_frame, text="Préstamos Vencidos", command=self.controller.show_vencidos, bootstyle="secondary")
        btn_vencidos.pack(fill="x", padx=10, pady=5)

        # Frame para mostrar el contenido del reporte seleccionado
        self.report_content_frame = tb.Frame(self)
        self.report_content_frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
    
    def clear_content_frame(self):
        """Limpia el frame de contenido antes de mostrar un nuevo reporte."""
        for widget in self.report_content_frame.winfo_children():
            widget.destroy()

    def display_kpis(self, data):
        """Muestra los datos del resumen como tarjetas KPI."""
        self.clear_content_frame()
        
        title = tb.Label(self.report_content_frame, text="Resumen General", font=("Calibri", 20, "bold"))
        title.pack(pady=20)

        kpi_frame = tb.Frame(self.report_content_frame)
        kpi_frame.pack(expand=True)

        kpis = [
            ("Títulos Únicos en Biblioteca", data.get('total_titulos', 0), "primary"),
            ("Total de Copias Físicas", data.get('total_copias', 0), "info"),
            ("Socios Activos", data.get('socios_activos', 0), "success"),
            ("Préstamos Activos", data.get('prestamos_activos', 0), "warning")
        ]

        for i, (text, value, style) in enumerate(kpis):
            card = tb.Frame(kpi_frame, bootstyle=style, padding=20)
            card.grid(row=0, column=i, padx=15, pady=15)
            
            value_label = tb.Label(card, text=str(value), font=("Calibri", 36, "bold"), bootstyle=f"inverse-{style}")
            value_label.pack()
            text_label = tb.Label(card, text=text, font=("Calibri", 12), bootstyle=f"inverse-{style}")
            text_label.pack()

    def display_table_report(self, title_text, data, columns):
        """Muestra un reporte en formato de tabla (Treeview)."""
        self.clear_content_frame()

        title = tb.Label(self.report_content_frame, text=title_text, font=("Calibri", 20, "bold"))
        title.pack(pady=20, padx=10, anchor="w")
        
        frame_tree = tb.Frame(self.report_content_frame)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)
        frame_tree.rowconfigure(0, weight=1)
        frame_tree.columnconfigure(0, weight=1)

        # Extraer los nombres de las columnas para el Treeview
        column_keys = [key for key, _ in columns]
        
        tree = tb.Treeview(frame_tree, columns=column_keys, show="headings", bootstyle="primary")
        tree.grid(row=0, column=0, sticky="nsew")

        # Configurar encabezados y anchos
        for key, (header, width) in columns:
            tree.heading(key, text=header)
            tree.column(key, width=width)

        # Poblar tabla
        for row in data:
            tree.insert("", "end", values=row)

        # Scrollbar
        scrollbar = tb.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)