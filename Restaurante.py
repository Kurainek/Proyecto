import logging
import customtkinter as ctk
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from tkinter.font import nametofont
import os
from PIL import Image
import pandas as pd
from Ingrediente import Ingrediente
from Stock import Stock
from Pedido import Pedido
from BoletaFacade import BoletaFacade
from Menu_catalog import get_default_menus
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer
from manejador_errores import manejar_errores
from utilidades import formatear_precio
from gestor_cache import cached
from base_datos import obtener_sesion
from estadisticas import top_productos, total_ventas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler("restaurante.log")
    fh.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)


class AplicacionConPestanas(ctk.CTk):
    """Aplicación principal con pestañas para gestionar stock, pedidos y boletas.

    Esta clase encapsula la interfaz y la interacción con las entidades del
    dominio (Stock, Pedido, Ingrediente, etc.).
    """

    def __init__(self) -> None:
        super().__init__()

        self.title("Gestión de ingredientes y pedidos")
        self.geometry("870x700")
        nametofont("TkHeadingFont").configure(size=14)
        nametofont("TkDefaultFont").configure(size=11)

        self.stock = Stock()
        self.menus_creados = set()
        self.pedido = Pedido()
        self.menus = get_default_menus()

        self.tabview = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_pestanas()

    def actualizar_treeview(self) -> None:
        """Actualiza la vista de árbol (`self.tree`) con el contenido del stock.

        Si el treeview aún no existe, la función sale silenciosamente.
        """
        tree = getattr(self, "tree", None)
        if tree is None:
            return

        for item in tree.get_children():
            tree.delete(item)

        for ingrediente in self.stock.lista_ingredientes:
            vals = (
                ingrediente.nombre,
                ingrediente.unidad,
                ingrediente.cantidad,
            )
            tree.insert("", "end", values=vals)

    def on_tab_change(self):
        selected_tab = self.tabview.get()
        if selected_tab == "carga de ingredientes":
            logger.debug("Pestaña: carga de ingredientes seleccionada")
        if selected_tab == "Stock":
            self.actualizar_treeview()
        if selected_tab == "Pedido":
            self.actualizar_treeview()
            logger.debug("Pestaña: Pedido seleccionada")
        if selected_tab == "Carta restorante":
            self.actualizar_treeview()
            logger.debug("Pestaña: Carta restorante seleccionada")
        if selected_tab == "Boleta":
            self.actualizar_treeview()
            logger.debug("Pestaña: Boleta seleccionada")

    def crear_pestanas(self):
        self.tab3 = self.tabview.add("carga de ingredientes")
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        self.tab6 = self.tabview.add("Estadísticas")
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()
        self.configurar_pestana_estadisticas()

    def configurar_pestana3(self):
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV")
        label.pack(pady=20)
        boton_cargar_csv = ctk.CTkButton(
            self.tab3,
            text="Cargar CSV",
            fg_color="#1976D2",
            text_color="white",
            command=self.cargar_csv,
        )

        boton_cargar_csv.pack(pady=10)

        self.frame_tabla_csv = ctk.CTkFrame(self.tab3)
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10)
        self.df_csv = None
        self.tabla_csv = None

        self.boton_agregar_stock = ctk.CTkButton(
            self.frame_tabla_csv,
            text="Agregar al Stock",
        )
        self.boton_agregar_stock.pack(side="bottom", pady=10)
        self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)

    def cargar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Selecciona un archivo CSV",
            filetypes=[("Archivos CSV", "*.csv")],
        )
        if archivo:
            try:
                df = pd.read_csv(archivo)
                self.df_csv = df
                CTkMessagebox(
                    title="CSV Cargado",
                    message=f"Archivo cargado correctamente.\nFilas: {len(df)}",
                    icon="info",
                    sound=False,
                )
                self.mostrar_dataframe_en_tabla(df)
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Error al cargar el archivo:\n{e}",
                    icon="warning",
                    sound=False,
                )
        else:
            CTkMessagebox(
                title="Sin archivo",
                message="No se seleccionó ningún archivo.",
                icon="warning",
                sound=False,
            )

    def agregar_csv_al_stock(self):
        if self.df_csv is None:
            CTkMessagebox(
                title="Error",
                message="Primero debes cargar un archivo CSV.",
                icon="warning",
                sound=False,
            )
            return

        required_columns = ["nombre", "unidad", "cantidad"]
        for col in required_columns:
            if col not in self.df_csv.columns:
                CTkMessagebox(
                    title="Error",
                    message=f"El CSV debe tener columna '{col}'.",
                    icon="warning",
                    sound=False,
                )
                return

        for _, row in self.df_csv.iterrows():
            nombre = str(row["nombre"])
            cantidad = float(row["cantidad"])
            unidad = str(row["unidad"])
            ingrediente = Ingrediente(
                nombre=nombre, unidad=unidad, cantidad=cantidad
            )
            self.stock.agregar_ingrediente(ingrediente)

        CTkMessagebox(
            title="Stock Actualizado",
            message="Ingredientes agregados al stock correctamente.",
            icon="info",
            sound=False,
        )
        self.actualizar_treeview()

    def mostrar_dataframe_en_tabla(self, df):
        if self.tabla_csv:
            self.tabla_csv.destroy()

        self.tabla_csv = ttk.Treeview(
            self.frame_tabla_csv, columns=list(df.columns), show="headings"
        )
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)
            self.tabla_csv.column(col, width=100, anchor="center")

        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)

        for menu in self.pedido.menus:
            vals = (
                menu.nombre,
                menu.cantidad,
                f"${menu.precio:.2f}",
            )
            self.treeview_menu.insert("", "end", values=vals)

    def _configurar_pestana_crear_menu(self):
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_menu = ctk.CTkButton(
            contenedor,
            text="Generar Carta (PDF)",
            command=self.generar_y_mostrar_carta_pdf,
        )
        boton_menu.pack(pady=10)

        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None

    @manejar_errores()
    def generar_y_mostrar_carta_pdf(self):
        try:
            pdf_path = "carta.pdf"
            menus_disponibles = [
                menu
                for menu in self.menus
                if menu.esta_disponible(self.stock)
            ]

            if not menus_disponibles:
                CTkMessagebox(
                    title="Sin Menús Disponibles",
                    message="No hay menús disponibles según el stock actual.",
                    icon="info",
                    sound=False,
                )
                return

            create_menu_pdf(
                menus_disponibles,
                pdf_path,
                titulo_negocio="Restaurante",
                subtitulo="Carta Primavera 2025",
                moneda="$",
            )

            if self.pdf_viewer_carta is not None:
                try:
                    self.pdf_viewer_carta.pack_forget()
                    self.pdf_viewer_carta.destroy()
                except Exception:
                    pass
                finally:
                    self.pdf_viewer_carta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo generar la carta.\n{e}",
                icon="warning",
                sound=False,
            )

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_boleta = ctk.CTkButton(
            contenedor,
            text="Mostrar Boleta (PDF)",
            command=self.mostrar_boleta,
        )
        boton_boleta.pack(pady=10)

        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_boleta = None

    @manejar_errores()
    def mostrar_boleta(self):
        try:
            if not hasattr(self, "pedido") or not self.pedido:
                CTkMessagebox(
                    title="Atención",
                    message="No hay pedido para generar la boleta.",
                    icon="warning",
                    sound=False,
                )
                return

            boleta_facade = BoletaFacade(self.pedido)
            pdf_path = boleta_facade.crear_pdf()

            if self.pdf_viewer_boleta is not None:
                try:
                    self.pdf_viewer_boleta.pack_forget()
                    self.pdf_viewer_boleta.destroy()
                except Exception:
                    pass
                finally:
                    self.pdf_viewer_boleta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo generar/mostrar la boleta.\n{e}",
                icon="warning",
                sound=False,
            )

    def configurar_pestana1(self):
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Form
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_unidad = ctk.CTkLabel(frame_formulario, text="Unidad: unid")
        label_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(
            frame_formulario,
            text="Ingresar Ingrediente",
        )
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(
            frame_treeview,
            text="Eliminar Ingrediente",
            fg_color="black",
            text_color="white",
        )
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.tree = ttk.Treeview(
            self.tab1,
            columns=("Nombre", "Unidad", "Cantidad"),
            show="headings",
            height=25,
        )

        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_menu = ctk.CTkButton(
            frame_treeview,
            text="Generar Menú",
            command=self.generar_menus,
        )
        self.boton_generar_menu.pack(pady=10)

    @manejar_errores()
    def tarjeta_click(self, event, menu):
        suficiente_stock = True

        if not self.stock.lista_ingredientes:
            suficiente_stock = False

        for ingrediente_necesario in menu.ingredientes:
            ingrediente_en_stock = next(
                (
                    i
                    for i in self.stock.lista_ingredientes
                    if i.nombre == ingrediente_necesario.nombre
                ),
                None,
            )
            if (
                not ingrediente_en_stock
                or ingrediente_en_stock.cantidad < ingrediente_necesario.cantidad
            ):
                suficiente_stock = False
                break

        if suficiente_stock:
            for ingrediente_necesario in menu.ingredientes:
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad -= ingrediente_necesario.cantidad

            self.pedido.agregar_menu(menu)
            self.actualizar_treeview_pedido()
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            CTkMessagebox(
                title="Stock Insuficiente",
                message=(
                    f"No hay suficientes ingredientes para preparar "
                    f"'{menu.nombre}'"
                ),
                icon="warning",
                sound=False,
            )

    def cargar_icono_menu(self, ruta_icono):
        try:
            imagen = Image.open(ruta_icono)
            return ctk.CTkImage(imagen, size=(64, 64))
        except FileNotFoundError:
            logger.debug("No se encontró el icono: %s", ruta_icono)
            return None
        except Exception as e:
            logger.exception("Error al cargar icono '%s': %s", ruta_icono, e)
            return None

    @cached(ttl=60)
    def generar_menus(self):
        self.menus_disponibles = []
        menus = get_default_menus()

        for menu in menus:
            if menu.esta_disponible(self.stock):
                self.menus_disponibles.append(menu)

        for widget in self.frame_menus.winfo_children():
            widget.destroy()

        for menu in self.menus_disponibles:
            icono = self.cargar_icono_menu(menu.icono_path)
            tarjeta = ctk.CTkButton(
                self.frame_menus,
                image=icono,
                text=f"{menu.nombre}\n${menu.precio}",
                compound="top",
                width=150,
                height=150,
                command=(lambda m=menu: self.tarjeta_click(None, m)),
            )

            tarjeta.pack(side="left", padx=10, pady=10)

    @manejar_errores()
    def eliminar_menu(self):
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            CTkMessagebox(
                title="Atención",
                message="Selecciona un menú para eliminar.",
                icon="warning",
                sound=False,
            )
            return

        item = self.treeview_menu.item(seleccion[0])
        nombre_menu = item["values"][0]

        menu_encontrado = next(
            (m for m in self.pedido.menus if m.nombre == nombre_menu),
            None,
        )
        if menu_encontrado:
            for ing in menu_encontrado.ingredientes:
                for ing_stock in self.stock.lista_ingredientes:
                    if ing_stock.nombre == ing.nombre:
                        ing_stock.cantidad += ing.cantidad
                        break

            # Eliminar el menú del pedido y actualizar vistas y totales
            try:
                self.pedido.eliminar_menu(nombre_menu)
            except Exception:
                logger.exception(
                    "Error al eliminar el menú '%s' del pedido",
                    nombre_menu,
                )

            self.actualizar_treeview_pedido()

            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")

    @manejar_errores()
    def generar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(
                title="Advertencia",
                message="No hay menús en el pedido.",
                icon="warning",
                sound=False,
            )
            return

        try:
            boleta = BoletaFacade(self.pedido)
            boleta.generar_boleta()

            self.mostrar_boleta()
            CTkMessagebox(
                title="Éxito",
                message="Boleta generada correctamente.",
                icon="info",
                sound=False,
            )
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo generar la boleta.\n{e}",
                icon="warning",
                sound=False,
            )

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        self.frame_menus = ctk.CTkScrollableFrame(
            frame_superior,
            orientation="horizontal",
        )
        self.frame_menus.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(
            frame_intermedio,
            text="Eliminar Menú",
            command=self.eliminar_menu,
        )
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.label_total = ctk.CTkLabel(
            frame_intermedio,
            text="Total: $0.00",
            anchor="e",
            font=("Helvetica", 12, "bold"),
        )
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(
            frame_inferior,
            columns=("Nombre", "Cantidad", "Precio Unitario"),
            show="headings",
        )
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta = ctk.CTkButton(
            frame_inferior,
            text="Generar Boleta",
            command=self.generar_boleta,
        )
        self.boton_generar_boleta.pack(side="bottom", pady=10)

    def crear_tarjeta(self, menu):
        num_tarjetas = len(self.menus_creados)
        fila = 0
        columna = num_tarjetas

        tarjeta = ctk.CTkFrame(
            self.frame_menus,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50",
            width=64,
            height=140,
            fg_color="gray",
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(
                    tarjeta,
                    image=icono,
                    width=64,
                    height=64,
                    text="",
                    bg_color="transparent",
                )
                imagen_label.image = icono
                imagen_label.pack(anchor="center", pady=5, padx=10)
                imagen_label.bind(
                    "<Button-1>",
                    lambda event: self.tarjeta_click(event, menu),
                )
            except Exception:
                logger.exception("No se pudo cargar la imagen '%s'", menu.icono_path)

        texto_label = ctk.CTkLabel(
            tarjeta,
            text=f"{menu.nombre}",
            text_color="black",
            font=("Helvetica", 12, "bold"),
            bg_color="transparent",
        )
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

    def configurar_pestana_estadisticas(self):
        """Configura la pestaña de estadísticas (top productos y ventas totales)."""
        cont = ctk.CTkFrame(self.tab6)
        cont.pack(expand=True, fill="both", padx=10, pady=10)

        top_frame = ctk.CTkFrame(cont)
        top_frame.pack(side="top", fill="x", padx=10, pady=5)

        boton_refrescar = ctk.CTkButton(
            top_frame,
            text="Refrescar estadísticas",
            command=self.refrescar_estadisticas,
        )
        boton_refrescar.pack(side="left", padx=8)

        self.label_total_ventas = ctk.CTkLabel(
            top_frame, text="Total ventas: $0.00"
        )
        self.label_total_ventas.pack(side="right", padx=8)

        # Treeview para top productos
        frame_tabla = ctk.CTkFrame(cont)
        frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree_estadisticas = ttk.Treeview(
            frame_tabla,
            columns=("Producto", "Vendidos"),
            show="headings",
        )
        self.tree_estadisticas.heading("Producto", text="Producto")
        self.tree_estadisticas.heading("Vendidos", text="Cantidad Vendida")
        self.tree_estadisticas.pack(expand=True, fill="both")

        # Cargar inmediatamente
        try:
            self.refrescar_estadisticas()
        except Exception:
            pass

    @manejar_errores()
    def refrescar_estadisticas(self):
        """Consulta la BD y actualiza la vista de estadísticas."""
        # limpiar tabla
        for it in self.tree_estadisticas.get_children():
            self.tree_estadisticas.delete(it)

        session = None
        try:
            session = obtener_sesion()
            top = top_productos(session, limite=10)
            total = total_ventas(session)

            # `top` puede ser una lista de tuplas (nombre, cantidad)
            # o una lista de dicts
            for item in top:
                if isinstance(item, (tuple, list)):
                    nombre, qty = item[0], item[1]
                elif isinstance(item, dict):
                    nombre = item.get("nombre")
                    qty = item.get("ventas") or item.get("cantidad")
                else:
                    continue
                self.tree_estadisticas.insert("", "end", values=(nombre, qty))

            formatted_total = formatear_precio(total)
            self.label_total_ventas.configure(
                text=f"Total ventas: {formatted_total}"
            )
        finally:
            if session:
                try:
                    session.close()
                except Exception:
                    pass

    def validar_nombre(self, nombre):
        """Valida que `nombre` contenga solo letras y espacios.

        Permite caracteres Unicode.
        """
        if not nombre:
            CTkMessagebox(
                title="Error de Validación",
                message="El nombre no puede estar vacío.",
                icon="warning",
                sound=False,
            )
            return False

        # Aceptar letras Unicode y espacios
        if all((ch.isalpha() or ch.isspace()) for ch in nombre):
            return True

        CTkMessagebox(
            title="Error de Validación",
            message="El nombre debe contener sólo letras y espacios.",
            icon="warning",
            sound=False,
        )
        return False

    def validar_cantidad(self, cantidad):
        """Valida que `cantidad` sea un número positivo (entero o decimal)."""
        if not cantidad:
            CTkMessagebox(
                title="Error de Validación",
                message="La cantidad no puede estar vacía.",
                icon="warning",
                sound=False,
            )
            return False

        try:
            val = float(cantidad)
            if val < 0:
                raise ValueError("negativo")
            return True
        except Exception:
            CTkMessagebox(
                title="Error de Validación",
                message="La cantidad debe ser un número positivo (p. ej. 1 o 1.5).",
                icon="warning",
                sound=False,
            )
            return False

    @manejar_errores()
    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        try:
            cantidad_val = float(cantidad)
        except ValueError:
            CTkMessagebox(
                title="Error de Validación",
                message="La cantidad ingresada no es un número válido.",
                icon="warning",
                sound=False,
            )
            return

        unidad = "unid"
        ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad_val)
        self.stock.agregar_ingrediente(ingrediente)
        self.actualizar_treeview()

    @manejar_errores()
    def eliminar_ingrediente(self):
        selected_items = self.tree.selection()
        if not selected_items:
            CTkMessagebox(
                title="Error",
                message="Debe seleccionar un ingrediente para eliminar.",
                icon="warning",
                sound=False,
            )
            return

        for item in selected_items:
            values = self.tree.item(item, "values")
            nombre = values[0]
            try:
                self.stock.eliminar_ingrediente(nombre)
            except Exception as e:
                logger.exception("Error al eliminar ingrediente '%s': %s", nombre, e)

        self.actualizar_treeview()

        # Informar si algún menú queda indisponible
        for menu in self.menus:
            if not menu.esta_disponible(self.stock):
                logger.info(
                    "No hay suficientes ingredientes para el menú '%s'",
                    menu.nombre,
                )


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    # Desactiva el beep de todas las ventanas de alerta
    app.bell = lambda *args, **kwargs: None

    try:
        style = ttk.Style(app)
        style.theme_use("clam")
    except Exception:
        pass

    app.mainloop()
