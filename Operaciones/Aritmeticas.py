from Abstractos.Abstracto import Abstracto


class N(Abstracto):
    def __init__(self, operacion, valor1, valor2, nodo_valor1, nodo_valor2, fila, columna):
        self.valor1 = valor1
        self.valor2 = valor2
        self.nodo_valor1 = nodo_valor1
        self.nodo_valor2 = nodo_valor2
        self.operacion = operacion
        super().__init__(fila, columna)

    def getValor(self, arbol):
        temp_val1 = ''
        temp_val2 = ''
        # ASIGNAR VALORES
        if self.valor1 != None:
            temp_val1 = self.valor1.getValor(arbol)
        if self.valor2 != None:
            temp_val2 = self.valor2.getValor(arbol)
        # OPERAR VALORES
        if self.operacion.getValor(arbol) == 'Suma':
            return round(temp_val1 + temp_val2, 4)
        elif self.operacion.getValor(arbol) == 'Resta':
            return round(temp_val1 - temp_val2, 4)
        elif self.operacion.getValor(arbol) == 'Multiplicacion':
            return round(temp_val1 * temp_val2, 4)
        elif self.operacion.getValor(arbol) == 'Division':
            try:
                return round(temp_val1 / temp_val2, 4)
            except ArithmeticError:
                return 0
        elif self.operacion.getValor(arbol) == 'Potencia':
            return round(temp_val1 ** temp_val2, 4)
        elif self.operacion.getValor(arbol) == 'Raiz':
            return round(temp_val1 ** (1 / temp_val2), 4)
        else:
            return None

    def getNodo_valor1(self):
        return self.nodo_valor1

    def getNodo_valor2(self):
        return self.nodo_valor2

    def getOperacion(self, arbol):
        return self.operacion.getValor(arbol)

    def getValor1(self, arbol):
        return self.valor1.getValor(arbol)

    def getValor2(self, arbol):
        return self.valor2.getValor(arbol)

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
