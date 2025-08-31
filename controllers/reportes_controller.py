# file: controllers/reportes_controller.py

from models.reportes_model import ReportesModel

class ReportesController:
    def __init__(self, view):
        self.view = view
        self.model = ReportesModel()

    def load_initial_report(self):
        """Carga el reporte inicial por defecto (el resumen)."""
        self.show_resumen()

    def show_resumen(self):
        kpi_data = self.model.get_resumen_inventario()
        self.view.display_kpis(kpi_data)

    def show_mas_solicitados(self):
        report_data = self.model.get_libros_mas_solicitados()
        column_config = [
            ("titulo", ("Título", 400)),
            ("autor", ("Autor", 350)),
            ("prestamos", ("Nº de Préstamos", 150))
        ]
        self.view.display_table_report("Libros más Solicitados", report_data, column_config)

    def show_vencidos(self):
        report_data = self.model.get_prestamos_vencidos()
        column_config = [
            ("id", ("ID Préstamo", 100)),
            ("socio", ("Socio", 300)),
            ("libros", ("Libros Prestados", 450)),
            ("fecha", ("Fecha de Devolución", 150))
        ]
        self.view.display_table_report("Préstamos Vencidos", report_data, column_config)