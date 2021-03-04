import pygame


class Portal(pygame.sprite.Sprite):
    def __init__(self, name, position, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.position = position
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

