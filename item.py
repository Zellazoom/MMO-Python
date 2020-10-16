import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, damage, is_on_ground, image, player_image, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.damage = damage
        self.is_on_ground = is_on_ground
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.image = image
        self.player_image = player_image
        self.position = position

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def on_ground(self):
        return self.is_on_ground

    def set_on_ground(self, value):
        self.is_on_ground = value

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_player_image(self):
        return self.player_image

    def set_player_image(self, player_image):
        self.player_image = player_image

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position