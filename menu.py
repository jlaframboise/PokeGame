# menu.py
# Jacob Laframboise
# June 14th, 2018
# This file holds the class for the menu

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
    '''A class to hold the methods and attributes to maintain a sidebar menu on the right of the main surface. '''

    def __init__(self, game):
        self.game = game
        self.bg_image = pg.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.bg_image.fill(BLACK)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = WIDTH
        self.in_battle = False

    def update(self):
        '''A method to update the menu and redraw it each frame. '''
        pg.display.set_caption(str(self.game.clock.get_fps()))
        self.bg_image.fill(MENU_BG_COLOUR)
        # move the menu rect based on whether in battle or main game
        if self.in_battle:
            self.bg_rect.x = BATTLE_SCREEN_WIDTH
        else:
            self.bg_rect.x = WIDTH

        draw_text2(self.bg_image, small_title_font_surface, MENU_WIDTH / 2, HEADER_SPACE * .2)
        draw_text2(self.bg_image, small_name_font_surface, MENU_WIDTH / 2, HEADER_SPACE * .7)

        # for every pokemon the player has
        for count, pokemon in enumerate(self.game.player.cap_pokemon):
            pokemon.number = count + 1  # pokemon number not zero indexed

            # find y location that places them equidistant from eachother and centered vertically
            y_location = HEADER_SPACE + int(
                (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon) * (count + 0.5))
            x_location = MENU_WIDTH // 4

            pokemon.rect.centerx = x_location
            pokemon.rect.centery = y_location
            self.bg_image.blit(pokemon.image, pokemon.rect)
            vertical_spacing = (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon)

            # shrink radius if the number of pokemon gets large
            if vertical_spacing < CIRCLE_RADIUS * 2:
                self.circle_radius = vertical_spacing // 2
            else:
                self.circle_radius = CIRCLE_RADIUS

            # draw the circles
            pg.draw.circle(self.bg_image, BLUE,
                           (x_location,
                            y_location),
                           self.circle_radius,
                           CIRCLE_WIDTH)
            # vertical_spacing = (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon)

            # draw the respective text for the pokemon based on attributes.
            draw_text2(self.bg_image, name_lines_surfaces[POKEMON_LIST.index(pokemon.name)], x_location + STATS_OFFSET,
                       y_location - 40)
            draw_text2(self.bg_image, type_lines_surfaces[TYPE_LIST.index(pokemon.type)], x_location + STATS_OFFSET,
                       y_location - 20)
            draw_text2(self.bg_image, health_lines[pokemon.kills], x_location + STATS_OFFSET, y_location - 0)
            draw_text2(self.bg_image, kills_lines[pokemon.kills], x_location + STATS_OFFSET, y_location + 20)
