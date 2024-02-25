import pygame
import os
import pygame.sprite

# making elements of the game
enemy_image = pygame.image.load('data/gomba.png')
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

block = pygame.image.load('data/block.png')
block = pygame.transform.scale(block, (60, 60))

brick = pygame.image.load('data/brick.png')
brick = pygame.transform.scale(brick, (60, 60))

lucky = pygame.image.load('data/lucky.png')
lucky = pygame.transform.scale(lucky, (60, 60))

psl = pygame.image.load('data/PipeSideL.png')
psl = pygame.transform.scale(psl, (60, 60))

psr = pygame.image.load('data/PipeSideR.png')
psr = pygame.transform.scale(psr, (60, 60))

ptr = pygame.image.load('data/PipeTopR.png')
ptr = pygame.transform.scale(ptr, (60, 60))

ptl = pygame.image.load('data/PipeTopL.png')
ptl = pygame.transform.scale(ptl, (60, 60))

# reading and making list with levels
names, levels = os.listdir(path="levels/"), []
for _ in names:
    with open(f'levels/{_}') as level:
        level = level.read().split('\n')
        levels.append(level)


# ------------------------------------


class Element(pygame.sprite.Sprite):
    def __init__(self, image, surface, coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.surface = surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

    def update(self, coord):
        self.rect.x += coord[0]
        self.surface.blit(self.image, self.rect)


class Level:
    def __init__(self, screen):
        self.level_file = levels
        self.level_number = 0
        self.mario = None
        self.surface = screen
        self.surfaces = pygame.sprite.Group()
        self.deco = pygame.sprite.Group()
        self.first_render()

    def first_render(self):
        level = self.level_file[self.level_number]
        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == '#':
                    el = Element(block, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == 'P':
                    self.mario = (0 + 60 * j, 0 + 60 * i)
                elif level[i][j] == 'H':
                    el = Element(brick, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == '?':
                    el = Element(lucky, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == '[':
                    el = Element(psl, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == ']':
                    el = Element(psr, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == '>':
                    el = Element(ptr, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)
                elif level[i][j] == '<':
                    el = Element(ptl, self.surface, (0 + 60 * j, 0 + 60 * i))
                    self.surfaces.add(el)

    def render(self, coord):
        self.surfaces.update(coord)
        self.deco.update(coord)

    def end_level(self):
        if len(self.level_file) > self.level_number + 2:
            self.level_number += 1
