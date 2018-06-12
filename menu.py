from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
from fonts import *
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
        pg.display.set_caption(str(self.game.clock.get_fps()))
        self.bg_image.fill(MENU_BG_COLOUR)
        if self.in_battle:
            self.bg_rect.x = BATTLE_SCREEN_WIDTH
        else:
            self.bg_rect.x = WIDTH

        for count, pokemon in enumerate(self.game.player.cap_pokemon):
            pokemon.number = count + 1

            y_location = HEADER_SPACE + int(
                (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon) * (count + 0.5))
            x_location = MENU_WIDTH // 4

            pokemon.rect.centerx = x_location
            pokemon.rect.centery = y_location
            self.bg_image.blit(pokemon.image, pokemon.rect)
            vertical_spacing = (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon)

            if vertical_spacing < CIRCLE_RADIUS*2:
                self.circle_radius = vertical_spacing//2
            else:
                self.circle_radius = CIRCLE_RADIUS

            pg.draw.circle(self.bg_image, BLUE,
                           (x_location,
                            y_location),
                           self.circle_radius,
                           CIRCLE_WIDTH)
            # vertical_spacing = (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon)
            draw_text2(self.bg_image, name_lines_surfaces[POKEMON_LIST.index(pokemon.name)], x_location + STATS_OFFSET, y_location - 40)
            draw_text2(self.bg_image, type_lines_surfaces[TYPE_LIST.index(pokemon.type)], x_location + STATS_OFFSET, y_location - 20)
            draw_text2(self.bg_image, health_line, x_location + STATS_OFFSET, y_location - 0)
            draw_text2(self.bg_image, kills_line, x_location + STATS_OFFSET, y_location + 20)
