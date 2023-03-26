import os
from Operaciones.Nodos import *
import tkinter.messagebox as mb
import tkinter.filedialog as fd

global titulo
global figura
global color_fondo
global color_fuente
titulo = ''
figura = ''
color_fondo = ''
color_fuente = ''


def graficar(lista_nodos):
    global titulo
    global figura
    global color_fondo
    global color_fuente
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
                titulo = nodo.getTexto()
                figura = "circle"
                if nodo.getColorFondo() in lista_colores.values():
                    color_fondo = nodo.getColorFondo()
                elif nodo.getColorFondo() in lista_colores.keys():
                    color_fondo = lista_colores[nodo.getColorFondo()]
                else:
                    color_fondo = "#FFFFFF"
                if nodo.getColorFuente() in lista_colores.values():
                    color_fuente = nodo.getColorFuente()
                elif nodo.getColorFuente() in lista_colores.keys():
                    color_fuente = lista_colores[nodo.getColorFuente()]
                else:
                    color_fondo = "#000"
                break

        ruta = fd.asksaveasfilename(title="Guardar como", filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")], defaultextension=".png")
        nombre_archivo, extension = os.path.splitext(ruta)
        extension =extension.replace('.','')
        archivo = f"{nombre_archivo}.dot"
        archivoDOT = open(archivo, "w")
        archivoDOT.write("digraph{\n")
        archivoDOT.write('label = "' + titulo+'";\n')
        archivoDOT.write('node [shape = ' + figura + '; fillcolor = '+color_fondo +
                         '; width = 1; fixedsize = true; style = filled; color = black; fontsize = 10;];\n')
        archivoDOT.write('edge [color = "red";];\n')
        archivoDOT.close()

        for i, nodo in enumerate(lista_nodos):
            imprimir_nodos(nodo, archivo, i)

        archivoDOT = open(archivo, "a")
        archivoDOT.write("\n\n")
        archivoDOT.close()

        for i, nodo in enumerate(lista_nodos):
            enlazar_nodos(nodo, archivo, i)

        archivoDOT = open(archivo, "a")
        archivoDOT.write("}\n")
        archivoDOT.close()
        if ruta:
            os.system(f'dot.exe -T{extension} "'+archivo+'" -o "'+nombre_archivo+f'.{extension}"')
            os.remove(archivo)
            mb.showinfo("Exito", "Se ha generado el archivo en:\n"+ruta)
    except Exception as e:
        mb.showerror("Error", "No se ha podido generar el archivo\n"+str(e))


def imprimir_nodos(nodo, ruta, n_padre=0, hijo=''):
    archivoDOT = open(ruta, "a")
    global color_fuente
    nombre_padre = 'padre'+str(n_padre) + hijo
    if isinstance(nodo, Nodo_Aritmetico):
        archivoDOT.write('"'+nombre_padre+'"[label=<<font color="'+color_fuente+'">'+nodo.getOperacion()+'</font><br/><font color="black">'+str(nodo.getResultado())+'</font>>, color=black]\n')
        if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
            imprimir_nodos(nodo.getNodo_valor1(), ruta, n_padre, hijo+'_hijo1')
        else:
            archivoDOT.write(
                '"'+nombre_padre+'_hijo1"[label="'+str(nodo.getValor1())+'";color=black]\n')
        if isinstance(nodo.getNodo_valor2(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor2(), Nodo_Trigonometrico):
            imprimir_nodos(nodo.getNodo_valor2(), ruta, n_padre, hijo+'_hijo2')
        else:
            archivoDOT.write(
                '"'+nombre_padre+'_hijo2"[label="'+str(nodo.getValor2())+'";color=black]\n')
    elif isinstance(nodo, Nodo_Trigonometrico):
        archivoDOT.write('"'+nombre_padre+'"[label=<<font color="'+color_fuente+'">'+nodo.getOperacion()+'</font><br/><font color="black">'+str(nodo.getResultado())+'</font>>, color=black]\n')
        if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
            imprimir_nodos(nodo.getNodo_valor1(), ruta, n_padre, hijo+'_hijo1')
        else:
            archivoDOT.write(
                '"'+nombre_padre+'_hijo1"[label="'+str(nodo.getValor1())+'";color=black]\n')
    else:
        pass
    archivoDOT.close()


def enlazar_nodos(nodo, ruta, n_padre=0, hijo=''):
    archivoDOT = open(ruta, "a")
    global color_fuente
    nombre_padre = 'padre'+str(n_padre) + hijo
    if isinstance(nodo, Nodo_Aritmetico):
        if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
            enlazar_nodos(nodo.getNodo_valor1(), ruta, n_padre, hijo+'_hijo1')
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo1"\n')
        else:
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo1"\n')
        if isinstance(nodo.getNodo_valor2(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor2(), Nodo_Trigonometrico):
            enlazar_nodos(nodo.getNodo_valor2(), ruta, n_padre, hijo+'_hijo2')
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo2"\n')
        else:
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo2"\n')
    elif isinstance(nodo, Nodo_Trigonometrico):
        if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
            enlazar_nodos(nodo.getNodo_valor1(), ruta, n_padre, hijo+'_hijo1')
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo1"\n')
        else:
            archivoDOT.write('"'+nombre_padre+'"->"'+nombre_padre+'_hijo1"\n')
    else:
        pass
    archivoDOT.close()
