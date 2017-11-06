#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# TODO creer juste la poule qui pond avec la touche espace loeuf et le child qui se barre au bout de 10 secondes
# TODO creer les groupes comme dans aliens.py, creer le groupe des oeufs

#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'images')
data_dir_sounds = os.path.join(main_dir, 'sounds')

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
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
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
        return Egg(self.rect)

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


class Egg(pygame.sprite.Sprite):
    def __init__(self, chicken_pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('egg.png', -1)
        print(chicken_pos)
        print(chicken_pos.x, chicken_pos.y)
        print(chicken_pos.x + chicken_pos.width/2 - 5, chicken_pos.y + chicken_pos.height/2)
        self.rect = self.rect.move(chicken_pos.x + chicken_pos.width/2 - 40, chicken_pos.y + chicken_pos.height/2)

    def update(self):
        pass
        # self.rect.move_ip(5, 10)


class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 1))
        print(self.move)
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
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
    chimp = Chimp()
    fist = Fist()
    chicken = Chicken()

    # Initialize Game Groups
    eggs = pygame.sprite.RenderPlain()
    allsprites = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Chicken.containers = allsprites
    # Egg.containers = eggs, allsprites

    # Activation de l'appuie long sur les touches
    pygame.key.set_repeat(400, 30)

    allsprites.add(chicken)
    allsprites.add(eggs)

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
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

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
                    eggs.add(chicken.lay())

        eggs.update()
        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        eggs.draw(screen)
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
