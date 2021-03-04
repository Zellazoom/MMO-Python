import pygame
import sys
import os
from player import Player
from enemy import Enemy
from item import Item
from portal import Portal
from graphics import Graphics
from pygame.locals import *
import collections
from copy import copy
import random
import time

clock = pygame.time.Clock()

pygame.init()  # initiates pygame
FPS = 60

pygame.display.set_caption('Pygame Platform')

WINDOW_SIZE = (1200, 800)
SCREEN_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface(SCREEN_SIZE)  # used as the surface for rendering, which is scaled
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
graphics_folder = os.path.join(game_folder, 'Graphics')
music_folder = os.path.join(game_folder, 'music')

map_level = 1
# Gets the basic game music going (Commented Cause Im listening to music. Uncomment if forgotten)
# pygame.mixer.init()
# pygame.mixer.music.load(os.path.join(music_folder, 'GameMusic_1.mp3'))
# pygame.mixer.music.play(-1, 0.0)

graphics = Graphics(graphics_folder, display, FPS)

dirt_img = pygame.image.load(os.path.join(img_folder, 'dirt.png'))
castle_img = pygame.image.load(os.path.join(img_folder, 'castleCenter.png'))
portal_img = pygame.image.load(os.path.join(img_folder, 'portal.jpg'))
item_img = pygame.image.load(os.path.join(img_folder, 'Chest.png')).convert_alpha()
player_img = graphics.Player.get_model()
spear_character_img = pygame.image.load(os.path.join(img_folder, 'MainCharacterSpear.png')).convert_alpha()
enemy1_img = graphics.Enemy1.get_model()
enemy2_img = graphics.Enemy2.get_model()


def split(word):
    return [char for char in word]


def enemy_values(enemy_type, difficulty):  # enemy_type 1-2 & difficulty 1-3
    enemy_identifier = "Enemy" + str(enemy_type)
    enemy_image = enemy1_img if enemy_type == 1 else enemy2_img
    enemy_name = "Enemy_" + str(random.randint(0, 10000))
    enemy_max_health = 10 * difficulty
    enemy_defense = 1 * difficulty
    enemy_accuracy = difficulty / 2
    enemy_agility = -2 + difficulty
    enemy_attack = difficulty / 2
    enemy_speed = max(1, difficulty - 1)
    enemy_is_dead = False
    enemy_position = [0, 0]
    if enemy_type == 1:
        enemy_type = 2
    elif enemy_type == 2:
        enemy_type = 1
    else:
        enemy_type = enemy_type
    enemy_starting_weapon = enemy_weapon_creator(enemy_type, difficulty, map_level)
    enemy_starting_xp = 0
    enemy_death_xp = 40 * difficulty
    enemy_characteristics = [enemy_identifier, enemy_image, enemy_name, enemy_max_health, enemy_defense, enemy_accuracy,
                             enemy_agility, enemy_attack, enemy_speed, enemy_is_dead, enemy_position,
                             enemy_starting_weapon, enemy_starting_xp, enemy_death_xp]
    return enemy_characteristics


def enemy_weapon_creator(enemy_type, difficulty, level):
    enemy_weapon_name = "Spear"
    enemy_weapon_item_type = "WEAPON"
    enemy_weapon_damage = (enemy_type * difficulty * level) + 6
    enemy_weapon_defense = 0
    enemy_weapon_health = 0
    enemy_weapon_speed = 0
    enemy_weapon_length = 0
    enemy_weapon_hit_chance = min(80 + (2 * enemy_type * difficulty * level), 100)
    enemy_weapon_is_on_ground = False
    enemy_weapon_image = item_img
    enemy_weapon_player_image = spear_character_img
    enemy_weapon_position = [0, 0]
    if enemy_type == 1:
        enemy_weapon_magic = None
    elif enemy_type == 2:
        if difficulty == 1:
            enemy_weapon_magic = ["DAMAGE", 1]
        elif difficulty == 2:
            enemy_weapon_magic = ["DAMAGE", 2]
        elif difficulty == 3:
            enemy_weapon_magic = ["DAMAGE", 3]
        else:
            enemy_weapon_magic = ["DAMAGE", difficulty * enemy_type]
    else:
        enemy_weapon_magic = None
    enemy_item = Item(enemy_weapon_name, enemy_weapon_item_type, enemy_weapon_damage, enemy_weapon_defense,
                      enemy_weapon_health, enemy_weapon_speed, enemy_weapon_length, enemy_weapon_hit_chance,
                      enemy_weapon_is_on_ground, enemy_weapon_image, enemy_weapon_player_image, enemy_weapon_position,
                      enemy_weapon_magic)
    return enemy_item


