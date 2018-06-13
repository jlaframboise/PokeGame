from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
from fonts import *
from main import *
import pygame as pg

vec = pg.math.Vector2


class Ending:
    def __init__(self, pokeballs_used, attacks_used, total_kills):
        pg.init()
        self.screen = pg.display.set_mode((OUTRO_WIDTH, OUTRO_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        Game.load_data(self)
        self.sprite_vertical_shift = 0
        self.sprite_scroll_rate = 2
        self.text_vertical_shift = 0
        self.text_scroll_rate = 0.5
        self.pokeballs_used = pokeballs_used
        self.attacks_used = attacks_used
        self.total_kills = total_kills
        self.load_text()
        self.run_end = True

    def load_text(self):
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
                            '',
                            "Anyways, it's about time you get going,",
                            "There are more pokemon out there."]

        # make font object for instructions
        self.outro_font = pg.font.Font(font_name, OUTRO_FONT_SIZE)
        # make list of rendered instructions surfaces, one line per surface
        self.outro_lines_surfaces = [self.outro_font.render(x, True, OUTRO_FONT_COLOUR) for x in self.outro_lines[::-1]]

    def update(self):
        self.sprite_vertical_shift += self.sprite_scroll_rate
        self.text_vertical_shift += self.text_scroll_rate
        if self.text_vertical_shift > OUTRO_TEXT_LENGTH+OUTRO_HEIGHT:
            self.run_end = False

    def draw(self):
        self.screen.fill(PALE_BLUE)
        for num, pokemon in enumerate(self.pokemon_images):
            vertical_pos = (OUTRO_HEIGHT / (len(self.pokemon_images) - 1) * num + self.sprite_vertical_shift) % (
                        OUTRO_HEIGHT + 60) - 60

            self.screen.blit(pokemon, pg.Rect(OUTRO_WIDTH / 8 - 30, vertical_pos, 1, 1))
            self.screen.blit(pokemon, pg.Rect(OUTRO_WIDTH / 8 * 7 - 30, vertical_pos, 1, 1))

        for num, line in enumerate(self.outro_lines_surfaces):
            vertical_pos = (OUTRO_TEXT_LENGTH / len(
                self.outro_lines_surfaces) * num + self.text_vertical_shift) - OUTRO_TEXT_LENGTH

            draw_text2(self.screen, line, OUTRO_WIDTH / 2, vertical_pos)

        pg.display.flip()

    def run(self):

        while self.run_end:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run_end = False


e = Ending(4, 5, 6)
e.run()
