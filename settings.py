import pygame as pg

WIDTH = 1024
HEIGHT = 768
TITLE = 'PokeGame'
FPS = 60
TILE_SIZE = 64

# Menu Settings
MENU_WIDTH = 300
MENU_HEIGHT = HEIGHT
CIRCLE_RADIUS = 80
CIRCLE_WIDTH = 6
NUMBER_OF_CIRCLES = 3
HEADER_SPACE = 80
BATTLE_SCREEN_WIDTH = 10 * 64

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

# player settings:
PLAYER_SPEED = 500
ROTATION_SPEED = 250
PLAYER_IMG = 'trainer.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Pokemon settings
TURTLE_IMG = 'turtle.png'
POKEMON_SPEED = 200
POKEMON_MOVE_DELAY = 500
