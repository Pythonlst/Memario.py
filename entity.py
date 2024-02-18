import pygame
w, h = 1200, 900


class Heatbox(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect

    def rect(self):
        return self.rect


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
        self.speed = 10
        self.life = True
        self.jump_speed = -20
        self.gravity = 1
        self.grounded = False
        self.is_out = False
        self.animation_step = 1
        self.left_detect = None
        self.right_detect = None
        self.bottom_detect = None
        self.top_detect = None
        self.body = None

    def hand_controll(self):
        pass

    def death(self, dead_image):
        self.image = dead_image
        self.life = False

    def update(self, list_sprites):
        if not self.grounded:
            self.y_speed += self.gravity

        if self.life:
            self.sprite_magic(list_sprites)
            self.hand_controll()
        pygame.draw.rect(self.surface, "WHITE", self.left_detect)
        pygame.draw.rect(self.surface, "WHITE", self.right_detect)
        pygame.draw.rect(self.surface, "GREEN", self.bottom_detect)
        pygame.draw.rect(self.surface, "GREEN", self.top_detect)
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def sprite_magic(self, list_sprites):
        self.left_detect = Heatbox(pygame.Rect(self.rect.x, self.rect.y + 10,
                                               self.rect[2] // 4, self.rect[3] - 20))
        self.right_detect = Heatbox(pygame.Rect(self.rect.x + self.rect[2] // 4 * 3, self.rect.y + 10,
                                                self.rect[2] // 4, self.rect[3] - 20))
        self.bottom_detect = Heatbox(pygame.Rect(self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 6,
                                                 self.rect[2] - 20, 5))
        self.top_detect = Heatbox(pygame.Rect(self.rect.x + 10, self.rect.y + 1, self.rect[2] - 20, 5))
        if len(pygame.sprite.spritecollide(self, list_sprites, dokill=False)) > 0:
            for i in pygame.sprite.spritecollide(self, list_sprites, dokill=False):
                sprite = i
                if pygame.sprite.spritecollide(self.bottom_detect, list_sprites, dokill=False):
                    self.rect.bottom = sprite.rect.top
                    self.y_speed = 0
                    self.grounded = True
                if pygame.sprite.spritecollide(self.top_detect, list_sprites, dokill=False):
                    self.y_speed = self.gravity
                    self.rect.top = sprite.rect.bottom
                if pygame.sprite.spritecollide(self.right_detect, list_sprites, dokill=False):
                    if self.x_speed > 0:
                        self.x_speed = 0
                    self.rect.right = sprite.rect.left
                if pygame.sprite.spritecollide(self.left_detect, list_sprites, dokill=False):
                    if self.x_speed < 0:
                        self.x_speed = 0
                    self.rect.left = sprite.rect.right
        else:
            self.grounded = False

    def draw(self):
        self.surface.blit(self.image, self.rect)
