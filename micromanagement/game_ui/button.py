import pygame as pg


class Button:

    def __init__(self, x, y, main_image, alternate_image=None, scale=1, active=True):
        width = main_image.get_width()
        height = main_image.get_height()

        self.main_image = pg.transform.scale(main_image, (int(width * scale), int(height * scale)))
        self.alternate_image = None
        if alternate_image:
            self.alternate_image = pg.transform.scale(alternate_image, (int(width * scale), int(height * scale)))

        self.image = main_image

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.active = active

    def draw(self, screen):
        action = False
        pos = pg.mouse.get_pos()

        if self.active:
            if self.rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1:
                    if self.alternate_image:
                        self.image = self.alternate_image
                    self.clicked = True
                    action = True

            if pg.mouse.get_pressed()[0] == 0:
                self.image = self.main_image
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def enable(self):
        self.active = True
        self.image = self.main_image
        return self.active

    def disable(self):
        self.active = False
        if self.alternate_image:
            self.image = self.alternate_image
        return self.active