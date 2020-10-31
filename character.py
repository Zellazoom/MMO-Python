import pygame
import numpy as np


class Character:
    def __init__(self, identifier, image, name, health, defense, accuracy, agility,
                 attack, speed, is_dead, position, starting_weapon, starting_xp, death_xp):
        self.identifier = identifier
        self.name = name
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.is_dead = is_dead
        self.position = position
        self.damage = 4
        self.hit_chance = 80
        self.health = health
        if self.health > 100:
            self.health = 100
        elif self.health < 0:
            self.health = 0
        self.current_health = health
        self.defense = defense
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

        self.hat = None
        self.necklace = None
        self.armor = None
        self.boots = None

        self.weapon = starting_weapon
        self.shield = None
        self.trinket = None
        self.active_potion = None

        # self.item = item
        self.inventory = []
        self.defensive_items = [self.shield, self.boots, self.armor, self.hat, self.trinket, self.active_potion]
        #self.defensive_items = ["SHIELD", "BOOTS", "ARMOR", "HAT", "TRINKET", "ACTIVE_POTION"]

        # First wearable in each slot is equipped (One of each)
        self.wearable_inventory = {"HAT": [], "NECKLACE": [], "ARMOR": [], "BOOTS": []}  # Hat, necklace, armor, shoes

        # First item in each slot is equipped (One of each)
        self.weapon_inventory = {"WEAPON": [], "SHIELD": []}  # Weapons, shields

        # No equipped items. All items in this are a one time use
        self.potion_inventory = {"DAMAGE_POTION": [], "HEALING_POTION": [],
                                 "SPEED_POTION": [], "DEFENCE_POTION": []}  # Damage, healing, speed

        # 1 Trinket can be equipped at a time from any of the groups
        self.trinket_inventory = {"DAMAGE_TRINKET": [], "HEALING_TRINKET": [],
                                  "SPEED_TRINKET": [], "DEFENCE_TRINKET": []}  # Damage, healing, speed

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
        self.current_health += added_health

    def get_current_health(self):
        return self.current_health

    def add_current_health(self, added_health):
        self.current_health += added_health
        if self.current_health <= 0:
            self.current_health = 0
            self.is_dead = True

    def compute_defense(self):
        self.defensive_items = [self.shield, self.boots, self.armor, self.hat, self.trinket, self.active_potion]
        defense = 0
        for item in self.defensive_items:
            if item is not None:
                try:
                    defense += item.get_defense()
                    print(str(item.get_name()) + str(item.get_defense()))
                except:
                    pass
            else:
                pass
        print(defense)
        self.defense = defense

    def get_defense(self):
        return self.defense

    def get_accuracy(self):
        return self.accuracy

    def get_accuracy_bonus(self):
        accuracy_modifier = 5
        return self.accuracy * accuracy_modifier

    def get_weapon_hit_chance(self):
        if self.weapon is not None:
            weapon_hit_chance = self.weapon.get_hit_chance()
            return weapon_hit_chance
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

    def get_weapon_damage(self):
        if self.weapon is not None:
            weapon_damage = self.weapon.get_damage()
            magic_damage = 0
            if self.weapon.get_magic_type() is not None:
                if self.weapon.get_magic_type() == "DAMAGE":
                    magic_damage = self.weapon.get_magic()[1]
                else:
                    pass
            else:
                pass

            return weapon_damage + magic_damage
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


    # Works with items and inventory  ------------------------------
    def get_item(self, item):
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                list.append(item)
                dict[item.get_type()] = list
            except:
                pass

    def drop_item(self, item):
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

    def get_equipped_weapon(self):
        if self.weapon is not None:
            return self.weapon
        else:
            return None

    def get_equipped_shield(self):
        if self.shield is not None:
            return self.shield
        else:
            return None

    def get_inventory(self):
        return self.inventory

    def get_weapons(self):
        weapon_dict = self.inventory[1]
        weapon_list = weapon_dict.get("WEAPON")
        return weapon_list

    def get_shields(self):
        shield_dict = self.inventory[1]
        shield_list = shield_dict.get("SHIELD")
        return shield_list

    def set_item(self, item):
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                if item in list:
                    setattr(self, item.get_type().lower(), item)
                    print("SETTING_ITEM: " + item.get_name())
                    if item.get_type() == "WEAPON":
                        self.set_image(item.get_player_image())
                    break
                elif list == self.trinket_inventory:
                    self.trinket = item
                    break
                else:
                    print("Item can not be equipped")
            except:
                pass
        self.compute_defense()

    def print_inventory(self):
        for dict in self.inventory:
            for key, val in dict.items():
                print(key + ": ")
                for i in val:
                    print("    " + i.get_name())

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

    def update_self(self):
        self.defensive_items = [self.shield, self.boots, self.armor, self.hat, self.trinket, self.active_potion]

        # pass  # Stuff that can happen every round for later use like health regen or something
        # Try two Ways for magical stuff:
        # 1) put code in constructor of item
        # 2) set certain properties like damage_buff, healing_buff, speed_buff, and stuff