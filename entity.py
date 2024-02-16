import pygame
w, h = 1200, 900


class Heatbox(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect.get_rect()
        print(self.rect)

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
        self.speed = 7
        self.life = True
        self.jump_speed = -9
        self.gravity = 0.2
        self.grounded = False
        self.is_out = False
        self.animation_step = 1
        self.left_detect = None
        self.right_detect = None
        self.bottom_detect = None
        self.top_detect = None

    def hand_controll(self):
        pass

    def death(self, dead_image):
        self.image = dead_image
        self.life = False

    def update(self, list_sprites):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if not self.grounded:
            self.y_speed += self.gravity
        self.left_detect = Heatbox(pygame.Rect((self.rect.x, self.rect.y + 10),
                                               (self.rect[3] // 2, self.rect[4] - 10)))
        self.right_detect = Heatbox(pygame.Rect((self.rect.x + self.rect[3] // 2, self.rect.y + 5),
                                                (self.rect[3] // 2, self.rect[4] - 10)))
        self.bottom_detect = Heatbox(pygame.Rect((self.rect.x, self.rect.bottom - 5),
                                                 (self.rect[3], 5)))
        self.top_detect = Heatbox(pygame.Rect((self.rect.x, self.rect.y), (self.rect[3], 5)))
        print(self.left_detect.rect())
        if self.life:
            self.hand_controll()
            if len(pygame.sprite.spritecollide(self, list_sprites, dokill=False)) > 0:
                for i in pygame.sprite.spritecollide(self, list_sprites, dokill=False):
                    sprite = i
                    if pygame.sprite.spritecollide(self.bottom_detect, list_sprites, dokill=False):
                        self.grounded = True
                        self.rect.bottom = sprite.rect.top
                    if pygame.sprite.spritecollide(self.top_detect, list_sprites, dokill=False):
                        self.y_speed = self.gravity
                    #if pygame.sprite.spritecollide(self.right_detect, list_sprites, dokill=False):
                        #self.x_speed = 0
                    if pygame.sprite.spritecollide(self.left_detect, list_sprites, dokill=False) and self.x_speed < 0:
                        self.x_speed = 0

            else:
                self.grounded = False
        else:
            pass

    def draw(self):
        self.surface.blit(self.image, self.rect)
