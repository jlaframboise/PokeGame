# outro.py
# Jacob Laframboise
# June 14th, 2018
# This file holds the class for the outro

from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
from fonts import *
import pygame as pg
from main import *

vec = pg.math.Vector2


class Ending:
    '''A class to run the ending scene for the game, will be a screen with scrolling text and pokemon.'''

    def __init__(self, pokeballs_used=3, attacks_used=4, total_kills=5):
        '''A method to initialize the ending scene with the attributes it needs. Uses Game.load_data for the images.'''
        pg.init()
        self.screen = pg.display.set_mode((OUTRO_WIDTH, OUTRO_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        Game.load_data(self)
        self.player_img = pg.transform.rotate(self.player_img, 90)
        self.sprite_vertical_shift = 0
        self.sprite_scroll_rate = 2
        self.text_vertical_shift = 0
        self.text_scroll_rate = 0.5
        self.player_vertical_pos = OUTRO_HEIGHT
        self.pokeballs_used = pokeballs_used
        self.attacks_used = attacks_used
        self.total_kills = total_kills
        self.load_text()
        self.run_end = True

    def load_text(self):
        '''A method to generate the text surfaces to blit to the screen. '''
        self.outro_lines = ['Congratulations,',
                            'You have trained hard alongside your pokemon,',
                            'You have explored the unexplored,',
                            'You have been challenged, and prevailed,',
                            'and in your journey,',
                            'you learned a great deal about Pokemon.',
                            'From your very first pokemon, to your latest addition, ',
                            'you have proven yourself to be great,',
                            'and your pokemon greater.',
                            "Congratulations, you are the first to catch 'em all!",
                            ' ',
                            ' ',
                            'Okay now enough of the fluffy good job stuff.',
                            'We need to talk.',
                            "On your journey you had to use {} Pokeballs,".format(self.pokeballs_used),
                            "where on earth will I find {} more Pokeballs??".format(self.pokeballs_used),
                            'Oh, and how many attacks does it take to capture eight pokemon??',
                            'I see you had to use {} attacks to get here,'.format(self.attacks_used),
                            'a little OVERKILL one might think?',
                            'Not to mention you killed HOW MANY POKEMON??',
                            '{}??'.format(self.total_kills),
                            "Pokemon don't grow on trees...",
                            ' ',
                            "Anyways, it's about time you get going,",
                            "There are more pokemon out there."]

        # make font object for outro comments
        self.outro_font = pg.font.Font(font_name, OUTRO_FONT_SIZE)
        # make list of rendered outro comment surfaces, one line per surface
        self.outro_lines_surfaces = [self.outro_font.render(x, True, OUTRO_FONT_COLOUR) for x in self.outro_lines[::-1]]

    def update(self):
        '''A method to move sprites and text down the screen and end the instance when done.'''
        self.sprite_vertical_shift += self.sprite_scroll_rate
        self.text_vertical_shift += self.text_scroll_rate

        self.player_vertical_pos = OUTRO_HEIGHT - OUTRO_HEIGHT * (
                self.text_vertical_shift / (OUTRO_TEXT_LENGTH + OUTRO_HEIGHT))

        # end the scene
        if self.text_vertical_shift > OUTRO_TEXT_LENGTH + OUTRO_HEIGHT:
            self.run_end = False

            draw_text2(self.screen, intro_title_font_surface, OUTRO_WIDTH / 2, OUTRO_HEIGHT * 0.4)
            draw_text2(self.screen, intro_name_font_surface, OUTRO_WIDTH / 2, OUTRO_HEIGHT * 0.6)
            pg.display.flip()

            pg.time.wait(6000)

    def draw(self):
        '''A method to draw all the sprites and text to the screen. '''
        self.screen.fill(PALE_BLUE)

        # draw the pokemon sprites
        for num, pokemon in enumerate(self.pokemon_images):
            # set each one's vertical position
            vertical_pos = (OUTRO_HEIGHT / (len(self.pokemon_images) - 1) * num + self.sprite_vertical_shift) % (
                    OUTRO_HEIGHT + 60) - 60

            # draw two columns
            self.screen.blit(pokemon, pg.Rect(OUTRO_WIDTH / 8 - 30, vertical_pos, 1, 1))
            self.screen.blit(pokemon, pg.Rect(OUTRO_WIDTH / 8 * 7 - 30, vertical_pos, 1, 1))

        # draw all the text
        for num, line in enumerate(self.outro_lines_surfaces):
            # work out vertical position, starting off screen.
            vertical_pos = (OUTRO_TEXT_LENGTH / len(
                self.outro_lines_surfaces) * num + self.text_vertical_shift) - OUTRO_TEXT_LENGTH

            draw_text2(self.screen, line, OUTRO_WIDTH / 2, vertical_pos)

        self.screen.blit(self.player_img, pg.Rect(OUTRO_WIDTH * 0.3, self.player_vertical_pos, 1, 1))

        pg.display.flip()

    def run(self):
        '''A method to hold a game loop for the ending scene to continually update and draw. '''
        while self.run_end:
            # game loop
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.draw()
            # let the use exit early
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run_end = False

# e = Ending()
# e.run()
