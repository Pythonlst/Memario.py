import pygame
import os

# making elements of the game
enemy_image = pygame.image.load('data/gomba.png')
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

block = pygame.image.load('data/block.png')
block = pygame.transform.scale(block, (60, 60))

brick = pygame.image.load('data/brick.png')
brick = pygame.transform.scale(brick, (60, 60))

lucky = pygame.image.load('data/lucky.png')
lucky = pygame.transform.scale(lucky, (60, 60))

# reading and making list with levels
names, levels = os.listdir(path="levels/"), []
for _ in names:
    with open(f'levels/{_}') as level:
        level = level.read().split('\n')
        levels.append(level)
# ------------------------------------


class Level:
    def __init__(self):
        self.level_file = levels
        self.level_number = 0
        self.mario = None
        self.surface = None

    def render(self):
        level = self.level_file[self.level_number]
        self.surface = pygame.surface.Surface((60 * len(level[0]), 60 * len(level)))
        self.surface.fill((6, 6, 6))
        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == '#':
                    self.surface.blit(block, (0 + 60 * j, 0 + 60 * i))
                elif level[i][j] == 'P':
                    self.mario = (0 + 60 * j, 0 + 60 * i)
                elif level[i][j] == 'H':
                    self.surface.blit(brick, (0 + 60 * j, 0 + 60 * i))
                elif level[i][j] == '?':
                    self.surface.blit(lucky, (0 + 60 * j, 0 + 60 * i))
        self.surface.set_colorkey((6, 6, 6))
        return self.surface

    def end_level(self):
        if len(self.level_file) > self.level_number + 2:
            self.level_number += 1
