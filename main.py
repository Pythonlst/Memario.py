import pygame
import os
pygame.init()

w = 1200
h = 900
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
# making sprites for the mario
buf = pygame.image.load('data/mario_sprite.png')
buf.set_colorkey((255, 255, 255))
frames = []
for _ in [(0, 0, 64, 85), (79, 0, 150, 85), (165, 0, 225, 85), (240, 0, 321, 85), (256, 100, 342, 187),
          (80, 101, 154, 186)]:
    cropped = pygame.Surface((_[2] - _[0], _[3] - _[1]))
    cropped.blit(buf, (0, 0), (_[0], _[1], _[2], _[3]))
    cropped.set_colorkey((0, 0, 0))
    cropped = pygame.transform.scale(cropped, (50, 60))
    frames.append(cropped)
# making elements of the game
enemy_image = pygame.image.load('data/gomba.png')
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

block = pygame.image.load('data/block.png')
block = pygame.transform.scale(block, (60, 60))

brick = pygame.image.load('data/brick.png')
brick = pygame.transform.scale(brick, (60, 60))

lucky = pygame.image.load('data/lucky.png')
lucky = pygame.transform.scale(lucky, (60, 60))

ground_h = 120

# reading and making list with levels
names, levels = os.listdir(path="levels/"), []
for _ in names:
    with open(f'levels/{_}') as level:
        level = level.read().split('\n')
        levels.append(level)
# ------------------------------------


class Entity:
    def __init__(self, image, cord):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = cord[0]
        self.rect.y = cord[1]
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 7
        self.life = True
        self.jump_speed = -9
        self.gravity = 0.2
        self.grounded = False
        self.is_out = False
        self.animation_step = 1

    def hand_controll(self):
        pass

    def kill(self, dead_image):
        self.image = dead_image
        self.life = False

    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.life:
            self.hand_controll()
            if self.rect.bottom >= h - ground_h:
                self.grounded = True
                self.rect.bottom = h - ground_h
        else:
            if self.rect.top > h - ground_h:
                self.is_out = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, coord):
        self.past = False
        self.t = 0
        self.camera = 0
        super().__init__(frames[0], coord)

    def animation(self, inverted=None, stop=False, jump=False, seat=False):
        zam = False
        if inverted is not None:
            self.past = inverted
        self.t += 1
        if jump:
            self.image = frames[4]
            self.animation_step = 1
            zam = True
            self.t = 0
        elif stop and self.grounded and self.t >= 3:
            self.image = frames[0]
            self.animation_step = 1
            zam = True
            self.t = 0
        elif self.grounded and self.t >= 3:
            self.image = frames[self.animation_step]
            if self.animation_step >= 3:
                self.animation_step = 1
            else:
                self.animation_step += 1
            zam = True
            self.t = 0
        elif self.grounded and seat:
            self.image = frames[5]
            zam, self.t, self.animation_step = True, 0, 1

        if self.past and zam:
            self.image = pygame.transform.flip(self.image, True, False)

    def hand_controll(self):
        self.x_speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.rect.bottomright[0] <= w - w // 2:
                self.x_speed = self.speed
            else:
                self.camera -= self.speed
            self.animation(inverted=False)
        elif keys[pygame.K_a]:
            if self.rect.bottomleft[0] >= 0:
                self.x_speed = -self.speed
            self.animation(inverted=True)
        elif keys[pygame.K_s]:
            self.animation(seat=True)
        else:
            self.animation(stop=True)
        if self.grounded and keys[pygame.K_w]:
            self.jump()
            self.animation(jump=True)

    def jump(self):
        self.y_speed = self.jump_speed
        self.grounded = False

    def respawn(self):
        self.is_out = False
        self.life = True
        self.rect.midbottom = (w // 2, h - ground_h)


class Level:
    def __init__(self, file):
        self.level_file = file
        self.level_number = 0
        self.mario = None

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


level = Level(levels)
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
