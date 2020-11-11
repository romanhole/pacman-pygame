from arena import *
from pacman_map import *
import random
import pygame
pygame.init() 

## constante
FPS = 30

class PacmanArena(Arena):

    ## instancia e define valor
    def __init__(self, width: int, height: int):
        self._w, self._h = width, height
        self._vidas = 2 # Vidas; você perde em -1
        self._atores = []
        ## inicializa personagens
        for x, y, w, h in posicaoParedes: Parede(self, x, y, w, h)
        for x, y in posicaoBiscoitos: Biscoito(self, x, y)
        for x, y in posicaoPoderes: Poder(self, x, y)
        Fantasma(self, 108, 88, 0)
        Fantasma(self, 108, 112, 1)
        Fantasma(self, 124, 112, 2)
        Fantasma(self, 92, 112, 3)
        Bonus(self)
        Portao(self)
        ## adiciona sons num vetor de sons
        self._sounds = [pygame.mixer.Sound('sound/OpeningSong.wav'),
                        pygame.mixer.Sound('sound/Dies.wav'),
                        pygame.mixer.Sound('sound/WakaWaka.wav'),
                        pygame.mixer.Sound('sound/Siren.wav'),
                        pygame.mixer.Sound('sound/EatingCherry.wav'),
                        pygame.mixer.Sound('sound/EatingGhost.wav'),
                        pygame.mixer.Sound('sound/ExtraLive.wav')]
        self.sound(0).play()

    def isJogando(self) -> bool:
        result = 1
        ## condição de vitória
        for a in self._atores:
            if isinstance(a, Biscoito) or isinstance(a, Poder):
                result = 0
        ## condição de derrota
        if self._vidas == -1: result = 2
        return result # 0 -> continua a jogar, 1 -> você ganhou, 2 -> você perdeu

    ## retorna som de acordo com o paremetro
    def sound(self, i:int):
        return self._sounds[i]

    def rect_in_Parede(self, ator: Ator, rect: (int, int, int, int)) -> bool:
        for outroAtor in self._atores:
            if isinstance(outroAtor, Parede) or (isinstance(outroAtor, Portao) and not ator.getPortao()):
                x1, y1, w1, h1 = rect
                x2, y2, w2, h2 = outroAtor.rect()
                if (y2 < y1 + h1 and y1 < y2 + h2 and x2 < x1 + w1 and x1 < x2 + w2):
                    return True
        return False

    def indoParaParede(self, ator: Ator, dx: int, dy: int) -> bool:
        x, y, w, h = ator.rect()
        return self.rect_in_Parede(ator, (x + dx, y + dy, w, h))


class Parede(Ator):

    ## instancia classe
    def __init__(self, arena, x:int, y:int, w:int, h:int):
        self._x, self._y = x, y
        self._w, self._h = w, h
        arena.adicionar(self)

    def rect(self) -> tuple:
        return self._x, self._y, self._w, self._h

class Bonus(Ator):

    ## instancia classe
    def __init__(self, arena):
        self._arena = arena
        self._simbolo = -1
        self._w = 16
        self._h = 16
        self._status = 1
        self._counter = 0
        self.set_pos()
        self._arena.adicionar(self)
        
    def set_pos(self):
    ## Gera a posição do bonus
        self._x = random.randint(1,14)*8
        self._y = random.randint(1,14)*8
        while self._arena.rect_in_Parede(self, self.rect()) or (92 <= self._x <= 139 and 108 <= self._y <= 131):
            self._x = random.randint(1,14)*16
            self._y = random.randint(1,14)*16

    def status(self,status):
    ## STATUS
    ## 0 -> visivel
    ## 1 -> comido por PacMan
    ## 2 -> todos os bônus já comidos, não visíveis

        if status == 1: self._symbol = -1
        elif status == 0:
            if self._simbolo < 7: self._simbolo += 1
            elif self._simbolo == 7: status = 2
        self._counter = 0
        self.set_pos()
        self._status = status

    def simbolo(self) -> tuple:
        if self._status == 1:
            self._counter += 1 
            if self._counter == FPS*10: self.status(0)
            return (48, 192)
        elif self._status == 0: return (32 + (16 * self._simbolo), 48)
        else: return (48, 192)

    def getNumber(self) -> int:
        return self._simbolo
    
    def getPortao(self)-> bool:
        return False

    def getStatus(self) -> int:
        return self._status
        
    def rect(self) -> tuple:
        return self._x, self._y, self._w, self._h
    

