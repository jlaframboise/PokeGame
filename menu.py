from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
import pygame as pg

vec = pg.math.Vector2


class Menu:
    def __init__(self, game):
        self.game = game
        self.image = pg.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH


    def draw(self):
        pass