from fpdf import FPDF
from datetime import datetime
from pathlib import Path
from typing import Optional


class BoletaFacade:
    """Fachada para generar una boleta (PDF) a partir de un `Pedido`."""

    def __init__(self, pedido) -> None:
        self.pedido = pedido
        self.detalle = ""
        self.subtotal = 0.0
        self.iva = 0.0
        self.total = 0.0

    def _format_currency(self, amount: float) -> str:
        return f"${amount:.2f}"

    def generar_detalle_boleta(self) -> None:
        self.detalle = ""
        for item in self.pedido.menus:
            if getattr(item, "cantidad", 0) > 0:
                subtotal = float(item.precio) * int(item.cantidad)
                precio_str = self._format_currency(float(item.precio))
                subtotal_str = self._format_currency(subtotal)
                line = (
                    f"{item.nombre:<30} {item.cantidad:<10} "
                    f"{precio_str:<10} {subtotal_str:<10}\n"
                )
                self.detalle += line
        self.subtotal = float(self.pedido.calcular_total())
        self.iva = round(self.subtotal * 0.19, 2)
        self.total = round(self.subtotal + self.iva, 2)

    def crear_pdf(self, output_path: Optional[str] = None) -> str:
        """Crea el PDF de la boleta y devuelve la ruta del archivo generado."""
        self.generar_detalle_boleta()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Boleta Restaurante", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, "Razón Social del Negocio", ln=True, align='L')
        pdf.cell(0, 8, "RUT: 12345678-9", ln=True, align='L')
        pdf.cell(0, 8, "Dirección: Calle Increible", ln=True, align='L')
        pdf.cell(0, 8, "Teléfono: +56 9 1234 5678", ln=True, align='L')
        fecha_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        pdf.cell(0, 8, f"Fecha: {fecha_str}", ln=True, align='R')
        pdf.ln(6)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(70, 8, "Nombre", border=1)
        pdf.cell(20, 8, "Cantidad", border=1)
        pdf.cell(35, 8, "Precio Unitario", border=1)
        pdf.cell(30, 8, "Subtotal", border=1)
        pdf.ln()
        pdf.set_font("Arial", size=12)
        for item in self.pedido.menus:
            if getattr(item, "cantidad", 0) > 0:
                subtotal = float(item.precio) * int(item.cantidad)
                pdf.cell(70, 8, str(item.nombre), border=1)
                pdf.cell(20, 8, str(item.cantidad), border=1)
                pdf.cell(35, 8, self._format_currency(float(item.precio)), border=1)
                pdf.cell(30, 8, self._format_currency(subtotal), border=1)
                pdf.ln()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 8, "Subtotal:", 0, 0, 'R')
        pdf.cell(30, 8, self._format_currency(self.subtotal), ln=True, align='R')
        pdf.cell(120, 8, "IVA (19%):", 0, 0, 'R')
        pdf.cell(30, 8, self._format_currency(self.iva), ln=True, align='R')
        pdf.cell(120, 8, "Total:", 0, 0, 'R')
        pdf.cell(30, 8, self._format_currency(self.total), ln=True, align='R')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 8, "Gracias por su compra.", 0, 1, 'C')

        pdf_filename = output_path or "boleta.pdf"
        pdf_path = Path(pdf_filename)
        # Ensure the output directory exists before writing the PDF
        try:
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            # ignore directory creation errors and let pdf.output raise if needed
            pass

        pdf.output(str(pdf_path))
        return str(pdf_path)

    def generar_boleta(self, output_path: Optional[str] = None) -> str:
        return self.crear_pdf(output_path=output_path)
