import pygame as pg

vec = pg.math.Vector2

# basic game settings
WIDTH = 1024
HEIGHT = 768
TITLE = 'PokeGame'
FPS = 60
TILE_SIZE = 64

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
PALE_BLUE = (8, 168, 255)
ORANGE = (255, 82, 48)
STRONG_ORANGE = (255, 106, 0)

# Menu Settings
MENU_WIDTH = 300
MENU_HEIGHT = HEIGHT
MENU_BG_COLOUR = PALE_BLUE
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 6
NUMBER_OF_CIRCLES = 3
HEADER_SPACE = 80
BATTLE_SCREEN_WIDTH = 10 * 64
MENU_FONT_SIZE = 14
MENU_FONT_COLOUR = BLACK
STATS_OFFSET = 120
STATS_SPACING = 10

X_AXIS = vec(1, 0)

# player settings:
PLAYER_SPEED = 500
ROTATION_SPEED = 250
PLAYER_IMG = 'trainer.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Pokemon settings
POKEMON_LIST = ['Turtle', 'FlamingPingu', 'Leafcoon', 'Woterpitter', 'Beary', 'Floataphant', 'Rocky', 'Flamingo']
TYPE_LIST = ['grass', 'fire', 'water']
TURTLE_IMG = 'turtle.png'
FIRE_PENGUIN_IMG = 'flaminghotpingu.png'
LEAFCOON_IMG = 'leafcoon.png'
WOTERPITTER_IMG = 'woterpitter.png'
FLOATAPHANT_IMG = 'floataphant.png'
FLAMINGO_IMG = 'flamingo.png'
BEARY_IMG = 'beary.png'
ROCKY_IMG = 'Rockey2.png'
POKEMON_SPEED = 200
POKEMON_MOVE_DELAY = 500
WILD_POKEMON_HEALTH = 100
TRAINED_POKEMON_HEALTH = 100
MAX_POKEMON_LIMIT = 8
HEALTH_BAR_OFFSET = vec(-52, 28)

# Projectile settings
PROJECTILE_SPEED = 500
POKEBALL_DELAY = 800
POKEBALL_LIFETIME = 1600
POKEBALL_IMG = 'pokeball.png'

GRASS_ATTACK_IMG = 'grass_attack.png'
WATER_ATTACK_IMG = 'water_attack.png'
FIRE_ATTACK_IMG = 'fire_attack.png'

ATTACK_DAMAGE = 20
TRAINED_ATTACK_DELAY = 400
WILD_ATTACK_DELAY = 1500

# health bars
HEALTH_LENGTH = 100
HEALTH_HEIGHT = 20

# intro settings
INTRO_TIME = 3000
INTRO_CIRCLE_RADIUS = 300
INTRO_RADIUS_MAX_VAR = 15
INTRO_CIRCLE_CENTER = vec(WIDTH / 2 - 30, HEIGHT / 100 * 48)
INTRO_BG_COLOUR = PALE_BLUE
INTRO_PLAYER_RUN_HEIGHT = HEIGHT / 100 * 67
INTRO_PLAYER_SPEED = 0.25
INTRO_TEXT_COLOUR = ORANGE
INTRO_TEXT_SIZE = 60
INTRO_SUBTEXT_SIZE = 30
INTRO_INST_BG_COLOUR = WHITE
INTRO_INST_TEXT_COLOUR = BLACK
INTRO_INST_TEXT_SIZE = 24
INTRO_INST_TOP_BUFFER = HEIGHT / 7
INTRO_INST_POKEMON_TOPLINE = INTRO_INST_TOP_BUFFER / 10 * 4
INTRO_INST_POKEMON_BOTTOMLINE = 60 + INTRO_INST_POKEMON_TOPLINE
