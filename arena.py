class Ator(object):

    def rect(self) -> tuple:
        return self._x, self._y, self.W, self.H

    def getStatus(self):
        pass

    def status(self, status: int):
        pass

    def comecar(self):
        pass

    def parar(self):
        pass

    def mover(self):
        pass

    def colidir(self, other):
        pass

    def simbolo(self):
        pass

class Arena(object):

    def __init__(self):
        pass

    def atores(self) -> list:
        return list(self._atores)

    def tamanho(self) -> tuple:
        return (self._w, self._h)

    def getVidas(self) -> int:
        return self._vidas


    def adicionar(self, a):
        if a not in self._atores: self._atores.append(a)

    def remover(self, a):
        if a in self._atores: self._atores.remove(a)

    def perderVida(self):
        self._vidas -= 1


    
    def moverTodos(self):
        for a in self.atores():
            ultimaPosicao = a.rect()
            a.mover()
            if a.rect() != ultimaPosicao:
                for other in reversed(self.atores()):
                    if other is not a and self.checarColisao(a, other):
                        a.colidir(other)
                        other.colidir(a)

    #verifica colisões
    def checarColisao(self, a1, a2) -> bool: 
        x1, y1, w1, h1 = a1.rect()
        x2, y2, w2, h2 = a2.rect()
        return (y2 < y1 + h1 and y1 < y2 + h2 and x2 < x1 + w1 and x1 < x2 + w2)
