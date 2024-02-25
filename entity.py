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

        self.detectgr = None
        self.surface = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = cord[0]
        self.rect.y = cord[1]
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5
        self.life = True
        self.jump_speed = -23
        self.gravity = 1
        self.grounded = False
        self.is_out = False
        self.animation_step = 1
        self.detect = None
        self.body = None

    def hand_controll(self):
        # найс костыль, бро. Убил 2 часа жизни
        pass

    def death(self, dead_image):
        self.image = dead_image
        self.life = False

    def update(self, list_sprites):
        if not self.grounded:
            if self.y_speed < 22:
                self.y_speed += self.gravity
                print(self.y_speed)
            if self.y_speed == 22:
                self.y_speed = 20
        # строчка внизу, оказывается, важна
        self.hand_controll()
        self.rect.y += self.y_speed
        self.sprite_magic(list_sprites, 0, self.y_speed)
        self.rect.x += self.x_speed
        self.sprite_magic(list_sprites, self.x_speed, 0)

    def sprite_magic(self, list_sprites, xvel, yvel):
        self.detect = Heatbox(pygame.Rect(self.rect.x, self.rect.y,
                                          self.rect[2], self.rect[3]))
        self.detectgr = Heatbox(pygame.Rect(self.rect.x + 10, self.rect.y + 70,
                                            self.rect[2] // 2, self.rect[3] // 2))
        if len(pygame.sprite.spritecollide(self, list_sprites, dokill=False)) > 0:
            for i in pygame.sprite.spritecollide(self, list_sprites, dokill=False):

                sprite = i
                if xvel == 0 and pygame.sprite.spritecollide(self, list_sprites, dokill=False):
                    self.x_speed = 1
                if xvel > 0:
                    self.rect.right = sprite.rect.left

                if xvel < 0:
                    self.rect.left = sprite.rect.right

                if yvel > 0:
                    self.rect.bottom = sprite.rect.top
                    self.grounded = True
                    self.y_speed = 0

                if yvel < 0:
                    self.rect.top = sprite.rect.bottom
                    self.y_speed = 0
        # 4 часа спустя, я переписал хитбоксы. Что за адскую Гидру ты здесь приютил ранее, Влад, зачем столько
        # сложностей?!
        if self.grounded and not pygame.sprite.spritecollide(self.detectgr, list_sprites, dokill=False):
            self.grounded = False

    def draw(self):
        self.surface.blit(self.image, self.rect)
#        pygame.draw.rect(self.surface, "WHITE", self.detect)
#        pygame.draw.rect(self.surface, "WHITE", self.detectgr)
