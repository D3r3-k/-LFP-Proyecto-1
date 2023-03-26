from Abstractos.Abstracto import Abstracto
from math import *


class Trigonometricas(Abstracto):
    def __init__(self, valor1, operacion, fila, columna):
        self.valor1 = valor1
        self.operacion = operacion
        super().__init__(fila, columna)

    def getValor(self, arbol):
        temp_val = ''
        # ASIGNAR VALORES
        if self.valor1 != None:
            temp_val = self.valor1.getValor(arbol)
        # OPERAR VALORES
        if self.operacion.getValor(arbol) == 'Seno':
            return sin(temp_val)
        elif self.operacion.getValor(arbol) == 'Coseno':
            return cos(temp_val)
        elif self.operacion.getValor(arbol) == 'Tangente':
            return tan(temp_val)
        elif self.operacion.getValor(arbol) == 'Inverso':
            return 1/temp_val
        else:
            return None

    def getOperacion(self, arbol):
        return self.operacion.getValor(arbol)

    def getValor1(self, arbol):
        return self.valor1.getValor(arbol)

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
