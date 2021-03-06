from character import Character
import pygame


class Player(pygame.sprite.Sprite, Character):
    def __init__(self, identifier, image, name, max_health, defense, accuracy, agility, attack, speed, is_dead, position, item, starting_xp, death_xp):
        Character.__init__(self, identifier, image, name, max_health, defense, accuracy, agility, attack, speed, is_dead, position, item, starting_xp, death_xp)
        pygame.sprite.Sprite.__init__(self)