def map_item_creator(level):
    map_1_drop = [19, 38, 57, 76, 95, 96, 97, 100]
    # map_2_drop = [12, 12, 12, 12, 12, 14, 14, 12]
    map_2_drop = [12, 24, 36, 48, 60, 74, 88, 100]
    # map_3_drop = [10, 10, 10, 10, 10, 20, 20, 10]
    map_3_drop = [10, 20, 30, 40, 50, 70, 90, 100]
    if level == 1:
        map_drop = map_1_drop
    elif level == 2:
        map_drop = map_2_drop
    elif level == 3:
        map_drop = map_3_drop
    else:
        map_drop = map_1_drop

    rand_int1 = random.randint(1, 100)
    rand_int2 = random.randint(1, 100)
    rand_int3 = random.randint(1, 2)
    rand_int = rand_int1 if rand_int3 == 1 else rand_int2
    if rand_int <= map_drop[0]:  # Spear -------------------------------------------------------------------------------
        item_name = "Spear"
        item_item_type = "WEAPON"
        item_damage = 8*level
        item_defense = 0
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = min(100, 90+(2*level))
        item_is_on_ground = True
        item_image = item_img
        item_player_image = spear_character_img
        item_magic = ["DAMAGE", level*5]

    elif map_drop[0] < rand_int <= map_drop[1]:  # Shield---------------------------------------------------------------
        item_name = "Shield"
        item_item_type = "SHIELD"
        item_damage = 0
        item_defense = 2*level
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = ["DEFENSE", level * 2]

    elif map_drop[1] < rand_int <= map_drop[2]:  # Helmet---------------------------------------------------------------
        item_name = "Helmet"
        item_item_type = "HELMET"
        item_damage = 0
        item_defense = level
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = None

    elif map_drop[2] < rand_int <= map_drop[3]:  # Armor----------------------------------------------------------------
        item_name = "Armor"
        item_item_type = "ARMOR"
        item_damage = 0
        item_defense = 3*level
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = None

    elif map_drop[3] < rand_int <= map_drop[4]:  # Boots----------------------------------------------------------------
        item_name = "Boots"
        item_item_type = "BOOTS"
        item_damage = 0
        item_defense = level
        item_health = 0
        item_speed = level
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = None

    elif map_drop[4] < rand_int <= map_drop[5]:  # Potions--------------------------------------------------------------
        rand_choice = random.randint(1, 4)
        item_name = "Potion"

        if rand_choice == 1:  # Damage potion
            item_item_type = "DAMAGE_POTION"
            item_damage = 5*level
            item_defense = 0
            item_health = 0
            item_speed = 0

        elif rand_choice == 2:  # Defense potion
            item_item_type = "DEFENSE_POTION"
            item_damage = 0
            item_defense = 5*level
            item_health = 0
            item_speed = 0

        elif rand_choice == 3:  # Healing potion
            item_item_type = "HEALING_POTION"
            item_damage = 0
            item_defense = 0
            item_health = 5*level
            item_speed = 0

        else:  # Speed potion
            item_item_type = "SPEED_POTION"
            item_damage = 0
            item_defense = 0
            item_health = 0
            item_speed = level

        item_length = 10 * level
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = None

    elif map_drop[5] < rand_int <= map_drop[6]:  # Trinkets-------------------------------------------------------------
        item_name = "Trinket"
        item_item_type = "TRINKET"
        item_damage = 0
        item_defense = 0
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = ["DAMAGE", int(2 * level)]

    elif map_drop[6] < rand_int <= map_drop[7]:  # Necklace-------------------------------------------------------------
        item_name = "Necklace"
        item_item_type = "NECKLACE"
        item_damage = 0
        item_defense = 0
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = ["HEALTH", 2*level]

    else:
        item_name = "Necklace"
        item_item_type = "NECKLACE"
        item_damage = 0
        item_defense = 0
        item_health = 0
        item_speed = 0
        item_length = 0
        item_hit_chance = 0
        item_is_on_ground = True
        item_image = item_img
        item_player_image = None
        item_magic = ["HEALTH", 2 * level]
        print("Problem with drop chances")

    item_position = [0, 0]
    item_to_return = Item(item_name, item_item_type, item_damage, item_defense, item_health, item_speed, item_length,
                          item_hit_chance, item_is_on_ground, item_image, item_player_image, item_position, item_magic)
    return item_to_return


def load_new_map(path, level):
    f = open(path + str(level) + '.txt', 'r')
    data = f.read()
    f.close()

    data = data.split('\n')

    items_set = []
    portal_set = []
    enemies_set_1 = []
    enemies_set_2 = []

    c = 0
    item_count = 0
    enemy1_count = 0
    enemy2_count = 0
    portal_count = 0

    f = open(path + '_' + str(level) + '.txt', 'w')
    f.seek(0, 0)
    for row in data:
        r = 0
        for k in row:
            if str(k) == str(2):
                new_item = map_item_creator(map_level)
                new_item.set_position([r, c])
                items_set.append(new_item)
                block = split(row)
                block[r] = "0"
                row = block
                row = ''.join(row)
                item_count += 1

            if str(k) == "*":
                portal_new_name = "Portal " + str(map_level)
                new_portal = Portal(portal_new_name, [r, c], portal_img)
                portal_set.append(new_portal)
                row = ''.join(row)
                portal_count += 1

            if str(k) == str(3):
                values = enemy_values(2, 1)
                enemy2 = Enemy(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                               values[8], values[9], values[10], values[11], values[12], values[13])
                enemy2.set_position([r, c])
                enemies_set_2.append(enemy2)
                block = split(row)
                block[r] = "0"
                row = block
                row = ''.join(row)
                enemy2_count += 1

            if str(k) == str(4):
                values = enemy_values(1, 2)
                enemy1 = Enemy(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                               values[8], values[9], values[10], values[11], values[12], values[13])
                enemy1.set_position([r, c])
                enemies_set_1.append(enemy1)
                block = split(row)
                block[r] = "0"
                row = block
                row = ''.join(row)
                enemy1_count += 1

            else:
                pass
            r += 1
        f.write(str(row) + '\n')
        c += 1
    f.close()
    return items_set, portal_set, enemies_set_1, enemies_set_2

