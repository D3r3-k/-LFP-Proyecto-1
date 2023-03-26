from Abstractos.Abstracto import Abstracto


class Numero(Abstracto):
    def __init__(self, valor, fila, columna):
        self.valor = valor
        super().__init__(fila, columna)

    def getValor(self, arbol):
        return self.valor

    def setValor(self, valor):
        self.lexema = valor

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
