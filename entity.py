ground_h = 120
w, h = 1200, 900


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
