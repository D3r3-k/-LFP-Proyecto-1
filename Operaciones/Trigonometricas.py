from Abstractos.Abstracto import Abstracto
from math import *


class Trigonometricas(Abstracto):
    def __init__(self, operacion, valor1, nodo_valor1, fila, columna):
        self.valor1 = valor1
        self.operacion = operacion
        self.nodo_valor1 = nodo_valor1
        super().__init__(fila, columna)

    def getValor(self, arbol):
        temp_val = ''
        # ASIGNAR VALORES
        if self.valor1 != None:
            temp_val = self.valor1.getValor(arbol)
        # OPERAR VALORES
        if self.operacion.getValor(arbol) == 'Seno':
            return round(sin(temp_val), 4)
        elif self.operacion.getValor(arbol) == 'Coseno':
            return round(cos(temp_val), 4)
        elif self.operacion.getValor(arbol) == 'Tangente':
            return round(tan(temp_val), 4)
        elif self.operacion.getValor(arbol) == 'Inverso':
            return round(1 / temp_val, 4)
        else:
            return None

    def getOperacion(self, arbol):
        return self.operacion.getValor(arbol)

    def getValor1(self, arbol):
        return self.valor1.getValor(arbol)

    def getNodo_valor1(self):
        return self.nodo_valor1

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