# name, item_type, damage, defense, health, speed, length, hit_chance, is_on_ground, image, player_image, position,
# magic):


# items = []
# item2 = Item("Spear", "WEAPON", 1, 0, 0, 0, 0, 90, True, item_img, spear_character_img, [0, 0], None)  # [10, 6]
# item3 = Item("Spear", "WEAPON", 1, 0, 0, 0, 0, 90, True, item_img, spear_character_img, [0, 0], None)
# item4 = Item("Spear", "WEAPON", 1, 0, 0, 0, 0, 90, True, item_img, spear_character_img, [0, 0], None)
# item5 = Item("Spear", "WEAPON", 1, 0, 0, 0, 0, 90, True, item_img, spear_character_img, [0, 0], None)
# item3 = Item("Leather Armor", "ARMOR", 0, 5, 0, 0, 0, True, item_img, None, [0, 0], None)  # [20, 3]"Boots", "BOOTS",
# 0, 1, 0, True, item_img, None, [0, 0], None
# item3 = Item("Attack Necklace", "NECKLACE", 0, 0, 0, 0, 0, 0, True, item_img, None, [0, 0], ["DAMAGE", 2])
# item3 = Item("Hth_Potion", "HEALING_POTION", 0, 0, 0, 0, 10, 0, True, item_img, None, [0, 0], ["HEALTH", 5])
# item3 = Item("Spd_Potion", "SPEED_POTION", 0, 0, 0, 0, 20, 0, True, item_img, None, [0, 0], ["SPEED", 1])
# item4 = Item("Shield", "SHIELD", 0, 3, 0, 0, 0, 0, True, item_img, None, [0, 0], None)  # [15, 6]
# item5 = Item("Boots", "BOOTS", 0, 1, 0, 0, 0, 0, True, item_img, None, [0, 0], None)  # [20, 6]
# item6 = Item("Helmet", "HELMET", 0, 1, 0, 0, 0, 0, True, item_img, None, [0, 0], None)  # [15, 6]
# item7 = Item("Boots", "BOOTS", 0, 2, 0, 0, 0, 0, True, item_img, None, [0, 0], None)  # [20, 6]

# item1 = Item("Spear", "WEAPON", 5, 0, 0, 0, 0, 90, False, item_img, spear_character_img, [0, 0], ["DAMAGE", 0])

#
# items.append(item2)
# items.append(item3)
# items.append(item4)
# items.append(item5)
# items.append(item6)
# items.append(item7)

players = []
player1 = Player("Player", player_img, "Andrew", 12, 0, -1, 0, -1, 1, False, [6, 6], None, 201, 20)
player2 = Player("Player", player_img, "Yeet",   100, 0,  1, 0,  1, 2, False, [1, 3], None, 201, 20)
players.append(player2)

items, portals, enemies1, enemies2 = load_new_map('map', map_level)
objects = [player2]
characters = [player2]

enemies = []
for i in items:
    objects.append(i)
for i in portals:
    objects.append(i)
for i in enemies1:
    objects.append(i)
    characters.append(i)
    enemies.append(i)
for i in enemies2:
    objects.append(i)
    characters.append(i)
    enemies.append(i)


true_scroll = [0, 0]
speed = 2
drop_proc = 10


