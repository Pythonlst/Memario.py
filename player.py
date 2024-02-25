import pygame
from entity import Entity

w, h = 1200, 900
# making sprites for the mario
buf = pygame.image.load('data/smb_mario_sheet.png')
buf.set_colorkey((255, 255, 255))
frames = []
for _ in [(419, 0, 451, 31), (480, 0, 511, 31), (539, 0, 571, 31), (600, 0, 632, 31), (718, 0, 751, 31),
          (80, 101, 154, 186)]:
    cropped = pygame.Surface((_[2] - _[0], _[3] - _[1]))
    cropped.blit(buf, (0, 0), (_[0], _[1], _[2], _[3]))
    cropped.set_colorkey((0, 0, 0))
    cropped = pygame.transform.scale(cropped, (50, 50))
    frames.append(cropped)


class Player(Entity):
    def __init__(self, coord, screen):
        self.past = False
        self.t = 0
        self.camera = [0, 0]
        super().__init__(frames[0], coord, screen)

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
        self.camera = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.rect.bottomright[0] <= w - w // 2:
                self.x_speed = self.speed
                if keys[pygame.K_LSHIFT]:
                    self.x_speed = self.speed * 1.6
                else:
                    self.x_speed = self.speed
            else:
                if keys[pygame.K_LSHIFT]:
                    self.camera[0] = self.camera[0] - self.speed * 1.6
                else:
                    self.camera[0] = self.camera[0] - self.speed
            self.animation(inverted=False)
        elif keys[pygame.K_a]:
            if self.rect.bottomleft[0] >= 0:
                self.x_speed = -self.speed
                if keys[pygame.K_LSHIFT]:
                    self.x_speed = -self.speed * 1.6
                else:
                    self.x_speed = -self.speed
            self.animation(inverted=True)

        elif keys[pygame.K_s]:
            self.animation(seat=True)
        else:
            self.animation(stop=True)
        if self.grounded and keys[pygame.K_w]:
            self.jump(self.jump_speed)
            self.animation(jump=True)

    def jump(self, js):
        self.y_speed = js
        self.grounded = False

    def respawn(self):
        self.is_out = False
        self.life = True
