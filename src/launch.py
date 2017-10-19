import pygame
from pygame.locals import *
from constant import *
from perso import Perso, Egg
from random import randint

# Initialisation de la bibliothèque Pygame
pygame.init()

# Création de la fenêtre
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))

# Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)

#Titre
pygame.display.set_caption(titre_fenetre)

# Chargement et collage du fond
# fond = pygame.image.load("images/background.jpg").convert()
# fenetre.blit(fond, (0, 0))
fenetre.fill([99, 219, 255])


# chicken = pygame.image.load("images/chicken.png").convert_alpha()
chicken = Perso("images/chicken.png", "images/chicken_left.png")
#pos_chicken = chicken.get_rect()
#chicken_x = 0
#chicken_y = 0
#fenetre.blit(chicken, (chicken_x, chicken_y))
# fenetre.blit(chicken, pos_chicken)

egg = pygame.image.load("images/egg.png").convert_alpha()

# Rafraîchissement de l'écran
pygame.display.flip()

# Variable qui continue la boucle si = 1, stoppe si = 0
continuer = 1

step = 15

# Activation de l'appuie long sur les touches
pygame.key.set_repeat(400, 30)
# Limitation de vitesse de la boucle
pygame.time.Clock().tick(30)

egg_list = []


def egg_already_exit(egg, egg_list):
    for eggl in egg_list:
        if eggl.case_x == egg.case_x and eggl.case_y == egg.case_y:
            return True
    return False

# Boucle infinie
while continuer:
    for event in pygame.event.get():   # On parcours la liste de tous les événements reçus
        if event.type == QUIT:     # Si un de ces événements est de type QUIT
            continuer = 0      # On arrête la boucle
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                print("DOWN")
                chicken.deplacer("bas")
                # chicken_y = step + chicken_y
                # pos_chicken = pos_chicken.move(0, step)
            if event.key == K_LEFT:
                print("LEFT")
                chicken.deplacer("gauche")
                # chicken_x = -1 * step + chicken_x
                # pos_chicken = pos_chicken.move(-1 * step, 0)
            if event.key == K_RIGHT:
                print("RIGHT")
                chicken.deplacer("droite")
                # chicken_x = step + chicken_x
                # pos_chicken = pos_chicken.move(step, 0)
            if event.key == K_UP:
                print("UP")
                chicken.deplacer("haut")
                # chicken_y = -1 * step + chicken_y
                # pos_chicken = pos_chicken.move(0, -1 * step)

            if event.key == K_SPACE:
                print("SPACE")
                son = pygame.mixer.Sound("sounds/coin.wav")
                son.play()
                egg = Egg("images/egg.png")
                egg.set_position_case(chicken.case_x, chicken.case_y)

                if not egg_already_exit(egg, egg_list):
                    egg_list.append(egg)

                # nouvelle position random pour le poulet
                chicken.set_position_case(randint(0, nombre_sprite_cote - 1),
                                          randint(0, nombre_sprite_cote - 1))

        # if event.type == MOUSEBUTTONDOWN:
        #     if event.button:
        #         # On change les coordonnées du perso
        #         chicken.x = event.pos[0]
        #         chicken.y = event.pos[1]

    # Re-collage
    fenetre.fill([99, 219, 255])
    #fenetre.blit(chicken, pos_chicken)
    for egg in egg_list:
        fenetre.blit(egg.direction, (egg.x, egg.y))

    fenetre.blit(chicken.direction, (chicken.x, chicken.y))

    if len(egg_list) == nombre_sprite_cote * nombre_sprite_cote:
        print("YOU WIN")
        fond = pygame.image.load("images/win.jpg").convert()
        fenetre.blit(fond, (0, 0))
    # Rafraichissement
    pygame.display.flip()


