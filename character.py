import pygame
import numpy as np


class Character:
    def __init__(self, identifier, image, name, health, accuracy, agility, attack, speed, is_dead, position, item, starting_xp, death_xp):
        self.identifier = identifier
        self.name = name
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.is_dead = is_dead
        self.position = position
        self.item = item
        self.inventory = []
        self.damage = 4
        self.hit_chance = 80
        self.health = health
        self.current_health = health
        self.accuracy = accuracy
        self.agility = agility
        self.attack = attack
        self.speed = speed
        self.type = "MOVE"
        self.value = [0, 0]

        self.death_xp = death_xp  # Amount of xp that is dropped when they are killed
        self.character_xp = starting_xp
        if self.character_xp < 100:
            self.current_rank = 0
            self.next_xp_rank = 100
        else:
            self.current_rank = int(np.log(self.character_xp/100)/np.log(2)) + 1
        self.next_rank = self.current_rank + 1




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

    def add_health(self, added_health):
        self.health += added_health
        self.current_health += added_health

    def get_current_health(self):
        return self.current_health

    def add_current_health(self, added_health):
        self.current_health += added_health
        if self.current_health <= 0:
            self.current_health = 0
            self.is_dead = True

    def get_accuracy(self):
        return self.accuracy

    def get_accuracy_bonus(self):
        accuracy_modifier = 5
        return self.accuracy * accuracy_modifier

    def get_item_hit_chance(self):
        if self.item is not None:
            item_hit_chance = self.item.get_hit_chance()
            return item_hit_chance
        else:
            return self.hit_chance

    def add_accuracy(self, added_accuracy):
        self.accuracy += added_accuracy

    def get_agility(self):
        return self.agility

    def get_agility_bonus(self):
        agility_modifier = 5
        return self.agility * agility_modifier

    def add_agility(self, added_agility):
        self.agility += added_agility

    def get_attack(self):
        return self.attack

    def get_attack_bonus(self):
        attack_modifier = 1
        return self.attack * attack_modifier

    def add_attack(self, added_attack):
        self.attack += added_attack

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_item_damage(self):
        if self.item is not None:
            item_damage = self.item.get_damage()
            if self.item.get_magic_type() == "DAMAGE":
                magic_damage = self.item.get_magic()[1]
            else:
                magic_damage = 0

            return item_damage + magic_damage
        else:
            return self.damage

    def set_action(self, type, value):
        self.type = type
        self.value = value

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def print_stats(self):
        print(self.get_name() + "'s Stats:")
        print("Rank: " + str(self.get_rank()))
        print("Max Health: " + str(self.get_health()))
        print("Accuracy: " + str(self.get_accuracy()))
        print("Agility: " + str(self.get_agility()))
        print("Attack: " + str(self.get_attack()))

        # Works with items and inventory
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


    # XP RANKING METHODS
    def get_xp(self):
        return self.character_xp

    def get_rank(self):
        return self.current_rank

    def add_xp(self, num):
        self.character_xp += num
        if self.character_xp < 100:
            self.current_rank = 1
        if self.character_xp >= 100:
            self.current_rank = int(np.log(self.character_xp / 100) / np.log(2)) + 1

    def get_death_xp(self):
        return self.death_xp

    def update(self):


        pass  # Stuff that can happen every round for later use like health regen or something
        # Try two Ways for magical stuff:
        # 1) put code in constructor of item
        # 2) set certain properties like damage_buff, healing_buff, speed_buff, and stuff
