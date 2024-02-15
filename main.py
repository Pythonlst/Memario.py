import pygame
import os
from entity import Entity
from player import Player
from level import Level
pygame.init()

# setting main window
w, h = 1200, 900
screen = pygame.display.set_mode((w, h))
fps = 60
clock = pygame.time.Clock()
game_over = False

# magic with language - not used
font_path = 'data/font.ttf'
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)
retry_text = font_small.render('press any key', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
# -------------------------------

level = Level()
level.render()
player = Player(level.mario)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    screen.fill((92, 148, 252))
    screen.blit(level.render(), (player.camera, 0))
    if not player.is_out:
        player.update()
        player.draw(screen)
    pygame.display.flip()
quit()
