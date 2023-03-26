from Abstractos.Abstracto import Abstracto


class Error(Abstracto):
    def __init__(self, lexema, tipo, fila, columna):
        self.lexema = lexema
        self.tipo = tipo
        super().__init__(fila, columna)

    def getValor(self, arbol):
        return self.lexema

    def getTipo(self):
        return self.tipo

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
