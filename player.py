import pygame
from entity import Entity

ground_h = 120
w, h = 1200, 900
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