def get_map_dimensions(path, level):
    f = open(path + '_' + str(level) + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    temp_game_map = []
    for row in data:
        temp_game_map.append(list(row))
    map_dim = [len(temp_game_map[0])-1, len(temp_game_map)-1]
    return map_dim


def load_map(path, level):
    f = open(path + "_" + str(level) + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    temp_game_map = []
    for row in data:
        temp_game_map.append(list(row))
    temp_game_map = [[j for j in k] for k in temp_game_map]  # --------------------------------------------------------------
    return temp_game_map


def get_pixels_from_chunks(chunks):
    return int(16 * chunks)


def get_chunks_from_pixels(pixels):
    return int(pixels / 16)


def collision_test(rect, tiles):
    hit_list = []
    for tile_block in tiles:
        if rect.colliderect(tile_block):
            hit_list.append(tile_block)
    return hit_list


def check_open_square(coordinates):
    x_coord, y_coord = coordinates[0], coordinates[1]
    if x_coord <= map_dimensions[0] and y_coord <= map_dimensions[1]:
        if str(game_map[y_coord][x_coord]) == "0":
            return True
        elif str(game_map[y_coord][x_coord]) == "1":
            return False
        elif str(game_map[y_coord][x_coord]) == "2":
            return False
        elif str(game_map[y_coord][x_coord]) == "3":
            return False
        elif str(game_map[y_coord][x_coord]) == "4":
            return False
        elif str(game_map[y_coord][x_coord]) == "*":
            return False
    else:
        return False


def find_objects_around(coordinates):
    # Checks the full 8 squares around the player
    list_of_objects = []
    list_of_coords = [[coordinates[0], coordinates[1] + 1], [coordinates[0] + 1, coordinates[1] + 1],
                      [coordinates[0] + 1, coordinates[1]], [coordinates[0] + 1, coordinates[1] - 1],
                      [coordinates[0], coordinates[1] - 1], [coordinates[0] - 1, coordinates[1] - 1],
                      [coordinates[0] - 1, coordinates[1]], [coordinates[0] - 1, coordinates[1] + 1]]
    for object_around in objects:
        for coord in list_of_coords:
            if object_around.get_position() == [coord[0], coord[1]]:
                list_of_objects.append(object_around)
            else:
                pass
    return list_of_objects


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    movement[0], movement[1] = get_pixels_from_chunks(movement[0]), get_pixels_from_chunks(movement[1])
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile_block in hit_list:
        if movement[0] > 0:
            rect.right = tile_block.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile_block.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile_block in hit_list:
        if movement[1] > 0:
            rect.bottom = tile_block.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile_block.bottom
            collision_types['top'] = True
    return rect, collision_types


def find_enemy_in_area(person):
    # returns an enemy of the opposite side
    list_of_objects = find_objects_around(person.get_position())
    if isinstance(person, Player):
        # enemy is enemy
        for object_in_game in list_of_objects:
            if isinstance(object_in_game, Enemy):
                return object_in_game
    if isinstance(person, Enemy):
        # enemy is player
        for object_in_game in list_of_objects:
            if isinstance(object_in_game, Player):
                return object_in_game
    else:
        return None


# Function to find the shortest path between
# a given source cell to a destination cell.
def bfs(grid, start_1, end):  # takes grid, (x, y), [x,y]
    grid = [list(map(str, row)) for row in grid]
    width, height = len(grid[0]), len(grid)
    wall, clear, player, enemy, item_tile, portal_tile = '1', '0', '2', '3', '4', '*'  # These numbers do not specify what enemy
    start = (start_1[0], start_1[1])
    queue = collections.deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x_val, y_val = path[-1]
        if grid[y_val][x_val] != "1" and y_val == end[1] and x_val == end[0]:
            return path

        if grid[end[1]][end[0]] == "0":
            for x2, y2 in ((x_val + 1, y_val), (x_val - 1, y_val), (x_val, y_val + 1), (x_val, y_val - 1)):
                if 0 <= x2 < width and 0 <= y2 < height and \
                        grid[y2][x2] not in (wall, player, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

        if grid[end[1]][end[0]] == "1":
            return -1

        if grid[end[1]][end[0]] == "2":
            for x2, y2 in ((x_val + 1, y_val), (x_val - 1, y_val), (x_val, y_val + 1), (x_val, y_val - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

                else:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        if grid[end[1]][end[0]] == "3":
            for x2, y2 in ((x_val + 1, y_val), (x_val - 1, y_val), (x_val, y_val + 1), (x_val, y_val - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

                else:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))


        if grid[end[1]][end[0]] == "4":
            for x2, y2 in ((x_val + 1, y_val), (x_val - 1, y_val), (x_val, y_val + 1), (x_val, y_val - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

                else:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        if grid[end[1]][end[0]] == "*":
            for x2, y2 in ((x_val + 1, y_val), (x_val - 1, y_val), (x_val, y_val + 1), (x_val, y_val - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, item_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

                else:
                    if 0 <= x2 < width and 0 <= y2 < height and \
                            grid[y2][x2] not in (wall, player, enemy, item_tile, portal_tile) and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

    print("Invalid location: " + str(end))
    return -1


def find_enemies_by_range(object_in_game):
    list_of_all_enemies = []
    if isinstance(object_in_game, Player):
        for enemy in enemies:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), enemy.get_position())
            list_of_all_enemies.append([enemy, len(path_1) - 1])

    if isinstance(object_in_game, Enemy):
        for player in players:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), player.get_position())
            list_of_all_enemies.append([player, len(path_1) - 1])

    sorted_list = sorted(list_of_all_enemies, key=lambda x_element: x_element[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def find_enemies_in_range(object_in_game, length):
    list_of_all_enemies = []
    if isinstance(object_in_game, Player):
        for enemy in enemies:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), enemy.get_position())
            if len(path_1) <= length:
                # print("Enemy " + object.get_name() + " is " + str(len(path_1)) + "blocks away")
                list_of_all_enemies.append([enemy, len(path_1) - 1])
            else:
                pass

    if isinstance(object_in_game, Enemy):
        for player in players:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), player.get_position())
            # list_of_all_enemies.append([player, len(path_1) - 1])
            # print("Player " + object.get_name() + " is " + str(len(path_1)) + "blocks away")
            if len(path_1) <= length:
                list_of_all_enemies.append([player, len(path_1) - 1])
            else:
                pass

    sorted_list = sorted(list_of_all_enemies, key=lambda x_val: x_val[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def shortest_dist_to_enemy(object_in_game):
    list_of_all_enemies = []
    if isinstance(object_in_game, Player):
        for enemy in enemies:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), enemy.get_position())
            list_of_all_enemies.append([enemy, len(path_1) - 1])

    if isinstance(object_in_game, Enemy):
        for player in players:
            path_1 = bfs(game_map_clean, object_in_game.get_position(), player.get_position())
            list_of_all_enemies.append([player, len(path_1) - 1])

    sorted_list = sorted(list_of_all_enemies, key=lambda x_val: x_val[1])
    if len(sorted_list) != 0:
        newly_sorted_list = []
        for lists in sorted_list:
            newly_sorted_list.append(lists[1])
        length_away = newly_sorted_list[0] - 1
    else:
        length_away = float('inf')
    return length_away


def shortest_dist_to_item(object_in_game):
    list_of_all_items = []
    for item_tile in items:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), item_tile.get_position())
        list_of_all_items.append([item_tile, len(path_1) - 1])

    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])
    if len(sorted_list) != 0:
        newly_sorted_list = []
        for lists in sorted_list:
            newly_sorted_list.append(lists[1])
        length_away = newly_sorted_list[0] - 1
    else:
        length_away = float('inf')
    return length_away


