import pygame, sys, os
from player import Player
from enemy import Enemy
from item import Item
from graphics import Graphics
from pygame.locals import *
import collections
from copy import copy

clock = pygame.time.Clock()

pygame.init()  # initiates pygame
FPS = 60

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface((600, 400))  # used as the surface for rendering, which is scaled
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
graphics_folder = os.path.join(game_folder, 'Graphics')

graphics = Graphics(graphics_folder, display, FPS)

dirt_img = pygame.image.load(os.path.join(img_folder, 'dirt.png'))
castle_img = pygame.image.load(os.path.join(img_folder, 'castleCenter.png'))
item_img = pygame.image.load(os.path.join(img_folder, 'Chest.png')).convert_alpha()
player_img = graphics.Player.get_model()
spear_character_img = pygame.image.load(os.path.join(img_folder, 'MainCharacterSpear.png')).convert_alpha()
enemy1_img = graphics.Enemy1.get_model()
enemy2_img = graphics.Enemy2.get_model()


items = []
item1 = Item("SPEAR", 6, True, item_img, spear_character_img, [10, 6])
item2 = Item("SPEAR2", 6, False, item_img, spear_character_img, [0, 0])
print(item2.is_on_ground)
items.append(item1)

enemies = []
enemy1 = Enemy("Enemy1", enemy1_img, "ENEMY", 20, False, [1, 6], item2)
enemy2 = Enemy("Enemy2", enemy2_img, "ENEMY", 10, False, [30, 6], None)
enemies.append(enemy1)
enemies.append(enemy2)

players = []
player1 = Player("Player", player_img, "Andrew", 12, False, [6, 6], None)
player2 = Player("Player", player_img, "Yeet", 30, False, [7, 6], None)
#players.append(player1)
players.append(player2)


objects = [player2, enemy1, enemy2, item1]  # player1
characters = [player2, enemy1, enemy2] # enemy1

true_scroll = [0, 0]


def get_map_dimensions(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    map_dim = [len(game_map[0])-1, len(game_map)-1]
    return map_dim


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    game_map = [[int(j) for j in i] for i in game_map]
    return game_map


game_map_clean = load_map('map')
game_map = load_map('map')
map_dimensions = get_map_dimensions('map')



def get_pixels_from_chunks(chunks):
    return int(16 * chunks)


def get_chunks_from_pixels(pixels):
    return int(pixels / 16)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def check_open_square(coordinates):
    x, y = coordinates[0], coordinates[1]
    if x <= map_dimensions[0] and y <= map_dimensions[1]:
        if game_map[y][x] == 0:
            return True
        elif game_map[y][x] == 1:
            return False
        elif game_map[y][x] == 2:
            return False
        elif game_map[y][x] == 3:
            return False
        elif game_map[y][x] == 4:
            return False
    else:
        return False


def find_objects_around(coordinates):
    # Checks the full 8 squares around the player
    list_of_objects = []
    list_of_coords =[]
    list_of_coords.append([coordinates[0], coordinates[1]+1])
    list_of_coords.append([coordinates[0]+1, coordinates[1] + 1])
    list_of_coords.append([coordinates[0]+1, coordinates[1]])
    list_of_coords.append([coordinates[0]+1, coordinates[1] - 1])
    list_of_coords.append([coordinates[0], coordinates[1] - 1])
    list_of_coords.append([coordinates[0]-1, coordinates[1] - 1])
    list_of_coords.append([coordinates[0]-1, coordinates[1]])
    list_of_coords.append([coordinates[0]-1, coordinates[1] + 1])
    for object in objects:
        for coord in list_of_coords:
            if object.get_position() == [coord[0], coord[1]]:
                list_of_objects.append(object)
            else:
                pass
    return list_of_objects


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    movement[0], movement[1] = get_pixels_from_chunks(movement[0]), get_pixels_from_chunks(movement[1])
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def find_enemy_in_area(person):
    # returns an enemy of the opposite side
    list_of_objects = find_objects_around(person.get_position())
    if isinstance(person, Player):
        # enemy is enemy
        for object in list_of_objects:
            if isinstance(object, Enemy):
                return object
    if isinstance(person, Enemy):
        # enemy is player
        for object in list_of_objects:
            if isinstance(object, Player):
                return object
    else:
        return None


# Function to find the shortest path between
# a given source cell to a destination cell.
def bfs(grid, start_1, end):  # takes grid, (x, y), [x,y]
    grid = [list(map(str, row)) for row in grid]
    width, height = len(grid[0]), len(grid)
    wall, clear, player, enemy, item = '1', '0', '2', '3', '4'
    start = (start_1[0], start_1[1])
    queue = collections.deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] != "1" and y == end[1] and x == end[0]:
            return path

        if grid[end[1]][end[0]] == "0":
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != enemy and grid[y2][x2] != item and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

        if grid[end[1]][end[0]] == "1":
            return -1

        if grid[end[1]][end[0]] == "2":
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != enemy and grid[y2][x2] != item and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                else:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != enemy and grid[y2][x2] != item and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        if grid[end[1]][end[0]] == "3":
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != item and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                else:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != enemy and grid[y2][x2] != item and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

        if grid[end[1]][end[0]] == "4":
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if grid[y2][x2] == grid[end[1]][end[0]]:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != enemy and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                else:
                    if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and grid[y2][x2] != player and grid[y2][x2] != enemy and grid[y2][x2] != item and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))

    print("Invalid location: " + str(end))
    return -1


