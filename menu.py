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
        self.bg_image = pg.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.bg_image.fill(BLACK)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = WIDTH
        self.in_battle = False

        # for x in range(NUMBER_OF_CIRCLES):
        # pg.draw.circle(self.bg_image, BLUE,
        # (MENU_WIDTH // 2,
        # HEADER_SPACE + int((MENU_HEIGHT - HEADER_SPACE) // NUMBER_OF_CIRCLES * (x + 0.5))),
        # CIRCLE_RADIUS,
        # CIRCLE_WIDTH)

    def update(self):
        self.bg_image.fill(BLACK)
        if self.in_battle:
            self.bg_rect.x = BATTLE_SCREEN_WIDTH
        else:
            self.bg_rect.x = WIDTH

        for count, pokemon in enumerate(self.game.player.cap_pokemon):
            y_location = HEADER_SPACE + int(
                (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon) * (count + 0.5))

            pokemon.rect.centerx = MENU_WIDTH // 2
            pokemon.rect.centery = y_location
            self.bg_image.blit(pokemon.image, pokemon.rect)
            pg.draw.circle(self.bg_image, BLUE,
                           (MENU_WIDTH // 2,
                            y_location),
                           CIRCLE_RADIUS,
                           CIRCLE_WIDTH)
