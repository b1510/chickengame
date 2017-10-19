#!/usr/bin/python
# coding: utf-8
#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://tom.acrewoods.net/projects/pong
#
# Released under the GNU General Public License

VERSION = "0.4"

import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *



def load_png(name):
    """Charge une image et retourne un objet image"""
    fullname = os.path.join('data', name)

    image = pygame.image.load(name)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    """Une balle qui se déplace sur lécran
    Retourne: objet ball
    Fonctions: update, calcnewpos
    Attributs: area, vector"""

    def __init__(self, xy, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(r"C:\Users\Anthony\PycharmProjects\chickengame\src\images\ball.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0


    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector


        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            if tl and bl:
                # self.offcourt()
                angle = math.pi - angle
            if tr and br:
                angle = math.pi - angle
        # self.offcourt()
        else:
            # Réduire les rectangles pour ne pas frapper la balle derrière les raquettes
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)
            # Est-ce que la raquette et la balle entre en collision ?
            # Notez que je mets dans une règle à part qui définit self.hit à 1 quand ils entrent en collision
            # et à 0 à la prochaine itération. C'est pour stopper un comportement étrange de la balle
            # lorsqu'il trouve une collision *à l'intérieur* de la raquette, la balle s'inverse, et est
            # toujours à l'intérieur de la raquette et donc rebondit à l'intérieur.
            # De cette façon, la balle peut toujours s'échapper et rebondir correctement
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = (angle, z)


    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)


class Bat(pygame.sprite.Sprite):
    """Raquette mobile qui peut frapper la balle
    Retourne: objet bat
    Méthode: reinit, update, moveup, movedown
    Attributs: which, speed"""

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(r"C:\Users\Anthony\PycharmProjects\chickengame\src\images\bat.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed)
        self.state = "moveup"


    def movedown(self):
        self.movepos[1] = self.movepos[1] + (self.speed)
        self.state = "movedown"


def main():
    # Initialisation de la fenêtre d'affichage
    pygame.init()
    screen = pygame.display.set_mode((900, 720))
    pygame.display.set_caption('Basic Pong')

    # Remplissage de l'arrière-plan
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialisation des joueurs
    global player1
    global player2
    player1 = Bat("left")
    player2 = Bat("right")

    # Initialisation de la balle
    speed = 10
    rand = ((0.1 * (random.randint(5, 8))))
    ball = Ball((0, 0), (0.47, speed))

    # Initialisation des sprites
    playersprites = pygame.sprite.RenderPlain((player1, player2))
    ballsprite = pygame.sprite.RenderPlain(ball)

    # Blitter le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialisation de l'horloge
    clock = pygame.time.Clock()

    # Boucle d'évènements
    while 1:
        # S'assurer que le jeu ne fonctionne pas à plus de 60 images par secondes
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    player1.moveup()
                if event.key == K_z:
                    player1.movedown()
                if event.key == K_UP:
                    player2.moveup()
                if event.key == K_DOWN:
                    player2.movedown()
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_z:
                    player1.movepos = [0, 0]
                    player1.state = "still"
                if event.key == K_UP or event.key == K_DOWN:
                    player2.movepos = [0, 0]
                    player2.state = "still"

        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)
        ballsprite.update()
        playersprites.update()
        ballsprite.draw(screen)
        playersprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
