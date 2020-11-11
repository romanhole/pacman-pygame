# Felipe Pires Araujo - 19169
# Rafael Romanhole Borrozino - 19196

import pygame
from arena import *
from pacman import *
from pygame.locals import (KEYDOWN, K_RIGHT, K_d, K_LEFT, K_a, K_UP, K_w, K_DOWN, K_s, K_ESCAPE)

## constantes
FPS = 30
larguraTela, alturaTela = 232, 272

## inicializacao da arena e dos personagens
arena = PacmanArena(larguraTela, alturaTela)

## inicializacao do PacMan
pacman = PacMan(arena, 108, 184)

pygame.init()
clock = pygame.time.Clock()
tela = pygame.display.set_mode(arena.tamanho())
imgFundo = pygame.image.load('pacman_background.png')
sprites = pygame.image.load('pacman_sprites.png')

isJogando = True
pacman.direcao(-2, 0)
while isJogando:
    tela.fill((0, 0, 0))
    tela.blit(imgFundo, (0, 0))

    ## ciclo de evento externo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            isJogando = False
            esc = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (K_RIGHT, K_d): pacman.direcao(2, 0)
            elif evento.key in (K_LEFT, K_a): pacman.direcao(-2, 0)
            elif evento.key in (K_UP, K_w): pacman.direcao(0, -2)
            elif evento.key in (K_DOWN, K_s): pacman.direcao(0, 2)
            if evento.key == pygame.K_ESCAPE:
                isJogando = False
                esc = True
    arena.moverTodos()

    ## Exibe o vídeo dos personagens
    for a in arena.atores():
        if not isinstance(a, Parede) and not isinstance(a, Portao):
            x, y, w, h = a.rect()
            xs, ys = a.simbolo()
            tela.blit(sprites, (x, y), area = (xs, ys, w, h))

    ## Exibe o vídeo dos pontos
    font = pygame.font.SysFont('Courier', 14)
    msg = font.render(str(pacman.pontuacao), True, (255, 255, 255))
    tela.blit(msg, (6, 254))

    ## Ponto dos fantasmas comidos
    for s in reversed(pacman.pontuacao_sprite):
        tela.blit(sprites, s[0], area = (s[1]*16, 128, 16, 16))
        if s[2] == FPS*3: pacman.pontuacao_sprite.remove(s)
        else: s[2] += 1

    ## Ponto dos itens bonus
    for b in reversed(pacman.bonus_sprite):
        tela.blit(sprites, b[0], area = (b[1]*16, 144, 16, 16))
        if b[2] == FPS*3: pacman.bonus_sprite.remove(b)
        else: b[2] += 1

    ## Exibe o vídeo das vidas disponíveis
    for l in range(arena.getVidas()):
        tela.blit(sprites, (210 - l*16, 254), area = (128, 16, 16, 16))

    ## Exibe o texto na tela escrito "PRONTO"
    if pacman.getStatus() == -1 and arena.isJogando() == 0:
        msg = font.render("PRONTO!", True, (255, 255, 0))
        tela.blit(msg, (92, 136))

    ## Controle
    if arena.isJogando() != 0:
        if arena.isJogando() == 1:
            msg = font.render("VOCE VENCEU", True, (255, 255, 0))
            tela.blit(msg, (88, 136))
        elif arena.isJogando() == 2:
            msg = font.render("FIM DE JOGO", True, (255, 0, 0))
            tela.blit(msg, (80, 136))
        arena.sound(3).stop()
        isJogando = False
        esc = False
    pygame.display.flip()
    clock.tick(FPS)
if esc: pygame.quit()