def find_enemies_by_range(object):
    list_of_all_enemies = []
    if isinstance(object, Player):
        for enemy in enemies:
            path_1 = bfs(game_map_clean, object.get_position(), enemy.get_position())
            list_of_all_enemies.append([enemy, len(path_1)-1])

    if isinstance(object, Enemy):
        for player in players:
            path_1 = bfs(game_map_clean, object.get_position(), player.get_position())
            list_of_all_enemies.append([player, len(path_1) - 1])

    sorted_list = sorted(list_of_all_enemies, key=lambda x: x[1])

    newly_sorted_list = []
    for list in sorted_list:
        newly_sorted_list.append(list[0])

    return newly_sorted_list


def find_items_by_range(object):
    list_of_all_items = []
    for item in items:
        path_1 = bfs(game_map_clean, object.get_position(), item.get_position())
        list_of_all_items.append([item, len(path_1)-1])
    sorted_list = sorted(list_of_all_items, key=lambda x: x[1])

    newly_sorted_list = []
    for list in sorted_list:
        newly_sorted_list.append(list[0])

    return newly_sorted_list


def find_item_in_area(person):
    # returns an enemy of the opposite side
    list_of_objects = find_objects_around(person.get_position())
    for object in list_of_objects:
        if isinstance(object, Item):
            return object
        else:
            pass
    else:
        return None


def get_list_of_movement(player_pos, path_coords):  # , set_dest
    list_of_movement = []
    for coord in path_coords[1:]:
        diff = [coord[0] - player_pos[0], coord[1] - player_pos[1]]
        player_pos = [coord[0] + player_pos[0], coord[1] + player_pos[1]]
        list_of_movement.append(diff)

    return list_of_movement


# END CODE FOR PLAYER TO CALL
def if_action_move(game_map, object):
    object_position = object.get_position()
    value = object.get_action()[1]
    object_rect = object.get_rect()
    if object_position != value:
        list_of_positions = bfs(game_map, object_position, value)
        if list_of_positions != -1:
            list_of_movement = get_list_of_movement(object_position, list_of_positions)
            if len(list_of_movement) != 0:
                new_coords = [object_position[0] + list_of_movement[0][0], object_position[1] + list_of_movement[0][1]]
                if check_open_square(new_coords):
                    object_new_pos = list_of_movement[0]
                    object.set_position(new_coords)
                    object_rect, collisions = move(object_rect, object_new_pos, tile_rects)  # , collisions

                    object.set_rect(object_rect)
                    list_of_movement.remove(list_of_movement[0])
                else:
                    object.set_action("STAY", object.get_position())

            else:
                object.set_action("STAY", object.get_position())

        else:
            print("Bot didn't Move. Invalid location")

    else:
        object.set_action("STAY", object.get_position())


def attack(attacker, attacked):
    damage = attacker.get_damage()
    health = attacked.get_health()
    attacked.set_health((health - damage))


def if_action_attack(object):
    action, attacked = object.get_action()
    attack(object, attacked)

    if attacked.is_dead:
        if isinstance(attacked, Player):
            try:
                print(attacked.get_name() + " IS DEAD+++++++++++++++")
                # Drop Equipped Item
                try:
                    if attacked.get_equipped_item() is not None:
                        the_item = attacked.get_equipped_item()
                        the_item.set_position(attacked.get_position())
                        items.append(the_item)
                        objects.append(the_item)
                        attacked.drop_item(the_item)
                except:
                    print("Something happened")

                players.remove(attacked)
                characters.remove(attacked)
                objects.remove(attacked)
            except:
                pass
        if isinstance(attacked, Enemy):

            try:
                # Drop Equipped Item
                try:
                    if attacked.get_equipped_item() is not None:
                        dropped_item = copy(attacked.get_equipped_item())
                        attacked.drop_item(dropped_item)
                        dropped_item.set_position(attacked.get_position())
                        dropped_item.set_on_ground(True)

                        items.append(dropped_item)
                        objects.append(dropped_item)
                except:
                    pass

                print(attacked.get_name() + " IS DEAD+++++++++++++++")
                enemies.remove(attacked)
                characters.remove(attacked)
                objects.remove(attacked)
            except:
                pass
        else:
            pass
    else:
        pass