class Portao(Ator):

    ## instancia classe
    def __init__(self, arena):
        self._x, self._y = 108, 104
        self._w, self._h = 16, 8
        arena.adicionar(self)

    def rect(self) -> tuple:
        return self._x, self._y, self._w, self._h


class Biscoito(Ator):
    W, H = 4, 4

    ## instancia classe
    def __init__(self, arena, x:int, y:int):
        self._x, self._y = x, y
        self._arena = arena
        self._arena.adicionar(self)

    def simbolo(self):
        return 166, 54
    
    ## colisão Biscoito
    def collide(self, other):
        if isinstance(other, PacMan):
            x, y, w, h = other.rect()
            if (self._y == y + 6 and y == self._y - 6 and self._x == x + 6 and x == self._x - 6):
                outroAtor.pontuacao += 10
                self._arena.sound(2).parar()
                self._arena.sound(2).play()
                self._arena.remove(self)


class Poder(Ator):
    W, H = 8, 8

    ## instancia classe
    def __init__(self, arena, x:int, y:int):
        self._x, self._y = x, y
        self._arena = arena
        self._arena.adicionar(self)
        self._counter = 0

    def simbolo(self):
        if self._counter < 5:
            self._counter += 1
            return 180, 52
        elif 5 <= self._counter <= 9:
            self._counter += 1
            if self._counter == 10: self._counter = 0
            return 180, 16
    
    def colidir(self, outroAtor):
        if isinstance(outroAtor, PacMan):
            x, y, w, h = outroAtor.rect()
            if (self._y == y + 4 and y == self._y - 4 and self._x == x + 4 and x == self._x - 4):
                outroAtor.pontuacao += 50
                self._arena.sound(6).play()
                self._arena.remove(self)
                for a in self._arena.atores():
                    if isinstance(a, Fantasma) and a.getStatus() != 4 and a.getStatus() != 5:
                        a.status(2)          

