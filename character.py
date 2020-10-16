import pygame


class Character:
    def __init__(self, identifier, image, name, health, is_dead, position, item):
        self.identifier = identifier
        self.name = name
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.is_dead = is_dead
        self.position = position
        self.item = item
        self.inventory = []
        self.damage = 4
        self.health = health
        self.type = "MOVE"
        self.value = [0, 0]
        self.xp = 0

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_identifier(self):
        return self.identifier

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_action(self):
        return self.type, self.value

    def get_health(self):
        return self.health

    def set_health(self, health):
        if health <= 0:
            self.health = 0
            self.is_dead = True
        else:
            self.health = health

    def get_damage(self):
        if self.item is not None:
            return self.item.get_damage()
        else:
            return self.damage

    def set_action(self, type, value):
        self.type = type
        self.value = value

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_item(self, item):
        self.inventory.append(item)

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        return item

    def get_equipped_item(self):
        return self.item

    def get_inventory(self):
        return self.inventory

    def set_item(self, item):
        if item in self.inventory:
            self.item = item
            self.set_image(item.get_player_image())
        else:
            pass

    def get_xp(self):
        return self.xp

    def add_xp(self, num):
        self.xp += num