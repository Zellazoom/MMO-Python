from character import Character
import pygame


class Player(pygame.sprite.Sprite, Character):
    def __init__(self, identifier, image, name, health, speed, is_dead, position, item, starting_xp, death_xp):
        Character.__init__(self, identifier, image, name, health, speed, is_dead, position, item, starting_xp, death_xp)
        pygame.sprite.Sprite.__init__(self)