def shortest_dist_to_portal(object_in_game):
    list_of_all_items = []
    for port in portals:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), port.get_position())
        list_of_all_items.append([port, len(path_1) - 1])

    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])
    if len(sorted_list) != 0:
        newly_sorted_list = []
        for lists in sorted_list:
            newly_sorted_list.append(lists[1])
        length_away = newly_sorted_list[0] - 1
    else:
        length_away = float('inf')
    return length_away


def find_items_by_range(object_in_game):
    list_of_all_items = []
    for item_tile in items:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), item_tile.get_position())
        list_of_all_items.append([item_tile, len(path_1) - 1])

    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def find_items_in_range(object_in_game, length):
    list_of_all_items = []
    for item_tile in items:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), item_tile.get_position())
        if len(path_1) - 1 <= length:
            list_of_all_items.append([item_tile, len(path_1) - 1])
        else:
            pass
    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def find_item_in_area(person):
    # returns an enemy of the opposite side
    list_of_objects = find_objects_around(person.get_position())
    for object_in_game in list_of_objects:
        if isinstance(object_in_game, Item):
            return object_in_game
        else:
            pass
    else:
        return None


def find_portal_in_range(object_in_game, length):
    list_of_all_items = []
    for port in portals:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), port.get_position())
        if len(path_1) - 1 <= length:
            list_of_all_items.append([port, len(path_1) - 1])
        else:
            pass
    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def find_portal_in_area(person):
    # returns an enemy of the opposite side
    list_of_objects = find_objects_around(person.get_position())
    for object_in_game in list_of_objects:
        if isinstance(object_in_game, Portal):
            return object_in_game
        else:
            pass
    else:
        return None


def find_portal_by_range(object_in_game):
    list_of_all_items = []
    for port in portals:
        path_1 = bfs(game_map_clean, object_in_game.get_position(), port.get_position())
        list_of_all_items.append([port, len(path_1) - 1])

    sorted_list = sorted(list_of_all_items, key=lambda x_val: x_val[1])

    newly_sorted_list = []
    for lists in sorted_list:
        newly_sorted_list.append(lists[0])

    return newly_sorted_list


def teleport(person):
    person.set_position([1, 1])
    global map_level, game_map_clean, game_map, map_dimensions, items, portals, enemies1, enemies2, objects, characters,\
        enemies
    map_level = 2

    items, portals, enemies1, enemies2 = load_new_map('map', map_level)
    objects = [player2]
    characters = [player2]

    enemies = []
    for t in items:
        objects.append(t)
    for t in portals:
        objects.append(t)
    for t in enemies1:
        objects.append(t)
        characters.append(t)
        enemies.append(t)
    for t in enemies2:
        objects.append(t)
        characters.append(t)
        enemies.append(t)

    game_map_clean = load_map('map', map_level)
    game_map = load_map('map', map_level)
    map_dimensions = get_map_dimensions('map', map_level)


def if_action_teleport(object_in_game):
    if find_portal_in_area(object_in_game) is not None:
        teleport(object_in_game)
        global has_teleported
        has_teleported = True
    else:
        print("Not able to teleport")


def get_list_of_movement(player_pos, path_coords):
    list_of_movement = []
    for coord in path_coords[1:]:
        diff = [coord[0] - player_pos[0], coord[1] - player_pos[1]]
        player_pos = [coord[0] + player_pos[0], coord[1] + player_pos[1]]
        list_of_movement.append(diff)

    return list_of_movement