def pickup(person, pickup_item):
    person.get_item(pickup_item)
    pickup_item.set_on_ground = False
    try:
        items.remove(pickup_item)
        objects.remove(pickup_item)
    except:
        print("Item is already removed Welp")


def if_action_pickup(object):
    action, item = object.get_action()
    pickup(object, item)


def rotate_list(list, num):
    list = list[num:] + list[:num]
    return list


def equip(person, equipping_item):
    person.set_item(equipping_item)


def if_action_equip(object):
    action, item = object.get_action()
    equip(object, item)


def get_player_decision(player):
    try:
        if find_item_in_area(player) is not None:
            item_to_pickup = find_item_in_area(player)
            player.set_action("PICKUP", item_to_pickup)

        elif player.get_equipped_item() is None and len(player.get_inventory()) != 0:
            item_to_equip = player.get_inventory()[0]
            player.set_action("EQUIP", item_to_equip)

        elif len(find_items_by_range(player)) != 0:
            target = find_items_by_range(player)
            player.set_action("MOVE", target[0].get_position())

        elif find_enemy_in_area(player) is not None:
            enemy_to_attack = find_enemy_in_area(player)
            player.set_action("ATTACK", enemy_to_attack)

        elif len(find_enemies_by_range(player)) != 0:
            target = find_enemies_by_range(player)
            player.set_action("MOVE", target[0].get_position())

        else:
            player.set_action("STAY", player.get_position())

        return player.get_action()
    except:
        print("Object is dead")


def get_enemy_decision(enemy):
    try:
        if find_enemy_in_area(enemy) is not None:
            enemy_to_attack = find_enemy_in_area(enemy)
            enemy.set_action("ATTACK", enemy_to_attack)
        elif len(find_enemies_by_range(enemy)) != 0:
            target = find_enemies_by_range(enemy)
            enemy.set_action("MOVE", target[0].get_position())
        else:
            enemy.set_action("STAY", enemy.get_position())

        return enemy.get_action()

    except:
        print("Object is dead")

# Set up
counter = 0
counter_two = 0
turn_count = 0
while True:
    display.fill((146, 244, 255))

    # BOT PROCESS CODE
    # END BOT PROCESS CODE

    # true_scroll[0] += ((player1.get_rect().x + player2.get_rect().x)/2 - true_scroll[0] - 152) / 20
    # true_scroll[1] += ((player1.get_rect().y + player2.get_rect().y)/2 - true_scroll[1] - 106) / 20

    true_scroll[0] += (player2.get_rect().x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player2.get_rect().y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map_clean:
        x = 0
        for tile in layer:
            if tile == 0:
                display.blit(castle_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == 1:
                display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != 0:
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    if counter % FPS == 0:  # Main Desicion Code here
        for character in characters:
            if isinstance(character, Player):
                get_player_decision(character)
            if isinstance(character, Enemy):
                get_enemy_decision(character)
            object_position = character.get_position()
            type_of_action, value = character.get_action()
            print(character.get_name() + " : " + str(turn_count) + " : " + str(type_of_action)  + " : " + str(object_position)+ " : " + str(character.get_health()))

            if type_of_action == "ATTACK":
                if_action_attack(character)
            if type_of_action == "MOVE":
                if_action_move(game_map, character)
            if type_of_action == "PICKUP":
                if_action_pickup(character)
            if type_of_action == "EQUIP":
                if_action_equip(character)

            game_map = load_map('map')
            if isinstance(character, Player):
                if character.is_dead:
                    players.remove(character)
                    characters.remove(character)
                    objects.remove(character)
                else:
                    display.blit(character.get_image(), (character.get_rect().x - scroll[0], character.get_rect().y - scroll[1]))
                    new_x, new_y = character.get_position()
                    game_map[new_y][new_x] = 2

            if isinstance(character, Enemy):
                if character.is_dead:
                    enemies.remove(character)
                    characters.remove(character)
                    objects.remove(character)
                else:
                    display.blit(character.get_image(), (character.get_rect().x - scroll[0], character.get_rect().y - scroll[1]))
                    new_x, new_y = character.get_position()
                    game_map[new_y][new_x] = 3

            for item in items:
                if item.on_ground():
                    display.blit(item.get_image(), (item.get_rect().x - scroll[0], item.get_rect().y - scroll[1]))
                    new_x, new_y = item.get_position()
                    game_map[new_y][new_x] = 4
                else:
                    try:
                        items.remove(item)
                        objects.remove(item)
                    except:
                        pass
        turn_count += 1
        counter = 0

    # Add item code
    for all_objects in objects:
        display.blit(all_objects.get_image(), (all_objects.get_rect().x - scroll[0], all_objects.get_rect().y - scroll[1]))

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
