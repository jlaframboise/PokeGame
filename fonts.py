import pygame as pg
from settings import *

pg.init()

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, col, x, y):
    '''A function to render and display text'''
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_text2(surf, text_surface, x, y):
    '''A function to display a pre-rendered surface with text'''
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


intro_title_font = pg.font.Font(font_name, INTRO_TEXT_SIZE)
intro_title_font_surface = intro_title_font.render(TITLE, True, INTRO_TEXT_COLOUR)

intro_title_subfont = pg.font.Font(font_name, INTRO_SUBTEXT_SIZE)

intro_title_subfont_surface = intro_title_subfont.render('Press R for Instructions.', True, INTRO_TEXT_COLOUR)
intro_title_subfont_surface2 = intro_title_subfont.render('OR', True, INTRO_TEXT_COLOUR)
intro_title_subfont_surface3 = intro_title_subfont.render('Press Space to Play!', True, INTRO_TEXT_COLOUR)

lines = ['Welcome to {}.'.format(TITLE), 'The objective of the game is to capture Pokemon.',
         'You move your player forward with W, and backwards with D.',
         'You may turn left and right with A and D.',
         'If your trainer encounters a Pokemon, a battle will begin.',
         'Your first encounter, decides your starter pokemon,',
         'and in your next battles, things get a little harder.',
         'You can control your pokemon with the IJKL keys as arrows,',
         'and you can press M for your pokemon to attack.',
         'To capture the pokemon, rotate your trainer with A and D,',
         'and hit SPACE to shoot a Pokeball at the enemy pokemon!',
         'Be careful, your pokemon can die if you let them take too many attacks,',
         "and you can't catch a wild pokemon if you kill it.",
         "Now go out there and catch 'em all!"]

intro_inst_font = pg.font.Font(font_name, INTRO_INST_TEXT_SIZE)
instruction_lines_surfaces = [intro_inst_font.render(x, True, INTRO_INST_TEXT_COLOUR) for x in lines]

stats_font = pg.font.Font(font_name, MENU_FONT_SIZE)
name_lines_surfaces = [stats_font.render('Name: ' + x, True, MENU_FONT_COLOUR) for x in POKEMON_LIST]
type_lines_surfaces = [stats_font.render('Type: ' + x, True, MENU_FONT_COLOUR) for x in TYPE_LIST]
health_line = stats_font.render('Health: 100', True, MENU_FONT_COLOUR)
kills_line = stats_font.render('Kills: 0', True, MENU_FONT_COLOUR)
kills_lines = [stats_font.render('Kills: {}'.format(str(x)), True, MENU_FONT_COLOUR) for x in range(41)]
