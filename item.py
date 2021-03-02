import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, item_type, damage, defense, health, speed, length, hit_chance, is_on_ground, image, player_image, position, magic):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.item_type = item_type  # Can be weapon, wearable, potion, trinket
        self.damage = damage
        self.defense = defense
        self.health = health
        self.speed = speed
        self.length = length
        self.hit_chance = hit_chance
        self.is_on_ground = is_on_ground
        self.image = image
        self.player_image = player_image
        self.position = position
        self.rect = pygame.Rect(self.position[0] * 16, self.position[1] * 16, 16, 16)
        self.magic = magic  # if none, magic = None else ["DAMAGE", 2] / ["DEFENSE", 3] / ["HEALTH", 5] / ["SPEED", 3]

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_type(self):
        return self.item_type

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        magic_damage = 0
        if self.magic is not None and self.magic[0] == "DAMAGE":
            magic_damage = self.magic[1]
        return self.damage + magic_damage

    def set_defense(self, defense):
        self.defense = defense

    def get_defense(self):
        magic_defense = 0
        if self.magic is not None and self.magic[0] == "DEFENSE":
            magic_defense = self.magic[1]
        return self.defense + magic_defense

    def set_health(self, health):
        self.health = health

    def get_health(self):
        magic_health = 0
        if self.magic is not None and self.magic[0] == "HEALTH":
            magic_health = self.magic[1]
        return self.health + magic_health

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        magic_speed = 0
        if self.magic is not None and self.magic[0] == "SPEED":
            magic_speed = self.magic[1]
        return self.speed + magic_speed

    def get_length(self):
        return self.length

    def set_hit_chance(self, hit_chance):
        self.hit_chance = hit_chance

    def get_hit_chance(self):
        return self.hit_chance

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
        self.rect = pygame.Rect(self.position[0] * 16, self.position[1] * 16, 16, 16)

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def get_magic_type(self):
        if self.magic is not None:
            return self.magic[0]
        else:
            return None

    def get_magic(self):
        return self.magic

    def set_magic(self, magic):
        self.magic = magic

    # def get_weapon_damage(self):
    #     weapon_damage = self.get_damage()
    #     magic_damage = 0
    #     if self.get_magic_type() is not None:
    #         if self.get_magic_type() == "DAMAGE":
    #             magic_damage = self.get_magic()[1]
    #         else:
    #             pass
    #     else:
    #         pass
    #
    #     return weapon_damage + magic_damage
