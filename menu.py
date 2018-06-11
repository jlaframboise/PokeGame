from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
import pygame as pg

vec = pg.math.Vector2

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, col, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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
        self.bg_image.fill(BLACK)
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
            if vertical_spacing < CIRCLE_RADIUS:

                self.circle_radius = vertical_spacing
            else:
                self.circle_radius = CIRCLE_RADIUS
            pg.draw.circle(self.bg_image, BLUE,
                           (x_location,
                            y_location),
                           self.circle_radius,
                           CIRCLE_WIDTH)
            # vertical_spacing = (MENU_HEIGHT - HEADER_SPACE) // len(self.game.player.cap_pokemon)
            draw_text(self.bg_image, 'Name: {}'.format(pokemon.name), MENU_FONT_SIZE, MENU_FONT_COLOUR,
                      x_location + STATS_OFFSET,
                      y_location - 40)
            draw_text(self.bg_image, 'Type: {}'.format(pokemon.type), MENU_FONT_SIZE, MENU_FONT_COLOUR,
                      x_location + STATS_OFFSET,
                      y_location - 20)
            draw_text(self.bg_image, 'Health: {}'.format(pokemon.health), MENU_FONT_SIZE, MENU_FONT_COLOUR,
                      x_location + STATS_OFFSET,
                      y_location + 0)
            draw_text(self.bg_image, 'Kills: {}'.format(pokemon.kills), MENU_FONT_SIZE, MENU_FONT_COLOUR,
                      x_location + STATS_OFFSET,
                      y_location + 20)