class Fantasma(Ator):
    W, H = 16, 16

    ## instancia classe
    def __init__(self, arena, x:int, y:int, color:int):
        self._comecar_x, self._comecar_y = x, y
        self._color = color
        self._velocidade = 0
        self._dir = [0, 0]
        self._status = 0
        self.status(-1)
        self._arena = arena
        self._arena.adicionar(self)
        self._behav = random.randint(0, 1)
        self._behav_count = random.randint(0, 50)
        self._Portao = False # Quando True, o fantasma pode passar pelo portão

    def getStatus(self) -> int:
        return self._status

    def getPortao(self) -> bool:
        return self._Portao

    def status(self, status: int):
        ## STATUS:
        ## -1 -> inicialização
        ## 0 -> normal
        ## 1 -> Pac-Man perde vida
        ## 2 -> Poder Pac-Man
        ## 3 -> Poder Pac-Man em conclusão
        ## 4 -> comido por Pac-Man durante 2/3 do estado
        if status == -1: self.pos_init()
        elif status == 0:
            if self._status == 3: self.normal()
            else: self.comecar()
        elif status == 1: self.parar()
        elif status == 2: self.fugir()
        elif status == 4: self.comido()
        self._status = status
        self._counter = 0

    def pos_init(self): # A posição do fantasma é redefinida para sua posição inicial
        self._x, self._y = self._comecar_x, self._comecar_y
        self._sprite = [64, 64 + self._color*16]

    def comecar(self): # O fantasma começa a se mover
        self._velocidade = 2
        self._dir = [0, -2]
        self._sprite = [64, 64 + self._color*16]

    def normal(self): # O fantasma retorna à velocidade normal
        self._velocidade = 2
        if self._y == 112 and 92 <= self._x <= 128: self._Portao = True # Se ele estiver dentro do recinto inicial, ele deve ser capaz de sair
        if (self._dir[0] != 0 and self._x % 2 == 0) or (self._dir[1] != 0 and self._y % 2 == 0):
            self._dir = [self._dir[0]*2, self._dir[1]*2]
        else:
            self._x += self._dir[0]
            self._y += self._dir[1]
            self._dir = [self._dir[0]*2, self._dir[1]*2]
        self._sprite = [0, 64 + self._color*16]

    def comecar(self): # O fantasma para
        self._velocidade = 0
        self._dir = [0, 0]

    def fugir(self): # O fantasma reverte, fica azul e fica mais lento
        self._velocidade = 1
        if self._dir[0] != 0: self._dir[0] = -self._dir[0]/abs(self._dir[0])
        else: self._dir[1] = -self._dir[1]/abs(self._dir[1])
        self._sprite = [144, 64]

    def comido(self): # O fantasma se torna os "olhinhos" e aumenta sua velocidade
        self._velocidade = 4
        self._Portao = True
        if (self._dir[0] != 0 and self._x % 4 == 0) or (self._dir[1] != 0 and self._y % 4 == 0):
            self._dir = [self._dir[0]*4, self._dir[1]*4]
        else:
            self._x += 4 - self._x % 4
            self._y += 4 - self._y % 4
            self._dir = [self._dir[0]*4, self._dir[1]*4]
        self._sprite = [128, 80]

    def move(self):
        Arena_W, Arena_H = self._arena.size()
        angles = ((0,0),(232,0),(0,232),(232,232))
        ## Controle dos limites da arena
        if self._x < self._velocidade - self.W: self._x = Arena_W - self._velocidade
        elif self._x > Arena_W - self._velocidade: self._x = self._velocidade - self.W
        ## Criação da lista de apenas direções possíveis
        dirs = []
        if not self._arena.indoParaParede(self, self._dir[0], self._dir[1]): dirs.append(self._dir)
        if self._dir[0] == 0:
            if not self._arena.indoParaParede(self, self._velocidade, 0): dirs.append([self._velocidade,0])
            if not self._arena.indoParaParede(self, -self._velocidade, 0): dirs.append([-self._velocidade, 0])
        else:
            if not self._arena.indoParaParede(self, 0, self._velocidade): dirs.append([0, self._velocidade])
            if not self._arena.indoParaParede(self, 0, -self._velocidade): dirs.append([0, -self._velocidade])

        ## O fantasma só se adapta se não puder fazer mais nada
        if len(dirs) == 0: self._dir = [-self._dir[0], -self._dir[1]]
        ## Modo assustado (movimentos aleatórios)
        elif self._status in [2, 3]: self._dir = random.choice(dirs)
        else:
            ## Seleção de alvo (xt, yt)
            if self._Portao and self._status != 4: # O fantasma sai do recinto inicial para entrar no jogo
                xt, yt = 108, 88
                if self._x == xt and self._y == yt:
                    self.status(0)
                    self._Portao = False
            elif self._status == 4: # O fantasma retorna ao recinto inicial quando comido por PacMan
                xt,yt = 108, 112
                if self._x == xt and self._y == yt:
                    self.status(0)
                    self._Portao = True
            elif self._behav == 0: # Modo de dispersão (patrulha de canto)
                xt,yt = angles[self._color]
                if self._behav_count == FPS*7:
                    self._behav_count = 0
                    self._behav = 1
                else: self._behav_count += 1
            elif self._behav == 1: # Modo de perseguição (perseguição Pac-Man)
                for a in self._arena.atores():
                    if isinstance(a, PacMan):
                        xt, yt, w, h = a.rect()
                if self._behav_count == FPS*7:
                    self._behav_count = 0
                    self._behav = 0
                else: self._behav_count += 1

            if len(dirs) == 1: self._dir = dirs[0]
            else: # Cálculo da distância mais curta para alcançar a meta
                x, y = self._x, self._y
                distancias = []
                for i in range(len(dirs)):
                    dist = ((x + dirs[i][0]*8 - xt)**2 + (y + dirs[i][1]*8 - yt)**2)**(1/2)
                    distancias.append(dist)
                dist_min = distancias[0]
                dir_min = 0
                for i in range(len(dirs)):
                    if distancias[i] < dist_min:
                        dist_min = distancias[i]
                        dir_min = i
                self._dir = dirs[dir_min]
        ## Por fim, o movimento é realizado
        self._x += self._dir[0]
        self._y += self._dir[1]

    def simbolo(self):
        # Status -1
        if self._status == -1:
            if self._counter % 3 == 0:
                if self._sprite[0] == 64: self._sprite[0] = 80
                else: self._sprite[0] = 64
            if self._counter == 5*FPS:
                if self._color == 0: self.status(0)
                else: self.comecar()
            if self._counter == 5*FPS + 90*self._color:
                if self._color != 0: self._Portao = True
            self._counter += 1
        ## Status 0
        elif self._status == 0 and self._counter == 3:
            if self._dir == [self._velocidade,0]:
                if self._sprite[0] == 0: self._sprite[0] = 16
                else: self._sprite[0] = 0
            elif self._dir == [-self._velocidade,0]:
                if self._sprite[0] == 32: self._sprite[0] = 48
                else: self._sprite[0] = 32
            elif self._dir == [0,-self._velocidade]:
                if self._sprite[0] == 64: self._sprite[0] = 80
                else: self._sprite[0] = 64
            elif self._dir == [0,self._velocidade]:
                if self._sprite[0] == 96: self._sprite[0] = 112
                else: self._sprite[0] = 96
            self._counter = 0
        ## Status 1
        elif self._status == 1:
            if self._counter == FPS: self._sprite = [96, 128]
            elif self._counter == FPS*3:
                self.status(-1)
                return [96, 128]
            self._counter += 1
        ## Status 2
        elif self._status == 2 and self._counter % 3 == 0:
            if self._sprite[0] == 128: self._sprite[0] = 144
            elif self._sprite[0] == 144: self._sprite[0] = 128
            self._counter += 1
        elif self._status == 2 and self._counter >= FPS*6:
            self.status(3)
        ## Status 3
        elif self._status == 3 and  self._counter % 3 == 0:
            if self._sprite[0] == 128: self._sprite[0] = 144
            elif self._sprite[0] == 144: self._sprite[0] = 160
            elif self._sprite[0] == 160: self._sprite[0] = 176
            elif self._sprite[0] == 176: self._sprite[0] = 128
            self._counter += 1
        elif self._status == 3 and self._counter >= FPS*3:
            self.status(0)
        ## Status 4
        elif self._status == 4:
            if self._dir == [self._velocidade,0]: self._sprite[0] = 128
            elif self._dir == [-self._velocidade,0]: self._sprite[0] = 144
            elif self._dir == [0,-self._velocidade]:  self._sprite[0] = 160
            elif self._dir == [0,self._velocidade]: self._sprite[0] = 176
            self._counter = 0
        else: self._counter += 1
        return self._sprite[0], self._sprite[1]
        

