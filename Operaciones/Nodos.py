class Nodo_Texto():
    def __init__(self, texto, color_fondo, color_fuente, forma):
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_fuente = color_fuente
        self.forma = forma

    def getTexto(self):
        return self.texto.getValor(None)

    def getColorFondo(self):
        return self.color_fondo.getValor(None)

    def getColorFuente(self):
        return self.color_fuente.getValor(None)

    def getForma(self):
        return self.forma.getValor(None)


class Nodo_Aritmetico():
    def __init__(self, operacion, valor1, valor2, nodo_valor1, nodo_valor2, resultado):
        self.operacion = operacion
        self.valor1 = valor1
        self.valor2 = valor2
        self.nodo_valor1 = nodo_valor1
        self.nodo_valor2 = nodo_valor2
        self.resultado = resultado

    def getOperacion(self):
        return self.operacion.getValor(None)

    def getValor1(self):
        return self.valor1.getValor(None)

    def getValor2(self):
        return self.valor2.getValor(None)

    def getNodo_valor1(self):
        return self.nodo_valor1

    def getNodo_valor2(self):
        return self.nodo_valor2

    def getResultado(self):
        return self.resultado.getValor(None)


class Nodo_Trigonometrico():
    def __init__(self, operacion, valor1, nodo_valor1,  resultado):
        self.operacion = operacion
        self.valor1 = valor1
        self.nodo_valor1 = nodo_valor1
        self.resultado = resultado

    def getOperacion(self):
        return self.operacion.getValor(None)

    def getValor1(self):
        return self.valor1.getValor(None)

    def getNodo_valor1(self):
        return self.nodo_valor1

    def getResultado(self):
        return self.resultado.getValor(None)
