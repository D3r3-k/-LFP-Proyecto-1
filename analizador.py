from extras.Instrucciones.aritmeticas import *
from extras.Instrucciones.trigonometricas import *
from extras.Abstract.lexema import *
from extras.Abstract.numero import *

reservados = {
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
global instrucciones
global lista_lexemas

global lista_nodos

lista_nodos = []
instrucciones = []
n_linea = 1
n_columna = 1
lista_lexemas = []


def instrucccion(cadena):
    global n_linea
    global n_columna
    global lista_lexema
    lexema = ''
    puntero = 0
    while cadena:
        char = cadena[puntero]
        puntero += 1
        if char == '\"':
            lexema, cadena = armar_lexema(cadena[puntero:])
            if lexema and cadena:
                n_columna += 1

                l = Lexema(lexema, n_linea, n_columna)

                lista_lexemas.append(l)
                n_columna += len(lexema)+1
                puntero = 0
        elif char.isdigit():
            token, cadena = armar_numero(cadena)
            if token and cadena:
                n_columna += 1

                n = Numero(token, n_linea, n_columna)

                lista_lexemas.append(n)
                n_columna += len(str(token))+1
        elif char == '[' or char == ']':

            c = Lexema(char, n_linea, n_columna)

            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1
        elif char == '\t':
            n_columna += 4
            cadena = cadena[4:]
            puntero = 0
        elif char == '\n':
            cadena = cadena[1:]
            puntero = 0
            n_linea += 1
            n_columna = 1
        else:
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1
    return lista_lexemas


def operar():
    global lista_lexemas
    global instruccciones
    operacion = ''
    n1 = ''
    n2 = ''
    nodo_temp = {
        'Tipo': None,
        'N1': None,
        'N2': None,
        'Res': None
    }
    while lista_lexemas:
        lexema = lista_lexemas.pop(0)
        if lexema.operar(None) == 'Operacion':
            operacion = lista_lexemas.pop(0)
            if nodo_temp['Tipo'] == None:
                nodo_temp['Tipo'] = operacion.operar(None)
        elif lexema.operar(None) == 'Valor1':
            n1 = lista_lexemas.pop(0)
            nodo_temp['N1'] = n1
            if n1.operar(None) == '[':
                n1 = operar()
                nodo_temp['N1'] = nodo_temp
        elif lexema.operar(None) == 'Valor2':
            n2 = lista_lexemas.pop(0)
            nodo_temp['N2'] = n2
            if n2.operar(None) == '[':
                n2 = operar()
                nodo_temp['N2'] = nodo_temp
        elif lexema.operar(None) == 'Texto':
            operacion = lista_lexemas.pop(0)

        if operacion and n1 and n2:
            lista_nodos.append(nodo_temp)
            return Aritmetica(n1, n2, operacion, f'Inicio: {operacion.getFila()}:{operacion.getColumna()}', f'Fin: {n2.getFila()}:{n2.getColumna()}')
        elif operacion and n1 and (operacion.operar(None) == 'Seno' or operacion.operar(None) == 'Coseno' or operacion.operar(None) == 'Tangente'):
            lista_nodos.append(nodo_temp)
            return Trigonometricas(n1, operacion, f'Inicio: {operacion.getFila()}:{operacion.getColumna()}', f'Fin: {n1.getFila()}:{n1.getColumna()}')
        # elif texto and color and fuente and forma:
        #     pass
    return None


def operar_():
    global instrucciones
    while True:
        operacion = operar()
        if operacion:
            instrucciones.append(operacion)
        else:
            break
    return instrucciones


def armar_lexema(cadena):
    global n_linea
    global n_columna
    global lista_lexema
    lexema = ''
    puntero = ''
    for char in cadena:
        puntero += char
        if char == '\"':
            return lexema, cadena[len(puntero):]
        else:
            lexema += char
    return None, None


def armar_numero(cadena):
    numero = ''
    puntero = ''
    is_decimal = False
    for char in cadena:
        puntero += char
        if char == '.':
            is_decimal = True
        if char == '\"' or char == ' ' or char == '\t' or char == '\n':
            try:
                if is_decimal:
                    return float(numero), cadena[len(puntero)-1:]
                else:
                    return int(numero), cadena[len(puntero)-1:]
            except ValueError:
                return None, None
        else:
            numero += char
    return None, None