# END CODE FOR PLAYER TO CALL
def if_action_move(game_map_temp, object_in_game):
    current_position = object_in_game.get_position()
    value_of_action = object_in_game.get_action()[1]
    object_rect = object_in_game.get_rect()
    if current_position != value_of_action:
        list_of_positions = bfs(game_map_temp, current_position, value_of_action)
        if list_of_positions != -1:
            list_of_moving = get_list_of_movement(current_position, list_of_positions)
            if len(list_of_moving) != 0:
                new_coords = [current_position[0] + list_of_moving[0][0], current_position[1] + list_of_moving[0][1]]
                if check_open_square(new_coords):
                    object_new_pos = list_of_moving[0]
                    object_in_game.set_position(new_coords)
                    object_rect, collisions = move(object_rect, object_new_pos, tile_rectangles)

                    object_in_game.set_rect(object_rect)
                    list_of_moving.remove(list_of_moving[0])
                else:
                    object_in_game.set_action("STAY", object_in_game.get_position())

            else:
                object_in_game.set_action("STAY", object_in_game.get_position())

        else:
            pass
            print("Bot didn't Move. Invalid location")

    else:
        object_in_game.set_action("STAY", object_in_game.get_position())


def attack(attacker, attacked):
    damage = 0
    hit_percentage = attacker.get_weapon_hit_chance() + attacker.get_accuracy_bonus() - attacked.get_agility_bonus()
    # print("Hit Percentage:" + str(hit_percentage))
    # print("Item Damage:" + str(attacker.get_item_damage()))
    # print("Attack Bonus:" + str(attacker.get_attack_bonus()))
    # If the attack hits set the damage, otherwise it stays at 0
    if random.randint(1, 100) <= hit_percentage:
        damage = max(0, attacker.get_damage() + attacker.get_attack_bonus() - attacked.get_defense())
        # print(attacked.get_defense())
        # Checks for critical strike
        if random.randint(1, 10) <= (attacker.get_accuracy() - attacked.get_agility()):
            damage = damage * 1.5
            print(attacker.get_name() + " critically struck " + attacked.get_name() + " for " + str(damage) + " damage")
        else:
            print(attacker.get_name() + " hit " + attacked.get_name() + " for " + str(damage) + " damage.")
    else:
        print(attacked.get_name() + " dodged the attack from " + attacker.get_name() + ".")
    attacked.add_current_health(-damage)
    print(attacked.get_name() + " has " + str(attacked.get_current_health()) + " health left.")


def if_action_attack(object_in_game):
    action, attacked = object_in_game.get_action()
    attack(object_in_game, attacked)

    if attacked.is_dead:
        if isinstance(attacked, Player):
            object_in_game.add_xp(attacked.get_death_xp())

            try:
                print(attacked.get_name() + " IS DEAD+++++++++++++++")
                # Drop Equipped Item
                try:
                    random_drop_roll = random.randint(1, 10)
                    if random_drop_roll < drop_proc:
                        if attacked.get_equipped_weapon() is not None:
                            item_from_drop = copy(attacked.get_equipped_weapon())
                            attacked.drop_item(item_from_drop)
                            item_from_drop.set_position(attacked.get_position())
                            item_from_drop.set_on_ground(True)

                            items.append(item_from_drop)
                            objects.append(item_from_drop)
                            [x_drop, y_drop] = attacked.get_position()
                            game_map[y_drop][x_drop] = "4"
                    else:
                        pass
                finally:
                    print("Attack did not go well... Check code")

                players.remove(attacked)
                characters.remove(attacked)
                objects.remove(attacked)
            finally:
                pass


        if isinstance(attacked, Enemy):
            print("Player's xp before kill: " + str(object_in_game.get_xp()) + ": " + str(object_in_game.get_rank()))
            object_in_game.add_xp(attacked.get_death_xp())
            print("Player's xp after kill: " + str(object_in_game.get_xp()) + ": " + str(object_in_game.get_rank()))
            try:
                # Drop Equipped Item
                try:
                    random_drop_roll = random.randint(1, 10)
                    if random_drop_roll < drop_proc:
                        if attacked.get_equipped_weapon() is not None:
                            item_from_drop = copy(attacked.get_equipped_weapon())
                            attacked.drop_item(item_from_drop)
                            item_from_drop.set_position(attacked.get_position())
                            item_from_drop.set_on_ground(True)

                            items.append(item_from_drop)
                            objects.append(item_from_drop)
                            [x_drop, y_drop] = attacked.get_position()
                            game_map[y_drop][x_drop] = "4"
                    else:
                        pass
                finally:
                    pass

                print(attacked.get_name() + " IS DEAD+++++++++++++++")
                enemies.remove(attacked)
                characters.remove(attacked)
                objects.remove(attacked)
            finally:
                pass
        else:
            pass
    else:
        pass


def pickup(person, pickup_item):
    person.get_item(pickup_item)
    pickup_item.set_on_ground(False)
    person.print_inventory()
    items.remove(pickup_item)
    objects.remove(pickup_item)
    person.set_has_new_weapon(True)


def if_action_pickup(object_in_game):
    action, item = object_in_game.get_action()
    pickup(object_in_game, item)


def drop(person, dropping_item):
    person.drop_item(dropping_item)


def if_action_drop(object_in_game):
    action, item = object_in_game.get_action()
    drop(object_in_game, item)


def activate(person, activate_item):
    person.set_active_potion(activate_item)


