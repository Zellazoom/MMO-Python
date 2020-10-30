import pygame
import numpy as np


class Character:
    def __init__(self, identifier, image, name, health, speed, is_dead, position, item, starting_xp, death_xp):
        self.identifier = identifier
        self.name = name
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.is_dead = is_dead
        self.position = position
        self.damage = 4
        self.health = health

        # Added this in
        if self.health > 100:
            self.health = 100
        elif self.health < 0:
            self.health = 0

        self.speed = speed
        self.type = "MOVE"
        self.value = [0, 0]

        self.death_xp = death_xp  # Amount of xp that is dropped when they are killed
        self.character_xp = starting_xp
        if self.character_xp < 100:
            self.current_rank = 0
            self.next_xp_rank = 100
        else:
            self.current_rank = int(np.log(self.character_xp / 100) / np.log(2)) + 1
        self.next_rank = self.current_rank + 1

        # This sets up the inventory
        self.hat = None
        self.necklace = None
        self.armor = None
        self.boots = None

        self.weapon = None
        self.shield = None
        self.trinket = None

        self.item = item
        self.inventory = []

        # First wearable in each slot is equipped (One of each)
        self.wearable_inventory = {"HAT": [], "NECKLACE": [], "ARMOR": [], "BOOTS": []}  # Hat, necklace, armor, shoes

        # First item in each slot is equipped (One of each)
        self.weapon_inventory = {"WEAPON": [], "SHIELD": []}                            # Weapons, shields

        # No equipped items. All items in this are a one time use
        self.potion_inventory = {"DAMAGE_POTION": [], "HEALING_POTION": [], "SPEED_POTION": []}                # Damage, healing, speed

        # 1 Trinket can be equipped at a time from any of the groups
        self.trinket_inventory = {"DAMAGE_TRINKET": [], "HEALING_TRINKET": [], "SPEED_TRINKET": []}               # Damage, healing, speed

        self.inventory = [self.wearable_inventory, self.weapon_inventory, self.potion_inventory, self.trinket_inventory]


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
        if self.health <= 0:
            self.health = 0
            self.is_dead = True

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_damage(self):
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


    # Works with items and inventory  ------------------------------
    def get_item(self, item):
        #self.inventory.append(item)
        # START OF WEARABLE INVENTORY
        if item.get_type() == "HAT":
            self.wearable_inventory["HAT"].append(item)
        elif item.get_type() == "NECKLACE":
            self.wearable_inventory["NECKLACE"].append(item)
        elif item.get_type() == "ARMOR":
            self.wearable_inventory["ARMOR"].append(item)
        elif item.get_type() == "BOOTS":
            self.wearable_inventory["BOOTS"].append(item)
        # START OF WEAPON INVENTORY
        elif item.get_type() == "WEAPON":
            self.weapon_inventory["WEAPON"].append(item)
        elif item.get_type() == "SHIELD":
            self.weapon_inventory["SHIELD"].append(item)
        # START OF POTION INVENTORY
        elif item.get_type() == "DAMAGE_POTION":
            self.potion_inventory["DAMAGE_POTION"].append(item)
        elif item.get_type() == "HEALING_POTION":
            self.potion_inventory["HEALING_POTION"].append(item)
        elif item.get_type() == "SPEED_POTION":
            self.potion_inventory["SPEED_POTION"].append(item)
        # START OF TRINKET INVENTORY
        elif item.get_type() == "DAMAGE_TRINKET":
            self.potion_inventory["DAMAGE_TRINKET"].append(item)
        elif item.get_type() == "HEALING_TRINKET":
            self.potion_inventory["HEALING_TRINKET"].append(item)
        elif item.get_type() == "SPEED_TRINKET":
            self.potion_inventory["SPEED_TRINKET"].append(item)


    def drop_item(self, item):
        # if item in self.inventory:
        #     self.inventory.remove(item)
        # This might delete all of the instances of the item
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                for objects in list:
                    if objects == item:
                        list.remove(item)
                        break
                    else:
                        pass
            except:
                pass
        return item


    # def get_equipped_item(self):
    #     return self.item
    def get_equipped_weapon(self):
        return self.weapon

    # Returns a list of dictionaries right now
    def get_inventory(self):
        return self.inventory

    def get_weapons(self):
        return self.weapon_inventory["WEAPONS"]

    def set_item(self, item):
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                for objects in list:
                    if objects == item:
                        list.remove(item)
                        break
                    else:
                        pass
            except:
                pass

        # if item in self.inventory:
        #     self.item = item
        #     self.set_image(item.get_player_image())
        # else:
        #     pass



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
