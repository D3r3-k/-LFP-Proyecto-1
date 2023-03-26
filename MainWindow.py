import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from Analizador import *
from graficar import *

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # VARIABLES
        self.ruta = None
        self.contenido_archivo = ""
        self.background = "#333333"
        # VENTANA
        self.title(
            "Proyecto 1 | Laboratorio de Lenguajes Formales y de Programación")
        self.geometry("800x800")
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
        archivo_menu.add_command(label="Errores", command=self.errores)
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
        # SECCION IZQUIERDA
        left_frame = tk.Frame(self, padx=20, pady=20, width=400)
        left_frame.pack(side=tk.LEFT, fill="both")
        label = tk.Label(left_frame, text="Proyecto 1",
                         font=("Arial Bold", 14))
        label.pack()
        # BOTONES
        name_button = tk.Button(
            left_frame, text="Analizar", command=self.analizar)
        name_button.pack(pady=10)
        info_button = tk.Button(
            left_frame, text="Graficar", command=self.abrir_archivo)
        info_button.pack(pady=10)
        self.name_label = tk.Label(left_frame, text="", padx=20, pady=20)
        self.name_label.pack()

        # SECCION DERECHA
        right_frame = tk.Frame(self, padx=20, pady=20, width=400)
        right_frame.pack(side=tk.RIGHT, fill="both")

        ruta_label = tk.Label(right_frame, text="Ruta: ",
                              font=("Arial Bold", 12))
        ruta_label.pack()
        self.ruta_label_t = tk.Label(right_frame, text="", font=("Arial", 12))
        self.ruta_label_t.pack(anchor="center")
        # TEXTAREA
        self.text_area = tk.Text(right_frame, padx=10,
                                 pady=10, font=("Arial", 12), wrap='none', width=50)
        self.scroll_y = tk.Scrollbar(right_frame, command=self.text_area.yview)
        self.scroll_x = tk.Scrollbar(
            right_frame, command=self.text_area.xview, orient='horizontal')
        self.text_area.configure(
            yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(side='right', fill='y')
        self.scroll_x.pack(side='bottom', fill='x')
        self.text_area.pack(fill=tk.BOTH, expand=True, side='left')

    def actualizar_contenido(self):
        if self.contenido_archivo:
            self.contenido_archivo = self.text_area.get("1.0", tk.END)

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
        image = tk.PhotoImage(file="imgs/logo.png")
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

    def analizar(self):
        contenido = self.text_area.get('1.0', tk.END)
        analizar_caneda(contenido)
        lista = obtener_respuestas()
        graficar(lista)

    def errores(self):
        pass


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
