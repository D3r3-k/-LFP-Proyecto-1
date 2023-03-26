import os
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from Analizador import *


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # VARIABLES
        self.ruta = None
        self.ruta_grafica = None
        self.contenido_archivo = ""
        self.background = "#333333"
        self.lista_respuestas = []
        self.lista_errores = []
        # VARIABLES GRAFICA
        self.titulo = ''
        self.figura = ''
        self.color_fondo = ''
        self.color_fuente = ''
        # VENTANA
        self.title(
            "Proyecto 1 | Laboratorio de Lenguajes Formales y de Programación")
        self.geometry("1000x800")
        self.resizable(False, False)
        self.crear_menu()
        self.crear_widgets()
        # Centrar la ventana en la pantalla
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def crear_menu(self):
        menu_bar = tk.Menu(self)
        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        ayuda_menu = tk.Menu(menu_bar, tearoff=0)
        # MENU ARCHIVO
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar Como",
                                 command=self.guardar_archivo_como)
        archivo_menu.add_command(label="Analizar", command=self.analizar)
        archivo_menu.add_command(label="Errores", command=self.generar_errores)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit())
        # MENU AYUDA
        ayuda_menu.add_command(label="Manual de Usuario")
        ayuda_menu.add_command(label="Manual Técnico")
        ayuda_menu.add_separator()
        ayuda_menu.add_command(label="Temas de Ayuda",
                               command=self.mostrar_ventana_info)
        # OPCIONES MENU
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)
        self.config(menu=menu_bar)

    def crear_widgets(self):
        header_general = tk.Frame(self, padx=20, pady=20, bg=self.background)
        header_general.pack(side=tk.TOP, fill="both")
        label_titulo = tk.Label(header_general, text="Proyecto 1", font=(
            "Arial Bold", 16), bg=self.background, fg="white")
        label_titulo.pack()

        # SECCION IZQUIERDA
        right_frame = tk.Frame(self, padx=20, pady=20, width=450)
        right_frame.pack(side=tk.LEFT, fill="both")
        right_header = tk.Frame(right_frame)
        right_header.pack(side=tk.TOP, fill="both")

        ruta_label = tk.Label(right_header, text="Ruta: ",
                              font=("Arial Bold", 12))
        ruta_label.pack()
        self.ruta_label_t = tk.Label(right_header, text="", font=("Arial", 12))
        self.ruta_label_t.pack(anchor="center")
        btn_guardar = tk.Button(
            right_header, text="Graficar", command=self.graficar_resultados)
        btn_guardar.pack(side='left', pady=(10))
        # TEXTAREA
        self.text_area = tk.Text(right_frame, padx=10, pady=10, font=(
            "Arial", 12), wrap='none', width=50)
        self.scroll_y = tk.Scrollbar(right_frame, command=self.text_area.yview)
        self.scroll_x = tk.Scrollbar(
            right_frame, command=self.text_area.xview, orient='horizontal')
        self.text_area.configure(
            yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(side='right', fill='y')
        self.scroll_x.pack(side='bottom', fill='x')
        self.text_area.pack(fill=tk.BOTH, expand=True, side='left')

        # SECCION DERECHA
        left_frame = tk.Frame(self, padx=20, pady=20, width=400)
        left_frame.pack(side=tk.RIGHT, fill="both")
        left_header = tk.Frame(left_frame)
        left_header.pack(side=tk.TOP, fill="both")

        ruta_label = tk.Label(left_header, text="Errores",
                              font=("Arial Bold", 12))
        ruta_label.pack()
        btn_guardar = tk.Button(
            left_header, text="Guardar Errores", command=self.guardar_archivo_errores)
        btn_guardar.pack(side='right', pady=20)
        # TEXTAREA ERRORES
        self.text_area_err = tk.Text(left_frame, padx=10,
                                     pady=10, font=("Arial", 12), wrap='none', width=50)
        self.scroll_y_err = tk.Scrollbar(
            left_frame, command=self.text_area_err.yview)
        self.scroll_x_err = tk.Scrollbar(
            left_frame, command=self.text_area_err.xview, orient='horizontal')
        self.text_area_err.configure(
            yscrollcommand=self.scroll_y_err.set, xscrollcommand=self.scroll_x_err.set)
        self.scroll_y_err.pack(side='right', fill='y')
        self.scroll_x_err.pack(side='bottom', fill='x')
        self.text_area_err.pack(fill=tk.BOTH, expand=True, side='left')

    def ventana_info(self, nombre, carnet, seccion):
        info_window = tk.Toplevel(self)
        info_window.title("Información del Estudiante")
        info_window.geometry("600x300")

        # Centrar la ventana en la pantalla
        info_window.update_idletasks()
        w = info_window.winfo_width()
        h = info_window.winfo_height()
        x = (info_window.winfo_screenwidth() - w) // 2
        y = (info_window.winfo_screenheight() - h) // 2
        info_window.geometry(f"+{x}+{y}")

        name_label = tk.Label(
            info_window, text=f"Nombre: {nombre}", padx=10, pady=10, font=("Arial", 14))
        name_label.place(x=10, y=10)
        carnet_label = tk.Label(
            info_window, text=f"Carnet: {carnet}", padx=10, pady=10, font=("Arial", 14))
        carnet_label.place(x=10, y=50)
        seccion_label = tk.Label(
            info_window, text=f"Sección: {seccion}", padx=10, pady=10, font=("Arial", 14))
        seccion_label.place(x=10, y=90)
        image = tk.PhotoImage(file="./imgs/logo.png")
        img_scal = image.subsample(2, 2)
        image_label = tk.Label(info_window, image=img_scal)
        image_label.image = img_scal
        image_label.place(relx=1.0, rely=1.0, anchor=tk.SE,
                          width=150, height=150, x=-10, y=-10)

    def mostrar_ventana_info(self):
        self.ventana_info("Derek Francisco Orellana Ibáñez", "202001151", "B-")

    def abrir_archivo(self):
        self.ruta = fd.askopenfilename(title="Selecciona un archivo", filetypes=[
            ('Archivo Json', '*.json'),
            ('Archivo de Texto', '*.txt')])
        self.ruta_label_t.config(text=self.ruta)
        self.leerArchivo(self.ruta)

    def leerArchivo(self, ruta):
        self.contenido_archivo = ""
        self.text_area.delete("1.0", tk.END)

        archivo = open(ruta, 'r')
        lineas = archivo.readlines()
        for linea in lineas:
            self.contenido_archivo += linea
        archivo.close()
        self.text_area.insert(tk.END, self.contenido_archivo)

    def guardar_archivo(self):
        if self.ruta is not None:
            archivo = open(self.ruta, 'w')
            archivo.write(self.text_area.get('1.0', tk.END))
            archivo.close()
            mb.showinfo("Exito", "Archivo guardado exitosamente.")
        else:
            self.guardar_archivo_como()

    def guardar_archivo_como(self):
        nueva_ruta = fd.asksaveasfilename(defaultextension='.json', filetypes=[
            ('Archivo Json', '*.json'),
            ('Archivo de Texto', '*.txt')])
        if nueva_ruta:
            archivo = open(nueva_ruta, 'w')
            archivo.write(self.text_area.get('1.0', tk.END))
            self.ruta = nueva_ruta
            self.ruta_label_t.config(text=nueva_ruta)
            mb.showinfo(
                "Exito", f"El archivo se guardo correctamente en: \n{nueva_ruta}")

    def guardar_archivo_errores(self):
        nueva_ruta = fd.asksaveasfilename(defaultextension='.json', filetypes=[
            ('Archivo Json', '*.json'),
            ('Archivo de Texto', '*.txt')])
        if nueva_ruta:
            archivo = open(nueva_ruta, 'w')
            archivo.write(self.text_area_err.get('1.0', tk.END))
            mb.showinfo(
                "Exito", f"El archivo se guardo correctamente en: \n{nueva_ruta}")

    def analizar(self):
        self.lista_respuestas = []
        self.lista_errores = []
        contenido = self.text_area.get('1.0', tk.END)
        analizar_caneda(contenido)
        self.lista_respuestas, self.lista_errores = obtener_respuestas()

    def graficar_resultados(self):
        self.graficar(self.lista_respuestas)
        self.generar_errores()

    def graficar(self, lista_nodos):
        self.ruta_grafica = ''
        try:
            lista_colores = {
                'Rojo': 'red',
                'Verde': 'green',
                'Azul': 'blue',
                'Amarillo': 'yellow',
                'Naranja': 'orange',
                'Blanco': 'white',
                'Negro': 'black',
                'Gris': 'gray',
                'Morado': 'purple',
                'Cafe': 'brown',
                'Rosa': 'pink'
            }
            for nodo in lista_nodos:
                if isinstance(nodo, Nodo_Texto):
                    self.titulo = nodo.getTexto()
                    self.figura = "circle"
                    if nodo.getColorFondo() in lista_colores.values():
                        self.color_fondo = nodo.getColorFondo()
                    elif nodo.getColorFondo() in lista_colores.keys():
                        self.color_fondo = lista_colores[nodo.getColorFondo()]
                    else:
                        self.color_fondo = "#FFFFFF"
                    if nodo.getColorFuente() in lista_colores.values():
                        self.color_fuente = nodo.getColorFuente()
                    elif nodo.getColorFuente() in lista_colores.keys():
                        self.color_fuente = lista_colores[nodo.getColorFuente(
                        )]
                    else:
                        self.color_fuente = "#000"
                    break

            ruta = fd.asksaveasfilename(title="Guardar Frafica", filetypes=[(
                "PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")], defaultextension=".png")
            if ruta:
                nombre_archivo, extension = os.path.splitext(ruta)
                self.ruta_grafica = nombre_archivo + extension
                extension = extension.replace('.', '')
                archivo = f"{nombre_archivo}.dot"
                archivoDOT = open(archivo, "w")
                archivoDOT.write("digraph{\n")
                archivoDOT.write('label = "' + self.titulo+'";\n')
                archivoDOT.write('node [shape = ' + self.figura + '; fillcolor = '+self.color_fondo +
                                 '; width = 1; fixedsize = true; style = filled; color = black; fontsize = 10;];\n')
                archivoDOT.write('edge [color = "red";];\n')
                archivoDOT.close()

                for i, nodo in enumerate(lista_nodos):
                    self.imprimir_nodos(nodo, archivo, i)

                archivoDOT = open(archivo, "a")
                archivoDOT.write("\n\n")
                archivoDOT.close()

                for i, nodo in enumerate(lista_nodos):
                    self.enlazar_nodos(nodo, archivo, i)

                archivoDOT = open(archivo, "a")
                archivoDOT.write("}\n")
                archivoDOT.close()
                os.system(f'dot.exe -T{extension} "'+archivo +
                          '" -o "'+nombre_archivo+f'.{extension}"')
                os.remove(archivo)
                mb.showinfo("Exito", "Se ha generado el archivo en:\n"+ruta)
        except Exception as e:
            mb.showerror(
                "Error", "No se ha podido generar el archivo\n"+str(e))

    def imprimir_nodos(self, nodo, ruta, n_padre=0, hijo=''):
        archivoDOT = open(ruta, "a")
        nombre_padre = 'padre'+str(n_padre) + hijo
        if isinstance(nodo, Nodo_Aritmetico):
            archivoDOT.write('"'+nombre_padre+'"[label=<<font color="'+self.color_fuente+'">'+nodo.getOperacion(
            )+'</font><br/><font color="black">'+str(nodo.getResultado())+'</font>>, color=black]\n')
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                self.imprimir_nodos(nodo.getNodo_valor1(),
                                    ruta, n_padre, hijo+'_hijo1')
            else:
                archivoDOT.write(
                    '"'+nombre_padre+'_hijo1"[label="'+str(nodo.getValor1())+'";color=black]\n')
            if isinstance(nodo.getNodo_valor2(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor2(), Nodo_Trigonometrico):
                self.imprimir_nodos(nodo.getNodo_valor2(),
                                    ruta, n_padre, hijo+'_hijo2')
            else:
                archivoDOT.write(
                    '"'+nombre_padre+'_hijo2"[label="'+str(nodo.getValor2())+'";color=black]\n')
        elif isinstance(nodo, Nodo_Trigonometrico):
            archivoDOT.write('"'+nombre_padre+'"[label=<<font color="'+self.color_fuente+'">'+nodo.getOperacion(
            )+'</font><br/><font color="black">'+str(nodo.getResultado())+'</font>>, color=black]\n')
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                self.imprimir_nodos(nodo.getNodo_valor1(),
                                    ruta, n_padre, hijo+'_hijo1')
            else:
                archivoDOT.write(
                    '"'+nombre_padre+'_hijo1"[label="'+str(nodo.getValor1())+'";color=black]\n')
        else:
            pass
        archivoDOT.close()

    def enlazar_nodos(self, nodo, ruta, n_padre=0, hijo=''):
        archivoDOT = open(ruta, "a")
        nombre_padre = 'padre'+str(n_padre) + hijo
        if isinstance(nodo, Nodo_Aritmetico):
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                self.enlazar_nodos(nodo.getNodo_valor1(),
                                   ruta, n_padre, hijo+'_hijo1')
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo1"\n')
            else:
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo1"\n')
            if isinstance(nodo.getNodo_valor2(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor2(), Nodo_Trigonometrico):
                self.enlazar_nodos(nodo.getNodo_valor2(),
                                   ruta, n_padre, hijo+'_hijo2')
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo2"\n')
            else:
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo2"\n')
        elif isinstance(nodo, Nodo_Trigonometrico):
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                self.enlazar_nodos(nodo.getNodo_valor1(),
                                   ruta, n_padre, hijo+'_hijo1')
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo1"\n')
            else:
                archivoDOT.write('"'+nombre_padre+'"->"' +
                                 nombre_padre+'_hijo1"\n')
        else:
            pass
        archivoDOT.close()

    def generar_errores(self):
        self.text_area_err.delete(1.0, tk.END)
        cadena = "{\n"
        for i, r in enumerate(self.lista_errores):
            cadena += "    {\n"
            cadena += '       "Descripcion del Token": {\n'
            cadena += f'          "No": {i+1},\n'
            cadena += f'          "Lexema": \'{r.getValor(None)}\',\n'
            cadena += f'          "Tipo": {r.getTipo()},\n'
            cadena += f'          "Columna": {r.getColumna()},\n'
            cadena += f'          "Fila": {r.getFila()}\n'
            cadena += "       }\n"
            cadena += "    },\n"
        cadena += "}"
        self.text_area_err.insert(tk.END, cadena)
        pass

    # def errores(self):
    #     print(f">>---------------------<<")
    #     for r in lista_errores:
    #         print(f"Lexema: {r.getValor(None)}")
    #         print(f"Tipo: {r.getTipo()}")
    #         print(f"Fila: {r.getFila()}")
    #         print(f"Columna: {r.getColumna()}")
    #         print(f">>---------------------<<")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
