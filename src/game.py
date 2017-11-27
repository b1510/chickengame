#!/usr/bin/env python
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror
from datetime import datetime, timedelta
from random import randint

# TODO animation
# TODO minichicken, bec coupé

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'images')
data_dir_sounds = os.path.join(main_dir, 'sounds')

LAY_TIME = 10
SCORE = 0


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
        print('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)  # call Sprite initializer
        self.original, self.rect = load_image('chicken.png', -1)
        self.image2, self.rect2 = load_image('chicken_2.png', -1)

        self.image = self.original

        self.lay_on_going = False
        self.droite = self.image
        self.gauche = pygame.transform.flip(self.image, 1, 0)
        self.facing = self.droite
        self.speed = 13
        self.step = 0
        self.current_animation = 0
        self.cro_prout_sound = load_sound("croa_prout.wav")

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):

        if self.lay_on_going:
            self._lay_animation()
            # pygame.mouse.set_pos(self.rect.midtop)
        else:
            pos = pygame.mouse.get_pos()
            # self.rect.midtop = pos
            
    def move(self, direction):
        if direction == 'droite':
            self.image = self.droite
            self.rect.move_ip(self.speed, 0)
        if direction == 'gauche':
            self.image = self.gauche
            self.rect.move_ip(-self.speed, 0)
        if direction == 'haut':
            self.rect.move_ip(0, -self.speed)
        if direction == 'bas':
            self.rect.move_ip(0, self.speed)

    def lay(self):
        self.lay_on_going = True
        self.cro_prout_sound.play()
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
                    # new random position
                    self.rect.bottomright = randint(0, self.area.right), randint(0, self.area.bottom)


class MiniChicken(pygame.sprite.Sprite):

    def __init__(self, chicken_pos):
        pygame.sprite.Sprite.__init__(self, self.containers)  # call Sprite initializer
        self.image, self.rect = load_image('chicken.png', -1)
        w, h = self.image.get_size()
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.image = pygame.transform.scale(self.image, (int(w * 0.4), int(h * 0.4)))

        self.rect = self.rect.move(chicken_pos.x + chicken_pos.width/2 - 40, chicken_pos.y + chicken_pos.height/2)
        self.minchiken_animation_on_going = True

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):

        if self.minchiken_animation_on_going:
            self.rect.move_ip(-4, 0)
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.kill()
                self.minchiken_animation_on_going = False


class Egg(pygame.sprite.Sprite):

    def __init__(self, chicken_pos):
        pygame.sprite.Sprite.__init__(self, self.containers)  # call Sprite initializer
        self.image, self.rect = load_image('egg.png', -1)
        self.image_bk, self.rect_bk = load_image('broken_egg.png', -1)
        self.rect = self.rect.move(chicken_pos.x + chicken_pos.width/2 - 40, chicken_pos.y + chicken_pos.height/2)

        self.time_start = datetime.now()
        self.step = 0
        self.dizzy = 1
        self.original = self.image_bk

        self.spawn_on_going = False
        self.minichicken_pop = False

        self.nb_spin = 0
        self.velocity = 1

        self.minchicken_group = pygame.sprite.RenderPlain()
        self.screen = pygame.display.get_surface()

        self.spawn_sound = load_sound("spawn.wav")

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
                if not self.minichicken_pop:
                    MiniChicken(self.rect)
                    self.spawn_sound.play()
                    self.minichicken_pop = True
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

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("fonts/Peppa_Pig1.ttf", 30)
        self.color = (10, 10, 10)
        self.lastscore = -1
        self.update()
        self.redraw()

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 1, self.color)

    def redraw(self):
        screen = pygame.display.get_surface()
        self.rect = self.image.get_rect().move(screen.get_width() - 150, 30)


animate_chicken = pygame.USEREVENT + 1
animate_chicken2 = pygame.USEREVENT + 2
pygame.time.set_timer(animate_chicken, 1000)
pygame.time.set_timer(animate_chicken2, 2500)

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pygame.init()
    pygame.display.set_caption('Mademoiselle Poule')
    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode((800, 800), HWSURFACE | DOUBLEBUF | RESIZABLE)

    background = draw_background(screen)

    # Prepare Game Objects
    clock = pygame.time.Clock()
    intro = load_sound("zic_peppa.wav")

    intro.play()

    # Initialize Game Groups
    eggs = pygame.sprite.RenderPlain()
    mini_chicken_group = pygame.sprite.Group()
    allsprites = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    MiniChicken.containers = mini_chicken_group, allsprites
    Egg.containers = eggs, allsprites
    Chicken.containers = allsprites
    Score.containers = allsprites

    chicken = Chicken()
    global SCORE
    display_score = Score()
    allsprites.add(display_score)
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
            elif event.type == VIDEORESIZE:
                # if screen is resize
                screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                background = draw_background(screen)
                chicken.kill()
                chicken = Chicken()
                display_score.redraw()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                chicken.lay()
            elif event.type == MOUSEBUTTONUP:
                pass

            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    chicken.move("bas")
                if event.key == K_LEFT:
                    chicken.move("gauche")
                if event.key == K_RIGHT:
                    chicken.move("droite")
                if event.key == K_UP:
                    chicken.move("haut")
                if event.key == K_SPACE:
                    chicken.lay()
                    SCORE += 1
            # elif event.type == animate_chicken:
            #     chicken.image = chicken.image2
            # elif event.type == animate_chicken2:
            #     chicken.image = chicken.original


        # clear/erase the last drawn sprites
        allsprites.clear(screen, background)
        allsprites.update()

        # draw the scene
        dirty = allsprites.draw(screen)
        pygame.display.update(dirty)

    pygame.quit()


def draw_background(screen):
    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((99, 219, 255))
    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font("fonts/Peppa_Pig1.ttf", 45)
        text = font.render("Mademoiselle Poule", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        textpos.y = 20
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    return background


# Game Over

main()
# if __name__ == '__main__':
#     main()
