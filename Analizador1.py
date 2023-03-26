from Abstractos.Lexema import Lexema
from Abstractos.Numero import Numero
from Abstractos.Error import Error
from Operaciones.Aritmeticas import Aritmetica
from Operaciones.Trigonometricas import Trigonometricas
from Operaciones.Nodos import *

lexemas_reservados = {
    'Operacion',
    'Valor1',
    'Valor2',
    'Suma',
    'Resta',
    'Multiplicacion',
    'Division',
    'Potencia',
    'Raiz',
    'Inverso',
    'Seno',
    'Coseno',
    'Tangente',
    'Modulo',
    'Texto',
    'Color-Fondo-Nodo',
    'Color-Fuente-Nodo',
    ',',
    '.',
    ':',
    '[',
    ']',
    '{',
    '}',
}

global n_linea
global n_columna
global lista_operaciones
global lista_lexemas_temp
global lista_lexemas
global lista_errores
global lista_nodos  # EN DISCUSION XD

lista_operaciones = []
lista_lexemas_temp = []  # Analizar Caneda -> obtiene todos los lexemas
lista_lexemas = []  # Analizar Caneda -> obtiene todos los lexemas
lista_errores = []
lista_nodos = []
n_linea = 1
n_columna = 1


def analizar_caneda(cadena):
    global n_linea
    global n_columna
    global lista_lexemas_temp
    global lista_lexemas
    lexema = ''
    index = 0
    while cadena:
        char = cadena[index]
        index += 1
        if char == '\"':
            lexema, cadena = armar_lexema(cadena[index:])
            if lexema and cadena:
                n_columna += 1
                lex = Lexema(lexema, n_linea, n_columna)
                lista_lexemas_temp.append(lex)
                lista_lexemas.append(lex)
                n_columna += len(lexema)+1
                index = 0
        elif char.isdigit():
            token, cadena = armar_numero(cadena)
            if lexema and cadena:
                n_columna += 1
                lex_num = Numero(token, n_linea, n_columna)
                lista_lexemas_temp.append(lex_num)
                lista_lexemas.append(lex_num)
                n_columna += len(str(token))+1
                index = 0
        elif char == '[' or char == ']':
            lex = Lexema(char, n_linea, n_columna)
            lista_lexemas_temp.append(lex)
            lista_lexemas.append(lex)
            cadena = cadena[1:]
            index = 0
            n_columna += 1
        elif char == '\t':
            n_columna += 4
            cadena = cadena[4:]
            index = 0
        elif char == '\n':
            n_columna = 1
            n_linea += 1
            index = 0
            cadena = cadena[1:]
        else:
            cadena = cadena[1:]
            index = 0
            n_columna += 1
    return lista_lexemas_temp


def armar_lexema(cadena):
    lexema = ''
    index = ''
    for char in cadena:
        index += char
        if char == '\"':
            return lexema, cadena[len(index):]
        else:
            lexema += char
    return None, None


def armar_numero(cadena):
    numero = ''
    index = ''
    is_decimal = False
    for char in cadena:
        index += char
        if char == '.':
            is_decimal = True
        if char == '\"' or char == ' ' or char == '\t' or char == '\n':
            try:
                if is_decimal:
                    return float(numero), cadena[len(index)-1:]
                else:
                    return int(numero), cadena[len(index)-1:]
            except ValueError:
                return None, None
        else:
            numero += char
    return None, None


