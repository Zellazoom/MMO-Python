import pygame
import numpy as np
import random
from insertion_sort import insertion_sort


class Character:
    def __init__(self, identifier, image, name, max_health, defense, accuracy, agility, attack, speed, is_dead, position, starting_weapon, starting_xp, death_xp):
        self.identifier = identifier
        self.name = name
        self.image = image
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.is_dead = is_dead
        self.position = position
        self.damage = 4
        self.hit_chance = 80
        self.max_health = max_health
        self.current_health = max_health
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        elif self.current_health < 0:
            self.current_health = 0
        self.defense = defense
        self.accuracy = accuracy
        self.agility = agility
        self.attack = attack
        self.speed = speed
        self.type = "MOVE"
        self.value = [0, 0]

        self.start_round = None
        self.round_counter = 0

        self.death_xp = death_xp  # Amount of xp thelmet is dropped when they are killed
        self.character_xp = starting_xp
        if self.character_xp < 100:
            self.current_rank = 0
            self.next_xp_rank = 100
        else:
            self.current_rank = int(np.log(self.character_xp/100)/np.log(2)) + 1
        self.next_rank = self.current_rank + 1

        self.helmet = None
        self.necklace = None
        self.armor = None
        self.boots = None

        self.no_new_weapon = True
        self.weapon = starting_weapon
        self.shield = None
        self.trinket = None
        self.active_potion = None

        # self.item = item
        self.defensive_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield, self.trinket, self.active_potion]
        self.all_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield, self.trinket, self.active_potion]
        #self.defensive_items = [self.shield, self.boots, self.armor, self.helmet, self.trinket, self.active_potion]
        #self.defensive_item_types = ["SHIELD", "BOOTS", "ARMOR", "HELMET", "TRINKET", "ACTIVE_POTION"]
        self.defensive_item_types = ["HELMET", "NECKLACE", "ARMOR", "BOOTS", "WEAPON", "SHIELD", "TRINKET", "ACTIVE_POTION"]

        # First wearable in each slot is equipped (One of each)
        self.wearable_inventory = {"HELMET": [], "NECKLACE": [], "ARMOR": [], "BOOTS": []}  # helmet, necklace, armor, shoes

        # First item in each slot is equipped (One of each)
        self.weapon_inventory = {"WEAPON": [], "SHIELD": []}  # Weapons, shields

        # No equipped items. All items in this are a one time use
        self.potion_inventory = {"DAMAGE_POTION": [], "HEALING_POTION": [],
                                 "SPEED_POTION": [], "DEFENSE_POTION": []}  # Damage, healing, speed

        # 1 Trinket can be equipped at a time from any of the groups
        self.trinket_inventory = {"DAMAGE_TRINKET": [], "HEALING_TRINKET": [],
                                  "SPEED_TRINKET": [], "DEFENSE_TRINKET": []}  # Damage, healing, speed

        self.inventory_types = ["WEARABLE", "WEAPON", "POTION", "TRINKET"]
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
        return self.current_health

    def add_max_health(self, added_health):
        self.max_health += added_health

    def get_current_health(self):
        return self.current_health

    def add_current_health(self, added_health):
        self.current_health += added_health
        if self.current_health <= 0:
            self.current_health = 0
            self.is_dead = True

    def compute_defense(self):
        defense = 0
        self.defensive_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield,
                                self.trinket, self.active_potion]
        for item in self.defensive_items:
            if item is not None:
                try:
                    defense += item.get_defense()
                except:
                    pass
            else:
                pass
        defense = self.defense + defense
        return defense

    def get_defense(self):
        defense = self.compute_defense()
        return defense

    def compute_speed(self):
        speed = 0
        self.all_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield,
                                self.trinket, self.active_potion]
        for item in self.all_items:
            if item is not None:
                try:
                    speed += item.get_speed()
                except:
                    pass
            else:
                pass
        speed = self.speed + speed
        return speed

    def get_speed(self):
        speed = self.compute_speed()
        return speed

    def compute_damage(self):
        damage = 0
        self.all_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield, self.trinket,
                          self.active_potion]
        for item in self.all_items:
            if item is not None:
                damage += item.get_damage()
            else:
                pass
        damage = self.damage + damage
        return damage

    def get_damage(self):
        damage = self.compute_damage()
        return damage

    def set_speed(self, speed):
        self.speed = speed

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

    def set_has_new_weapon(self, boolean):
        self.no_new_weapon = boolean

    def get_has_new_weapon(self):
        return self.no_new_weapon

    def set_action(self, type, value):
        self.type = type
        self.value = value

    def set_position(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)

    def get_position(self):
        return self.position

    def level_up(self):
        print(self.get_name() + " leveled up!")
        self.add_max_health(5)
        self.current_health = self.max_health
        print("+5 Max Health")
        increased_stat = random.randint(1, 3)
        if increased_stat == 1:
            self.add_accuracy(1)
            print("+1 Accuracy")
        elif increased_stat == 2:
            self.add_agility(1)
            print("+1 Agility")
        else:
            self.add_attack(1)
            print("+1 Attack")
        self.print_stats()

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
                if len(list) == 1:
                    setattr(self, item.get_type().lower(), item)
                    list.remove(item)
                    list.insert(0, item)
                    print("SETTING_ITEM: " + item.get_name())
                    if item.get_type() == "WEAPON":
                        self.set_image(item.get_player_image())
                    break
            except:
                pass

        weapon_list = self.get_weapons()
        new_list = []
        for i in weapon_list:
            new_list.append([i, i.get_damage()])

        self.inventory[1]["WEAPON"] = insertion_sort(new_list)


    def set_item(self, item):
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                if item in list:
                    setattr(self, item.get_type().lower(), item)
                    list.remove(item)
                    list.insert(0, item)
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

    def set_active_potion(self, item):
        self.active_potion = item
        self.start_round = self.round_counter

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

    def get_equipped_helmet(self):
        if self.helmet is not None:
            return self.helmet
        else:
            return None

    def get_equipped_necklace(self):
        if self.necklace is not None:
            return self.necklace
        else:
            return None

    def get_equipped_armor(self):
        if self.armor is not None:
            return self.armor
        else:
            return None

    def get_equipped_boots(self):
        if self.boots is not None:
            return self.boots
        else:
            return None

    def get_equipped_trinket(self):
        if self.trinket is not None:
            return self.trinket
        else:
            return None

    def get_active_potion(self):
        if self.active_potion is not None:
            return self.active_potion
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

    def get_helmets(self):
        helmets_dict = self.inventory[0]
        helmets_list = helmets_dict.get("HELMET")
        return helmets_list

    def get_necklaces(self):
        necklace_dict = self.inventory[0]
        necklace_list = necklace_dict.get("NECKLACE")
        return necklace_list

    def get_armor(self):
        armor_dict = self.inventory[0]
        armor_list = armor_dict.get("ARMOR")
        return armor_list

    def get_boots(self):
        boots_dict = self.inventory[0]
        boots_list = boots_dict.get("BOOTS")
        return boots_list

    def get_all_potions(self):
        potions_list = []
        potions_dict = self.inventory[2]
        potions_list.extend(potions_dict.get("DAMAGE_POTION"))
        potions_list.extend(potions_dict.get("HEALING_POTION"))
        potions_list.extend(potions_dict.get("SPEED_POTION"))
        potions_list.extend(potions_dict.get("DEFENSE_POTION"))
        return potions_list

    def get_damage_potions(self):
        potions_list = []
        potions_dict = self.inventory[2]
        potions_list.extend(potions_dict.get("DAMAGE_POTION"))
        return potions_list
    def get_healing_potions(self):
        potions_list = []
        potions_dict = self.inventory[2]
        potions_list.extend(potions_dict.get("HEALING_POTION"))
        return potions_list
    def get_speed_potions(self):
        potions_list = []
        potions_dict = self.inventory[2]
        potions_list.extend(potions_dict.get("SPEED_POTION"))
        return potions_list
    def get_defense_potions(self):
        potions_list = []
        potions_dict = self.inventory[2]
        potions_list.extend(potions_dict.get("DEFENSE_POTION"))
        return potions_list

    def get_all_trinkets(self):
        trinkets_list = []
        trinkets_dict = self.inventory[3]
        trinkets_list.extend(trinkets_dict.get("DAMAGE_TRINKET"))
        trinkets_list.extend(trinkets_dict.get("HEALING_TRINKET"))
        trinkets_list.extend(trinkets_dict.get("SPEED_TRINKET"))
        trinkets_list.extend(trinkets_dict.get("DEFENSE_TRINKET"))
        return trinkets_list

    def get_damage_trinkets(self):
        trinkets_list = []
        trinkets_dict = self.inventory[3]
        trinkets_list.extend(trinkets_dict.get("DAMAGE_TRINKET"))
        return trinkets_list

    def get_healing_trinkets(self):
        trinkets_list = []
        trinkets_dict = self.inventory[3]
        trinkets_list.extend(trinkets_dict.get("HEALING_TRINKET"))
        return trinkets_list

    def get_speed_trinkets(self):
        trinkets_list = []
        trinkets_dict = self.inventory[3]
        trinkets_list.extend(trinkets_dict.get("SPEED_TRINKET"))
        return trinkets_list

    def get_defense_trinkets(self):
        trinkets_list = []
        trinkets_dict = self.inventory[3]
        trinkets_list.extend(trinkets_dict.get("DEFENSE_TRINKET"))
        return trinkets_list

    def set_item(self, item):
        for dict in self.inventory:
            try:
                list = dict.get(item.get_type())
                if item in list:
                    setattr(self, item.get_type().lower(), item)
                    list.remove(item)
                    list.insert(0, item)
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
        self.print_inventory()
        self.compute_defense()
        self.compute_damage()
        self.compute_speed()

    def get_max_weapon_damage(self):
        weapon_list = self.get_weapons()
        max_weapon = weapon_list[0]
        return max_weapon

    def print_inventory(self):
        for type in self.inventory_types:
            self.print_inventory_of_type(type)

    def print_inventory_of_type(self, type_of_inventory):
        tab_space = 2
        if type_of_inventory is not None:
            if type_of_inventory == "WEARABLE":
                dictionary = self.wearable_inventory
            elif type_of_inventory == "WEAPON":
                dictionary = self.weapon_inventory
            elif type_of_inventory == "POTION":
                dictionary = self.potion_inventory
            elif type_of_inventory == "TRINKET":
                dictionary = self.trinket_inventory
            else:
                print("There was no type: " + str(type_of_inventory))
                self.print_inventory()
                return
            length_of_string = 20
            lengths = {key: len(value) for key, value in dictionary.items()}
            max_length = lengths.get(max(lengths, key=lengths.get)) + 1
            for i in range(max_length):
                temp = '|'
                if i != 0:
                    for key, val in dictionary.items():
                        if val is not None:
                            stat = 0
                            if len(val) > i - 1:
                                if val[i - 1].get_type() == "WEAPON":
                                    stat = val[i - 1].get_damage()
                                elif val[i - 1].get_type() in self.defensive_item_types:
                                    stat = val[i - 1].get_defense()
                                temp += " " * tab_space + "•" + str(val[i - 1].get_name()) + "." * (length_of_string - len(str(val[i - 1].get_name())) - tab_space - 1 - len(str(stat))) + str(stat)
                            else:
                                temp += " " * length_of_string
                        else:
                            temp += " " * length_of_string
                        temp += "|"

                else:
                    for key, val in dictionary.items():
                        if len(key) > i:
                            if key == "WEAPON" or key == "SHIELD":
                                temp += str(key) + "S:" + " " * (length_of_string - len(str(key)) - 2)
                            else:
                                temp += str(key) + ":" + " " * (length_of_string - len(str(key))-1)
                        else:
                            temp += " " * length_of_string + "|"
                        temp += "|"
                print(temp)
        else:
            self.print_inventory()


    # XP RANKING METHODS
    def get_xp(self):
        return self.character_xp

    def get_rank(self):
        return self.current_rank

    def add_xp(self, num):
        before_rank = self.current_rank
        self.character_xp += num
        if self.character_xp < 100:
            self.current_rank = 1
        if self.character_xp >= 100 * self.current_rank:
            self.current_rank = int(np.log(self.character_xp / 100) / np.log(2)) + 1
        if self.current_rank > before_rank:
            self.level_up()

    def get_death_xp(self):
        return self.death_xp

    def update_self(self):
        self.defensive_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield,
                                self.trinket, self.active_potion]
        self.all_items = [self.helmet, self.necklace, self.armor, self.boots, self.weapon, self.shield, self.trinket,
                          self.active_potion]
        if self.start_round is not None:
            print(str(self.round_counter - self.start_round) + "=================================")
        if self.start_round is not None and (self.round_counter - self.start_round) < self.active_potion.get_length():  # 10 is how many rounds, make into variable if works
            if self.active_potion.item_type == "DAMAGE_POTION":
                pass
            elif self.active_potion.item_type == "HEALING_POTION":
                self.add_current_health(self.active_potion.get_health())
            elif self.active_potion.item_type == "SPEED_POTION":
                pass
            elif self.active_potion.item_type == "DEFENSE_POTION":
                pass
            else:
                print("WARNING: POTIONS ARE NOT UPDATING ACCORDING TO PLAN")
        else:
            self.start_round = None
            self.drop_item(self.active_potion)
            self.active_potion = None

        self.round_counter += 1
        # pass  # Stuff that can happen every round for later use like health regen or something
        # Try two Ways for magical stuff:
        # 1) put code in constructor of item
        # 2) set certain properties like damage_buff, healing_buff, speed_buff, and stuff