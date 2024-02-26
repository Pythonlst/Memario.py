import pygame
from entity import Entity

enemy_image = pygame.image.load('data/gomba.png')
enemy_image.get_colorkey()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))


class Goomba(Entity):
    def __init__(self, coord, screen):
        self.timer = 0
        self.x_speed = -1
        super().__init__(enemy_image, coord, screen)

    def animation(self):
        if self.timer > 5:
            self.image, self.timer = pygame.transform.flip(self.image, True, False), 0
        else:
            self.timer += 1

    def update(self, sprites, coord):
        super().update(sprites)
        self.animation()
        self.rect.x += coord[0]
        self.draw()

    def hand_controll(self):
        if self.surface.get_width() >= self.rect.x:
            if self.right_detect:
                self.x_speed = 1
            if self.left_detect:
                self.x_speed = -1