class PacMan(Ator):
    W, H = 16, 16

    ## instancia classe
    def __init__(self, arena, x:int, y:int):
        self._x, self._y = x, y
        self.status(-1)
        self._arena = arena
        self._arena.adicionar(self)
        self.pontuacao = 0 # Ponto
        self.pontuacao_sprite = []
        self.bonus_sprite = []
        self._bonus = [100, 300, 500, 700, 1000, 2000, 3000, 5000] #valor do bonus
        self._Portao = False

    def direcao(self, next_dx:int, next_dy:int):
        self._next_dir = (next_dx, next_dy)

    def getStatus(self) -> int:
        return self._status

    def getPortao(self) -> bool:
        return self._Portao

    def status(self, status: int):
        ## STATUS:
        ## -1 -> inicialização
        ## 0 -> normal
        ## 1 -> Pac-Man perde vida
        if status == -1: self.pos_init()
        elif status == 0: self.comecar()
        elif status == 1: self.parar()
        self._status = status
        self._counter = 0

    def pos_init(self): # A posição do PacMan é redefinida para sua posição inicial
        self._x, self._y = 108, 184
        self._sprite = (16, 16)

    def comecar(self): # PacMan começa a se mover
        self.pos_init()
        self._dir = (-2, 0)
        self._next_dir = (-2, 0)

    def parar(self): # PacMan para
        self._arena.sound(3).parar()
        self._dir = (0,0)
        self._next_dir = (0,0)
        self._sprite = (16, self._sprite[1])

    def colidir(self, outroAtor):
        if isinstance(outroAtor, Parede):
            self._x -= self._dir[0]
            self._y -= self._dir[1]
            if self._dir == (2,0): self._sprite = (16,0)
            elif self._dir == (-2,0): self._sprite = (16,16)
            elif self._dir == (0,-2): self._sprite = (16,32)
            elif self._dir == (0,2): self._sprite = (16,48)
            self._dir = (0, 0)
        elif isinstance(outroAtor, Fantasma):
            x, y, w, h = outroAtor.rect()
            if (y < self._y + self.H//2 and self._y < y + h//2 and x < self._x + self.W//2 and self._x < x + w//2):
                if outroAtor.getStatus() == 0:
                    for a in self._arena.atores(): a.status(1)
                elif outroAtor.getStatus() == 2 or outroAtor.getStatus() == 3:
                    self._arena.sound(5).play()
                    ## Cálculo de pontos de bônus
                    num = 0 # Número de fantasmas já comidos
                    for a in self._arena.actors():
                        if isinstance(a, Fantasma) and a.getStatus() in [0,4]: num += 1
                    if other.getStatus() == 3: num += 1
                    score = 100 * (2**(num + 1))
                    self.pontuacao_sprite.append([(x, y), num, 0])
                    self.pontuacao += score
                    outroAtor.status(4)
        elif isinstance(outroAtor, Bonus) and outroAtor.getStatus() == 0:
            x, y, w, h = outroAtor.rect()
            if (y < self._y + self.H//2 and self._y < y + h//2 and x < self._x + self.W//2 and self._x < x + w//2):
                outroAtor.status(-1)
                n = outroAtor.getNumber()
                self._arena.sound(4).play()
                self.bonus_sprite.append([(x, y), n, 0 ])
                self.pontuacao += self._bonus[n]
            
    def move(self):
        Arena_W, Arena_H = self._arena.size()
        if self._status == 0:
            ## Controle dos limites da arena
            if self._x < 2 - self.W: self._x = Arena_W - 2
            elif self._x > Arena_W - 2: self._x = 2 - self.W
            ## Substituindo dir por next_dir se possível
            if self._dir != self._next_dir and not self._arena.going_to_Parede(self, self._next_dir[0], self._next_dir[1]):
                self._dir = self._next_dir
            self._x += self._dir[0]
            self._y += self._dir[1]

    def simbolo(self):
        ## Status -1
        if self._status == -1:
            if self._counter == FPS*5:
                self._arena.sound(3).play(-1)
                self.status(0)
            self._counter += 1
        ## Status 0
        elif self._status == 0 and self._counter == 2:
            if self._dir == (2,0):
                if self._sprite == (0,0): self._sprite = (16,0)
                elif self._sprite == (16,0): self._sprite = (32,0)
                else: self._sprite = (0,0)
            elif self._dir == (-2,0):
                if self._sprite == (0,16): self._sprite = (16,16)
                elif self._sprite == (16,16): self._sprite = (32,0)
                else: self._sprite = (0,16)
            elif self._dir == (0,-2):
                if self._sprite == (0,32): self._sprite = (16,32)
                elif self._sprite == (16,32): self._sprite = (32,0)
                else: self._sprite = (0,32)
            elif self._dir == (0,2):
                if self._sprite == (0,48): self._sprite = (16,48)
                elif self._sprite == (16,48): self._sprite = (32,0)
                else: self._sprite = (0,48)
            self._counter = 0
        ## Status 1
        elif self._status == 1:
            if self._counter == FPS:
                self._arena.sound(1).play()
                self._sprite = (48, 0)
            elif FPS < self._counter < FPS*3:
                if self._counter % 5 == 0: self._sprite = (self._sprite[0] + 16, 0)
            elif self._counter == FPS*3:
                self._arena.perderVida()
                self.status(-1)
                return (180, 16)
            self._counter += 1
        else: self._counter += 1
        return self._sprite