def if_action_activate(object_in_game):
    action, item = object_in_game.get_action()
    activate(object_in_game, item)


def rotate_list(given_list, num):
    given_list = given_list[num:] + given_list[:num]
    return given_list


def equip(person, equipping_item):
    person.set_item(equipping_item)
    person.set_has_new_weapon(False)


def if_action_equip(object_in_game):
    action, item = object_in_game.get_action()
    equip(object_in_game, item)


def get_player_decision(player):
    # Compare and equip weapons/shields code:
    a = True if player.get_equipped_weapon() is not None else False
    if a:
        b = len(player.get_weapons()) > 1
        c = player.get_has_new_weapon()
        item_to_equip = player.get_max_weapon_damage()
        d = False if item_to_equip == player.get_equipped_weapon() else True
        var = a and b and c and d
    else:
        var = False

    # try:
    # Checking immediate area: 1 block in any direction
    if find_enemy_in_area(player) is not None:
        enemy_to_attack = find_enemy_in_area(player)
        player.set_action("ATTACK", enemy_to_attack)

    elif find_item_in_area(player) is not None:
        item_to_pickup = find_item_in_area(player)
        player.set_action("PICKUP", item_to_pickup)

    elif find_portal_in_area(player) is not None:
        player.set_action("TELEPORT", 0)

    # Equipping first gear
    elif player.get_equipped_weapon() is None and len(player.get_weapons()) != 0:
        item_to_equip = player.get_weapons()[0]
        player.set_action("EQUIP", item_to_equip)

    elif player.get_equipped_shield() is None and len(player.get_shields()) != 0:
        item_to_equip = player.get_shields()[0]
        player.set_action("EQUIP", item_to_equip)

    elif player.get_equipped_helmet() is None and len(player.get_helmets()) != 0:
        item_to_equip = player.get_helmets()[0]
        player.set_action("EQUIP", item_to_equip)

    elif player.get_equipped_necklace() is None and len(player.get_necklaces()) != 0:
        item_to_equip = player.get_necklaces()[0]
        player.set_action("EQUIP", item_to_equip)

    elif player.get_equipped_trinket() is None and len(player.get_all_trinkets()) != 0:
        item_to_equip = player.get_all_trinkets()[0]
        player.set_action("EQUIP", item_to_equip)

    # Activating Health Potion
    elif player.get_active_potion() is None and len(player.get_healing_potions()) != 0 and player.get_health() < 55:
        item_to_activate = player.get_healing_potions()[0]
        player.set_action("ACTIVATE", item_to_activate)

    # Activating Speed Potion
    elif player.get_active_potion() is None and len(player.get_speed_potions()) != 0:
        item_to_activate = player.get_speed_potions()[0]
        player.set_action("ACTIVATE", item_to_activate)

    # Equipping the better weapon
    elif var:
        item_to_equip = player.get_max_weapon_damage()
        player.set_action("EQUIP", item_to_equip)
        player.print_inventory()

    elif len(player.get_weapons()) > 3:
        weapons = player.get_weapons()
        player.set_action("DROP", weapons[len(weapons)-1])

    # This checks if enemies are closer than chest in the area
    elif (str(shortest_dist_to_item(player)) != 'inf' and str(shortest_dist_to_item(player)) != 'inf') and \
            (shortest_dist_to_enemy(player) <= shortest_dist_to_item(player)):
        target = find_enemies_by_range(player)
        player.set_action("MOVE", target[0].get_position())

    # Checks if there is items and goes for them
    elif len(find_items_by_range(player)) != 0:
        target = find_items_by_range(player)
        player.set_action("MOVE", target[0].get_position())

    # Check if there is enemies and goes for them
    elif len(find_enemies_by_range(player)) != 0:
        target = find_enemies_by_range(player)
        player.set_action("MOVE", target[0].get_position())

    elif len(find_portal_by_range(player)) != 0:
        target = find_portal_by_range(player)
        player.set_action("MOVE", target[0].get_position())

    else:
        player.set_action("STAY", player.get_position())

    return player.get_action()


def get_enemy_decision(enemy):
    if find_enemy_in_area(enemy) is not None:
        enemy_to_attack = find_enemy_in_area(enemy)
        enemy.set_action("ATTACK", enemy_to_attack)

    elif len(find_enemies_in_range(enemy, 4)) != 0:
        target = find_enemies_in_range(enemy, 4)
        enemy.set_action("MOVE", target[0].get_position())

    # elif len(find_enemies_by_range(enemy)) != 0:
    #     target = find_enemies_by_range(enemy)
    #     enemy.set_action("MOVE", target[0].get_position())
    else:
        enemy.set_action("STAY", enemy.get_position())

    return enemy.get_action()


game_map_clean = load_map('map', map_level)
game_map = load_map('map', map_level)
map_dimensions = get_map_dimensions('map', map_level)
has_teleported = False

