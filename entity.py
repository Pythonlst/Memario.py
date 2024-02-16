import pygame
from level import Level
ground_h = 120
w, h = 1200, 900


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, cord, screen):
        super().__init__()
        self.surface = screen
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

    def update(self, list_sprites):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if not self.grounded:
            self.y_speed += self.gravity
        if self.life:
            self.hand_controll()
            if len(pygame.sprite.spritecollide(self, list_sprites, dokill=False)) > 0:
                for i in pygame.sprite.spritecollide(self, list_sprites, dokill=False):
                    sprite = i
                    if sprite.rect.collidepoint(self.rect[0] + self.rect[3] // 2, self.rect.bottom):
                        self.grounded = True
                        self.rect.bottom = sprite.rect.top
                    if (sprite.rect.collidepoint(self.rect[0] + self.rect[3] // 2, self.rect[2])
                            and self.x_speed < 0):
                        self.x_speed = 0

            else:
                self.grounded = False
        else:
            if self.rect.top > h - ground_h:
                self.is_out = True

    def draw(self):
        self.surface.blit(self.image, self.rect)
