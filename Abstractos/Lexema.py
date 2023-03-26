from Abstractos.Abstracto import Abstracto


class Lexema(Abstracto):
    def __init__(self, lexema, fila, columna):
        self.lexema = lexema
        super().__init__(fila, columna)

    def getValor(self, arbol):
        return self.lexema

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
