import sys
import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 800))
screen_rect = screen.get_rect()
clock = pg.time.Clock()

font = pg.font.Font(None, 48)
rendered_text = font.render("Animated Text", True, pg.Color("dodgerblue"))
text_rect = rendered_text.get_rect(midleft=(900, screen_rect.centery))

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    if text_rect.centerx > screen_rect.centerx:
        print(text_rect.centerx)
        text_rect.move_ip(-5, 0)

    screen.fill(pg.Color("gray5"))
    screen.blit(rendered_text, text_rect)

    pg.display.update()
    clock.tick(60)

pg.quit()
sys.exit()