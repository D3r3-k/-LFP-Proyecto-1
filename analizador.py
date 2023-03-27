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
global lista_errores
global lista_nodos

lista_operaciones = []
lista_lexemas = []
lista_errores = []
lista_nodos = []


def analizar_caneda(cadena):
    global lista_errores
    global n_linea
    global n_columna
    lista_errores = []
    lexema = ''
    index = 0
    n_linea = 1
    n_columna = 1
    while cadena:
        char = cadena[index]
        index += 1
        if char == '\"':
            lexema, cadena = construir_lexema(cadena[index:])
            n_columna += 1
            if lexema and cadena:
                lex = Lexema(lexema, n_linea, n_columna)
                lista_lexemas.append(lex)
                n_columna += len(lexema)+1
                index = 0
        elif verificar_numero(char):
            token, cadena = construir_numero(cadena)
            if lexema and cadena:
                lex_num = Numero(token, n_linea, n_columna)
                lista_lexemas.append(lex_num)
                n_columna += len(str(token))+1
                index = 0
        elif char == '[' or char == ']':
            lex = Lexema(char, n_linea, n_columna)
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
        elif char == '{' or char == '}':
            n_columna += 1
            index = 0
            cadena = cadena[1:]
        elif char == ' ' or char == ':' or char == '.' or char == ',' or char == ',':
            n_columna += 1
            index = 0
            cadena = cadena[1:]
        else:
            nodo_err = Error(char, "Error", n_linea, n_columna)
            lista_errores.append(nodo_err)
            cadena = cadena[1:]
            index = 0
    return lista_lexemas

def verificar_numero(numero):
    numero = str(numero)
    try:
        int(numero)
        return True
    except ValueError:
        try:
            float(numero)
            return True
        except ValueError:
            return False

def construir_lexema(cadena):
    lexema = ''
    index = ''
    for char in cadena:
        index += char
        if char == '\"':
            return lexema, cadena[len(index):]
        else:
            lexema += char
    return None, None


def construir_numero(cadena):
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
    global lista_lexemas
    # OPERACIONES
    operacion = None
    valor1 = None
    valor2 = None
    # NODOS
    nodo_valor1 = None
    nodo_valor2 = None
    # TEXTOS
    texto = None
    color_fondo = None
    color_fuente = None
    forma = None
    while lista_lexemas:
        lex = lista_lexemas.pop(0)
        # OBTENER TIPO DE OPERACION
        if lex.getValor(None) == 'Operacion':
            operacion = lista_lexemas.pop(0)
            res = analizar_errores(operacion)
            operacion.setValor(res)
        # OBTENER VALOR 1
        elif lex.getValor(None) == 'Valor1':
            valor1 = lista_lexemas.pop(0)
            res = analizar_errores(valor1)
            valor1.setValor(res)
            if valor1.getValor(None) == '[':
                valor1, nodo = realizar_operacion(True)
                nodo_valor1 = nodo
        # OBTENER VALOR 2
        elif lex.getValor(None) == 'Valor2':
            valor2 = lista_lexemas.pop(0)
            res = analizar_errores(valor2)
            valor2.setValor(res)
            if valor2.getValor(None) == '[':
                valor2, nodo = realizar_operacion(True)
                nodo_valor2 = nodo
        # OBTENER TEXTOS PARA EL NODO
        elif lex.getValor(None) == 'Texto':
            texto = lista_lexemas.pop(0)
        elif lex.getValor(None) == 'Color-Fondo-Nodo':
            color_fondo = lista_lexemas.pop(0)
        elif lex.getValor(None) == 'Color-Fuente-Nodo':
            color_fuente = lista_lexemas.pop(0)
        elif lex.getValor(None) == 'Forma-Nodo':
            forma = lista_lexemas.pop(0)

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
            lista_nodos.append(nodo)
            return None, None
    return None, None


def obtener_respuestas():
    global lista_operaciones
    global lista_nodos
    global lista_errores
    lista_nodos = []
    lista_operaciones = []
    while True:
        operacion, nodo = realizar_operacion()
        if operacion:
            lista_operaciones.append(operacion)
        else:
            break
    return lista_nodos, lista_errores


def analizar_errores(palabra):
    for segunda_palabra in lexemas_reservados:
        n_col = 1
        armar_palabra = ''
        errores = []
        if not (isinstance(palabra.getValor(None), int) or isinstance(palabra.getValor(None), float) or isinstance(palabra.getValor(None), Numero)):
            for p in str(palabra.getValor(None)):
                for s in segunda_palabra:
                    if p == s:
                        armar_palabra += p
                        n_col += 1
                        break
                    else:
                        if p not in segunda_palabra:
                            n_err = {
                                'index': n_col,
                                'palabra': p,
                            }
                            if n_err not in errores and p not in segunda_palabra:
                                errores.append(n_err)
                        continue
            if segunda_palabra == armar_palabra:
                break
    for err in errores:
        nodo = Error(err['palabra'], "Error", palabra.getFila(),
                     palabra.getColumna()+err['index'])
        lista_errores.append(nodo)
    return armar_palabra

# print(f">>---------------------<<")
# for r in lista_errores:
#     print(f"Lexema: {r.getValor(None)}")
#     print(f"Tipo: {r.getTipo()}")
#     print(f"Fila: {r.getFila()}")
#     print(f"Columna: {r.getColumna()}")
#     print(f">>---------------------<<")
