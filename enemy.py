from character import Character
import pygame


class Enemy(pygame.sprite.Sprite, Character):
    def __init__(self, identifier, image, name, health, is_dead, position, item):
        Character.__init__(self, identifier, image, name, health, is_dead, position, item)
        pygame.sprite.Sprite.__init__(self)