def realizar_operacion(es_hijo=False):
    global lista_lexemas_temp
    # OPERACIONES
    operacion = None
    valor1 = None
    valor2 = None
    respuesta = None
    # NODOS
    nodo_valor1 = None
    nodo_valor2 = None
    # TEXTOS
    texto = None
    color_fondo = None
    color_fuente = None
    forma = None
    while lista_lexemas_temp:
        lex = lista_lexemas_temp.pop(0)
        # OBTENER TIPO DE OPERACION
        if lex.getValor(None) == 'Operacion':
            operacion = lista_lexemas_temp.pop(0)

        # OBTENER VALOR 1
        elif lex.getValor(None) == 'Valor1':
            valor1 = lista_lexemas_temp.pop(0)
            if valor1.getValor(None) == '[':
                valor1, nodo = realizar_operacion(True)
                nodo_valor1 = nodo
        # OBTENER VALOR 2
        elif lex.getValor(None) == 'Valor2':
            valor2 = lista_lexemas_temp.pop(0)
            if valor2.getValor(None) == '[':
                valor2, nodo = realizar_operacion(True)
                nodo_valor2 = nodo
        # OBTENER TEXTOS PARA EL NODO
        elif lex.getValor(None) == 'Texto':
            texto = lista_lexemas_temp.pop(0)
        elif lex.getValor(None) == 'Color-Fondo-Nodo':
            color_fondo = lista_lexemas_temp.pop(0)
        elif lex.getValor(None) == 'Color-Fuente-Nodo':
            color_fuente = lista_lexemas_temp.pop(0)
        elif lex.getValor(None) == 'Forma-Nodo':
            forma = lista_lexemas_temp.pop(0)

        # RETORNAR LOS VALORES
        if operacion and valor1 and valor2:
            resultado = Aritmetica(operacion, valor1, valor2, nodo_valor1, nodo_valor2,
                                   f'{operacion.getFila()}:{operacion.getColumna()}', f'{valor2.getFila()}:{valor2.getColumna()}')
            nodo = Nodo_Aritmetico(
                operacion, valor1, valor2, nodo_valor1, nodo_valor2, resultado)
            if es_hijo:
                return resultado, nodo
            lista_nodos.append(nodo)
            return resultado, None
        elif operacion and valor1 and (operacion.getValor(None) == 'Seno' or operacion.getValor(None) == 'Coseno' or operacion.getValor(None) == 'Tangente' or operacion.getValor(None) == 'Inverso'):
            resultado = Trigonometricas(
                operacion, valor1, nodo_valor1, f'{operacion.getFila()}:{operacion.getColumna()}', f'{valor1.getFila()}:{valor1.getColumna()}')
            nodo = Nodo_Trigonometrico(
                operacion, valor1, nodo_valor1, resultado)
            if es_hijo:
                return resultado, nodo
            lista_nodos.append(nodo)
            return resultado, None
        elif texto and color_fondo and color_fuente and forma:
            nodo = Nodo_Texto(texto, color_fondo, color_fuente, forma)
            # lista_nodos.append(nodo)
            return None, None
    return None, None


def crear_nodo(operacion, valor1, valor2, nodo1, nodo2, respuesta):
    # Lógica para crear un nodo aritmético
    pass


def crear_nodo(operacion, valor1, nodo1, respuesta):
    # Lógica para crear un nodo trigonométrico
    pass


def obtener_respuestas():
    global lista_operaciones
    global lista_nodos
    lista_nodos = []
    lista_operaciones = []
    while True:
        operacion, nodo = realizar_operacion()
        if operacion:
            lista_operaciones.append(operacion)
        else:
            break

    indice = 0
    for nodo in lista_nodos:
        imprimir_nodo(nodo, indice)
        indice += 1


def imprimir_nodo(nodo, index):
    espa = "    "
    if isinstance(nodo, Nodo_Aritmetico):
            print(f"[{index}]Tipo: {nodo.getOperacion()}")
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                imprimir_nodo(nodo.getNodo_valor1(), index)
            else:
                print(f"{espa}Valor 1: {nodo.getValor1()}")
            if isinstance(nodo.getNodo_valor2(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor2(), Nodo_Trigonometrico):
                imprimir_nodo(nodo.getNodo_valor2(), index)
            else:
                print(f"{espa}Valor 2: {nodo.getValor2()}")
            print(f"{espa}Resultado: {nodo.getResultado()}")

    if isinstance(nodo, Nodo_Trigonometrico):
            print(f"[{index}]Tipo: {nodo.getOperacion()}")
            if isinstance(nodo.getNodo_valor1(), Nodo_Aritmetico) or isinstance(nodo.getNodo_valor1(), Nodo_Trigonometrico):
                imprimir_nodo(nodo.getNodo_valor1(), index)
            else:
                print(f"{espa}Valor 1: {nodo.getValor1()}")
            print(f"{espa}Resultado: {nodo.getResultado()}")


entrada = '''{
    {
        {
            "Operacion": "Tangente"
            "Valor1": [
                "Operacion": "Resta"
                "Valor1": 5
                "Valor2": [
                    "Operacion": "Suma"
                    "Valor1": 8
                    "Valor2": 3
                ]
            ]
        },
        {
            "Operacion": "Resta"
            "Valor1": 4.5
            "Valor2": [
                "Operacion": "Potencia"
                "Valor1": 10
                "Valor2": 3
            ]
        },
        {
            "Operacion": "Multiplicacion"
            "Valor1": [
                "Operacion": "Seno"
                "Valor1": 90
            ]
            "Valor2": 5.32
        }
        "Texto": "Realizacion de Operaciones"
        "Color-Fondo-Nodo": "Amarillo"
        "Color-Fuente-Nodo": "Rojo"
        "Forma-Nodo": "Circulo"
    }
    }
'''


# def analizar_errores(lexemas):
#     n_col = 0
#     lista_errores = []
#     for lexema in lexemas:
#         for lex in lexema.getValor(None):
#             error_encontra = False
#             indice = 0
#             for i in "Operacion"[indice]:
#                 if lex != i:
#                     indice += 1
#                     n_col += 1
#                     continue
#                 else:
#                     indice += 1
#                     error_encontra = True
#             if not error_encontra:
#                 lex_err = Error(lex, "Error", lexema.getFila(), lexema.getColumna()+n_col)
#                 lista_errores.append(lex_err)
#                 break
#     return lista_errores
