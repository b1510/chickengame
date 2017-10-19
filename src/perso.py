import pygame
from constant import *


class Perso(pygame.sprite.Sprite):
    """Classe permettant de créer un personnage"""

    def __init__(self, droite, gauche=None, haut=None, bas=None, niveau=None):
        # Sprites du personnage
        self.droite = pygame.image.load(droite).convert_alpha()

        self.gauche = None
        if gauche is not None:
            self.gauche = pygame.image.load(gauche).convert_alpha()

        self.haut = None
        if haut is not None:
            self.haut = pygame.image.load(haut).convert_alpha()

        self.bas = None
        if bas is not None:
            self.bas = pygame.image.load(bas).convert_alpha()
        # Position du personnage en cases et en pixels
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        # Direction par défaut
        self.direction = self.droite
        # Niveau dans lequel le personnage se trouve
        self.niveau = niveau

    def deplacer(self, direction):
        """Methode permettant de déplacer le personnage"""

        # Déplacement vers la droite
        if direction == 'droite':
            # Pour ne pas dépasser l'écran
            if self.case_x < (nombre_sprite_cote - 1):
                # On vérifie que la case de destination n'est pas un mur
                #if self.niveau.structure[self.case_y][self.case_x + 1] != 'm':
                # Déplacement d'une case
                self.case_x += 1
                # Calcul de la position "réelle" en pixel
                self.x = self.case_x * taille_sprite
            # Image dans la bonne direction
            self.direction = self.droite

        # Déplacement vers la gauche
        if direction == 'gauche':
            if self.case_x > 0:
                #if self.niveau.structure[self.case_y][self.case_x - 1] != 'm':
                self.case_x -= 1
                self.x = self.case_x * taille_sprite
            self.direction = self.gauche

        # Déplacement vers le haut
        if direction == 'haut':
            if self.case_y > 0:
                #if self.niveau.structure[self.case_y - 1][self.case_x] != 'm':
                self.case_y -= 1
                self.y = self.case_y * taille_sprite
            if self.haut is not None:
                self.direction = self.haut

        # Déplacement vers le bas
        if direction == 'bas':
            if self.case_y < (nombre_sprite_cote - 1):
                # if self.niveau.structure[self.case_y + 1][self.case_x] != 'm':
                self.case_y += 1
                self.y = self.case_y * taille_sprite
            if self.bas is not None:
                self.direction = self.bas

    def set_position_case(self, case_x, case_y):
        self.case_x = case_x
        self.case_y = case_y
        self.x = self.case_x * taille_sprite
        self.y = self.case_y * taille_sprite

class Egg(Perso):
    def __init__(self, droite, gauche=None, haut=None, bas=None, niveau=None):
        super().__init__(droite, gauche, haut, bas, niveau)
