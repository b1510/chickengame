#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# TODO creer juste la poule qui pond avec la touche espace loeuf et le child qui se barre au bout de 10 secondes
# TODO creer les groupes comme dans aliens.py, creer le groupe des oeufs
# TODO creer les minichicken qui se barrent !! faire le groupe
# TODO les sons
# TODO le controle de la souris
#Import Modules
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror
from datetime import datetime, timedelta

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'images')
data_dir_sounds = os.path.join(main_dir, 'sounds')

LAY_TIME = 10

# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir_sounds, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects
class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers) #call Sprite initializer
        self.image, self.rect = load_image('chicken.png', -1)

        self.lay_on_going = False
        self.droite = self.image
        self.gauche = pygame.transform.flip(self.image, 1, 0)
        self.facing = self.droite
        self.speed = 10
        self.step = 0
        self.current_animation = 0




    def update(self):

        if self.lay_on_going:
            self._lay_animation()
            pygame.mouse.set_pos(self.rect.midtop)
        else:
            pos = pygame.mouse.get_pos()
            self.rect.midtop = pos
            
    def move(self, direction):
        # Déplacement vers la droite
        if direction == 'droite':
            self.image = self.droite
            self.rect.move_ip(self.speed, 0)

        # Déplacement vers la gauche
        if direction == 'gauche':
            self.image = self.gauche
            self.rect.move_ip(-self.speed, 0)

        # Déplacement vers le haut
        if direction == 'haut':
            self.rect.move_ip(0, -self.speed)

        # Déplacement vers le bas
        if direction == 'bas':
            self.rect.move_ip(0, self.speed)

    def lay(self):
        self.lay_on_going = True
        Egg(self.rect)

    def _lay_animation(self):

        if self.lay_on_going:
            self.animate_speed = 20
            if self.step == 0:
                self.rect.move_ip(0, -self.animate_speed)
                self.current_animation += 1
                if self.current_animation > 5:
                    self.step += 1
            elif self.step == 1:
                self.rect.move_ip(self.animate_speed, 0)
                self.current_animation += 1
                if self.current_animation > 10:
                    self.step += 1
            elif self.step == 2:
                self.rect.move_ip(0, self.animate_speed)
                self.current_animation += 1
                if self.current_animation > 16:
                    self.step = 0
                    self.current_animation = 0
                    self.lay_on_going = False


class MiniChicken(pygame.sprite.Sprite):

    def __init__(self, chicken_pos):
        pygame.sprite.Sprite.__init__(self, self.containers) #call Sprite initializer
        self.image, self.rect = load_image('chicken.png', -1)
        w, h = self.image.get_size()
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.image = pygame.transform.scale(self.image, (int(w * 0.4), int(h * 0.4)))
        print(self.rect)
        self.rect = self.rect.move(chicken_pos.x + chicken_pos.width/2 - 40, chicken_pos.y + chicken_pos.height/2)
        self.minchiken_animation_on_going = True
        self.current_animation = 0

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):

        if self.minchiken_animation_on_going:
            self.rect.move_ip(-5, 0)
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.kill()
                self.minchiken_animation_on_going = False



class Egg(pygame.sprite.Sprite):

    def __init__(self, chicken_pos):
        pygame.sprite.Sprite.__init__(self, self.containers) #call Sprite initializer
        self.image, self.rect = load_image('egg.png', -1)
        self.image_bk, self.rect_bk = load_image('broken_egg.png', -1)
        self.rect = self.rect.move(chicken_pos.x + chicken_pos.width/2 - 40, chicken_pos.y + chicken_pos.height/2)

        self.time_start = datetime.now()
        self.step = 0
        self.current_animation = 0
        self.dizzy = 1
        self.original = self.image_bk

        self.spawn_on_going = False

        self.nb_spin = 0
        self.velocity = 1

        self.minchicken_group = pygame.sprite.RenderPlain()
        self.screen = pygame.display.get_surface()

    def update(self):
        if self.time_start + timedelta(seconds=LAY_TIME) < datetime.now():
            self.spawn()


    def spawn(self):
        self.spawn_on_going = True
        self._spawn_animation()

    def _spawn_animation(self):
        if self.spawn_on_going:

            if self.step == 0:
                self._spin()
            elif self.step == 1:
                MiniChicken(self.rect)
                self.kill()
                self.spawn_on_going = False


    def _spin(self):

        self.rect.move_ip(0, -2 * self.velocity)
        center = self.rect.center
        if self.nb_spin >= 40:
            self.step += 1
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)

            self.nb_spin += 1
            self.rect.move_ip(12, 0)
            self.image.get_rect().move_ip(12, 0)
            if 10 <= self.nb_spin <= 30:
                self.velocity = -1 * self.velocity
                self.dizzy -= 2
            else:
                self.dizzy += 2
        self.rect = self.image.get_rect(center=center)


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((99, 219, 255))

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Mademoiselle Poule", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')

    screen.blit(background, (0,0))
    pygame.display.flip()

    # Initialize Game Groups
    eggs = pygame.sprite.RenderPlain()
    mini_chicken_group = pygame.sprite.Group()
    allsprites = pygame.sprite.RenderUpdates()

    #assign default groups to each sprite class
    MiniChicken.containers = mini_chicken_group, allsprites
    Egg.containers = eggs, allsprites
    Chicken.containers = allsprites

    chicken = Chicken()

    # Activation de l'appuie long sur les touches
    pygame.key.set_repeat(400, 30)

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pass

            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    print("DOWN")
                    chicken.move("bas")
                if event.key == K_LEFT:
                    print("LEFT")
                    chicken.move("gauche")
                if event.key == K_RIGHT:
                    print("RIGHT")
                    chicken.move("droite")
                if event.key == K_UP:
                    print("UP")
                    chicken.move("haut")

                if event.key == K_SPACE:
                    print("SPACE")
                    chicken.lay()
                    # eggs.add(egg)
                    # mini_chicken_group.add(mc)

        # clear/erase the last drawn sprites
        allsprites.clear(screen, background)
        allsprites.update()

        #draw the scene
        dirty = allsprites.draw(screen)
        pygame.display.update(dirty)

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