# Set up
counter = 0
counter_two = 0
turn_count = 0
while True:
    display.fill((146, 244, 255))
    game_loop_normal = True

    # true_scroll[0] += ((player1.get_rect().x + player2.get_rect().x)/2 - true_scroll[0] - 152) / 20
    # true_scroll[1] += ((player1.get_rect().y + player2.get_rect().y)/2 - true_scroll[1] - 106) / 20

    true_scroll[0] += (player2.get_rect().x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player2.get_rect().y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rectangles = []
    y = 0
    for layer in game_map_clean:
        x = 0
        for tile in layer:
            try:
                if int(tile) == 0:
                    display.blit(castle_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if int(tile) == 1:
                    display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if int(tile) != 0:
                    tile_rectangles.append(pygame.Rect(x * 16, y * 16, 16, 16))
            except ValueError:
                if str(tile) == "*":
                    display.blit(portal_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            x += 1
        y += 1

    if counter % FPS == 0:  # Main Decision Code here
        print("-----------------------NEW LOOP-----------------------------")
        for character in characters:
            character.update_self()
        for character in characters:  # For loop after this can double action

            if not game_loop_normal:
                break

            move_only = False
            # Testing speed
            if isinstance(character, Player):
                get_player_decision(character)

            if isinstance(character, Enemy):
                get_enemy_decision(character)

            # This is just printing player decision for now otherwise it gets cluttered
            object_position = character.get_position()
            type_of_action, value = character.get_action()
            # print(character.get_name() + " : " + str(type_of_action)  + " : " + str(object_position) + " : " +
            # str(character.get_current_health()))

            if isinstance(character, Player):
                print(character.get_name() + " : " + str(character.get_defense()) + " : " + str(
                    type_of_action) + " : " + str(object_position) + " : " + str(character.get_current_health()))
                # print("PLAYER SPEED: " + str(character.get_speed()))

            turn_range = 1
            if character.get_action()[0] == "MOVE" and character.get_speed() > 1:
                move_only = True
                path_2 = bfs(game_map_clean, character.get_position(), character.get_action()[1])
                turn_range = len(path_2)
                if turn_range >= character.get_speed():
                    turn_range = character.get_speed()
                else:
                    turn_range = turn_range
            else:
                move_only = False

            for i in range(turn_range):
                if isinstance(character, Player):
                    get_player_decision(character)

                if isinstance(character, Enemy):
                    get_enemy_decision(character)

                object_position = character.get_position()
                type_of_action, value = character.get_action()

                if type_of_action == "ATTACK" and not move_only:
                    if_action_attack(character)
                elif type_of_action == "MOVE":
                    if_action_move(game_map, character)
                elif type_of_action == "PICKUP" and not move_only:
                    if_action_pickup(character)
                elif type_of_action == "DROP" and not move_only:
                    if_action_drop(character)
                elif type_of_action == "EQUIP" and not move_only:
                    if_action_equip(character)
                elif type_of_action == "ACTIVATE" and not move_only:
                    if_action_activate(character)
                elif type_of_action == "TELEPORT" and not move_only:
                    if_action_teleport(character)
                    if has_teleported:
                        game_loop_normal = False
                        has_teleported = False
                        break
                    else:
                        pass
                else:
                    pass

                if not game_loop_normal:
                    break

                game_map = load_map('map', map_level)
                if isinstance(character, Player):
                    if character.is_dead:
                        players.remove(character)
                        characters.remove(character)
                        objects.remove(character)
                    else:
                        display.blit(character.get_image(),
                                     (character.get_rect().x - scroll[0], character.get_rect().y - scroll[1]))
                        new_x, new_y = character.get_position()
                        game_map[new_y][new_x] = "2"

                if isinstance(character, Enemy):
                    if character.is_dead:
                        enemies.remove(character)
                        characters.remove(character)
                        objects.remove(character)
                    else:
                        display.blit(character.get_image(),
                                     (character.get_rect().x - scroll[0], character.get_rect().y - scroll[1]))
                        new_x, new_y = character.get_position()
                        game_map[new_y][new_x] = "3"

                for item_box in items:
                    if item_box.on_ground():
                        display.blit(item_box.get_image(),
                                     (item_box.get_rect().x - scroll[0], item_box.get_rect().y - scroll[1]))
                        new_x, new_y = item_box.get_position()
                        game_map[new_y][new_x] = "4"
                    else:
                        items.remove(item_box)
                        objects.remove(item_box)

                for all_objects in objects:
                    display.blit(all_objects.get_image(),
                                 (all_objects.get_rect().x - scroll[0], all_objects.get_rect().y - scroll[1]))
        turn_count += 1
        counter = 0

    # Add item code
    for all_objects in objects:
        display.blit(all_objects.get_image(), (all_objects.get_rect().x - scroll[0],
                                               all_objects.get_rect().y - scroll[1]))

    graphics.animate(counter_two, scroll, players, enemies)


    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == VIDEORESIZE:
        #     screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        #     display = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        #     screen.blit(pygame.transform.scale(screen, event.dict['size']), (0, 0))
        #     display.blit(pygame.transform.scale(display, event.dict['size']), (0, 0))
        #     pygame.display.update()
        #     counter += 1
        #     clock.tick(FPS)



    if counter_two == FPS:
        counter_two = 0

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    counter += 1
    counter_two += 1
    clock.tick(FPS)
