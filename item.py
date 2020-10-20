import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, item_type, damage, is_on_ground, image, player_image, position, magic):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.item_type = item_type  # Can be weapon, wearable, potion, trinket
        self.damage = damage
        self.is_on_ground = is_on_ground
        self.image = image
        self.player_image = player_image
        self.position = position
        self.rect = pygame.Rect(self.position[0] * 16, self.position[1] * 16, 16, 16)
        self.magic = magic


    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_type(self):
        return self.item_type

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def on_ground(self):
        return self.is_on_ground

    def set_on_ground(self, value):
        self.is_on_ground = value
        self.rect = pygame.Rect(self.position[0] * 16, self.position[1] * 16, 16, 16)

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

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def get_magic_type(self):
        return self.magic[0]

    def get_magic(self):
        return self.magic

    def set_magic(self, magic):
        self.magic = magic

