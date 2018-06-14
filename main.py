# main.py
# Jacob Laframboise
# June 14th, 2018
# This file is the main file for the PokeGame game.
# it holds classes for the game, the battles, and the intro screen, and the draw_health function
# It also holds the main loop


from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform, randrange
import sys
from os import path
import pygame as pg
from math import sin, cos, pi
from menu import *
from fonts import *

# comment out the outro import if running outro by itself
from outro import *

vec = pg.math.Vector2


def draw_health_bar(surf, x, y, pct):
    '''A function to draw a health bar on a sprite which is damaged. Will display green yellow or red based on damage taken.'''
    if pct < 0:
        pct = 0
    outline_rect = pg.Rect(x, y, HEALTH_LENGTH, HEALTH_HEIGHT)  # make the outline and fill
    fill_rect = pg.Rect(x, y, HEALTH_LENGTH * pct, HEALTH_HEIGHT)
    # change colours based on health
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    # draw them
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    '''A class to hold the methods and attributes which will be used and run to form the foundation of the game. Contains the game loop.'''

    def __init__(self):
        '''Initializing the game object with no variables, as this starts fresh. '''
        pg.init()
        self.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.battle_on = False
        self.need_to_delete_battle = False
        self.total_kills = 0
        self.pokeballs_used = 0
        self.attacks_used = 0
        self.load_data()

    def load_data(self):
        '''A method to load data and graphics from files and organize the folders using os.path.join. This function also calls the map rendering functions from tilemap.py'''
        # set up directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        # load in images and maps
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.map1 = TiledMap(path.join(map_folder, 'map1.tmx'))
        self.map1_img = self.map1.make_map()
        self.map_rect = self.map1_img.get_rect()
        self.turtle_img = pg.image.load(path.join(img_folder, TURTLE_IMG)).convert_alpha()
        self.fire_penguin_img = pg.image.load(path.join(img_folder, FIRE_PENGUIN_IMG)).convert_alpha()
        self.leafcoon_img = pg.image.load(path.join(img_folder, LEAFCOON_IMG)).convert_alpha()
        self.woterpitter_img = pg.image.load(path.join(img_folder, WOTERPITTER_IMG)).convert_alpha()
        self.floataphant_img = pg.image.load(path.join(img_folder, FLOATAPHANT_IMG)).convert_alpha()
        self.beary_img = pg.image.load(path.join(img_folder, BEARY_IMG)).convert_alpha()
        self.rocky_img = pg.image.load(path.join(img_folder, ROCKY_IMG)).convert_alpha()
        self.flamingo_img = pg.image.load(path.join(img_folder, FLAMINGO_IMG)).convert_alpha()
        self.pokeball_img = pg.image.load(path.join(img_folder, POKEBALL_IMG)).convert_alpha()
        self.fire_attack_img = pg.image.load(path.join(img_folder, FIRE_ATTACK_IMG)).convert_alpha()
        self.water_attack_img = pg.image.load(path.join(img_folder, WATER_ATTACK_IMG)).convert_alpha()
        self.grass_attack_img = pg.image.load(path.join(img_folder, GRASS_ATTACK_IMG)).convert_alpha()

        self.pokemon_images = [self.turtle_img, self.fire_penguin_img, self.leafcoon_img,
                               self.woterpitter_img, self.floataphant_img, self.beary_img,
                               self.rocky_img, self.flamingo_img]

    def new(self):
        '''A function that will be run everytime a new game is created, and it initializes the sprites, groups, and camera. '''
        # initialize groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pokemon = pg.sprite.Group()

        self.camera = Camera(self.map1.width, self.map1.height)

        # load in sprites and walls on the map from the tmx file
        for obj in self.map1.tmxdata.objects:
            obj_center = vec(obj.x + obj.width / 2, obj.y + obj.height / 2)
            if obj.name == 'wall':
                Wall(self, obj.x, obj.y, obj.width, obj.height)
            if obj.type == 'pokemon':
                if obj.name[-4:] == 'sure':
                    obj.name = obj.name[:-5]
                else:
                    obj.name = choice(POKEMON_LIST)
                if obj.name == 'Leafcoon':
                    Leafcoon(self, obj_center.x, obj_center.y)
                elif obj.name == 'FlamingPingu':
                    FirePenguin(self, obj_center.x, obj_center.y)
                elif obj.name == 'Woterpitter':
                    Woterpitter(self, obj_center.x, obj_center.y)
                elif obj.name == 'Turtle':
                    Pokemon(self, obj_center.x, obj_center.y)
                elif obj.name == 'Beary':
                    Beary(self, obj_center.x, obj_center.y)
                elif obj.name == 'Rocky':
                    Rocky(self, obj_center.x, obj_center.y)
                elif obj.name == 'Flamingo':
                    Flamingo(self, obj_center.x, obj_center.y)
                elif obj.name == 'Floataphant':
                    Floataphant(self, obj_center.x, obj_center.y)
            if obj.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
        self.debug_mode = False

        self.menu = Menu(self)
        # uncomment the following line if a pokemon is to be added by default
        # self.player.cap_pokemon.add(FirePenguin(self, 400, 400))

    def run(self):
        '''The method that contains and runs the game loop, calling the events, update, draw and fps regulating functions'''
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        '''A function to quit the game.'''
        pg.quit()
        sys.exit()

    def update(self):
        '''A function to update the game each frame, checking collisions between pokemon and player, and updating all sprites. '''
        pg.display.set_caption(str(self.clock.get_fps()))
        self.all_sprites.update()
        self.camera.update(self.player)
        # check for collisions between player and pokemon
        hits = pg.sprite.spritecollide(self.player, self.pokemon, True, collide_hit_rect)
        if hits:
            self.on_contact_pokemon(hits[0])
        self.menu.update()

        # temporary end game condition
        # if len(self.player.cap_pokemon)>0:
        # self.playing = False

    def trigger_ending(self):
        '''A method to run the ending scene with the three stats below. '''
        e = Ending(self.pokeballs_used, self.attacks_used, self.total_kills)
        e.run()

    def on_contact_pokemon(self, pokemon):
        '''A function that will be run when a pokemon touches a player. Launches the battle. '''
        self.player.before_battle_pos = vec(self.player.pos)
        self.battle = Battle(self, pokemon)

    def draw(self):
        '''A function to draw all the gam elements to the screen. '''
        self.screen.fill(BLACK)
        self.screen.blit(self.map1_img, self.camera.apply_rect(self.map_rect))

        # draw all the sprites and the cyan outline on hit_rects if debug mode is on
        for sprite in self.all_sprites:
            # placing the blit function in the if statement stops game from drawing sprites that are offscreen, efficiency
            if abs(sprite.rect.x - self.player.rect.x) < WIDTH / 2 + 360 and abs(
                    sprite.rect.y - self.player.rect.y) < HEIGHT / 2 + 360:
                self.screen.blit(sprite.image, self.camera.apply_rect(sprite.rect))
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        for wall in self.walls:
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply(wall), 1)
        self.screen.blit(self.menu.bg_image, self.menu.bg_rect)
        pg.display.flip()

    def events(self):
        '''A function to handle all the events that occur, namely triggering methods based on keyboard input. '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
                # get keyboard input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.debug_mode = not self.debug_mode
                if event.key == pg.K_f and self.debug_mode:
                    self.player.freeze = not self.player.freeze


class Battle:
    '''A class to run the battle sequence, and holds the functions and attributes to run the battle. '''

    def __init__(self, game, pokemon):
        '''A method to initialize the battle class with variables and groups'''
        self.game = game
        self.game.battle_on = True
        game.battle = self
        self.wild_pokemon = pokemon
        # init groups
        self.wild_pokemon_in_battle = pg.sprite.Group()
        self.players_pokemon_group = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.wild_projectiles = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        self.wild_pokemon_in_battle.add(self.wild_pokemon)
        self.battle_walls = pg.sprite.Group()
        self.permeable_battle_walls = pg.sprite.Group()
        self.all_battle_walls = pg.sprite.Group()

        self.load_battle_data()

        self.game.player.in_battle = True
        self.wild_pokemon.in_battle = True
        self.game.menu.in_battle = True
        self.run()

    def load_battle_data(self):
        '''A function that loads all the resources for the battle to run and display.'''
        # setup directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        # set up map
        self.b_map = TiledMap(path.join(map_folder, 'b_map.tmx'))
        self.b_map_img = self.b_map.make_map()
        self.b_map_rect = self.b_map_img.get_rect()

        self.game.screen = pg.display.set_mode((BATTLE_SCREEN_WIDTH + MENU_WIDTH, HEIGHT))
        # load in sprites and walls
        for obj in self.b_map.tmxdata.objects:
            obj_center = vec(obj.x + obj.width / 2, obj.y + obj.height / 2)
            if obj.name == 'trained_pokemon':
                self.spawn_pos = vec(obj_center.x, obj_center.y)
            if obj.name == 'wild_pokemon':
                self.wild_pokemon.pos = vec(obj_center.x, obj_center.y)
            if obj.name == 'wall':
                Battle_Wall(self, obj.x, obj.y, obj.width, obj.height)
            if obj.name == 'p_wall':
                Permeable_Battle_Wall(self, obj.x, obj.y, obj.width, obj.height)
            if obj.name == 'standby_spot':
                self.standby_spot = vec(obj_center.x, obj_center.y)
        self.game.player.rot = 90
        self.pokemon_in = False
        # auto deploy pokemon
        if len(self.game.player.cap_pokemon) > 0:
            self.deploy_pokemon(1)
        else:
            self.game.player.pos = self.spawn_pos

    def events(self):
        '''A function which processes events to trigger actions based on keyboard input. '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
                # get keybaord input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.game.debug_mode = not self.game.debug_mode
                if event.key == pg.K_f and self.game.debug_mode:
                    self.game.player.freeze = not self.game.player.freeze
                if event.key == pg.K_q:
                    self.deploy_pokemon(1)
                if event.key == pg.K_c and self.game.debug_mode:
                    self.players_pokemon.is_controlled = not self.players_pokemon.is_controlled
                if event.key == pg.K_g and self.game.debug_mode:
                    self.game.player.stick = not self.game.player.stick
                if event.key == pg.K_0:
                    self.leave_without_capture()

    def capture_pokemon_and_leave(self):
        '''A function which will add the wild pokemon to the players pokemon, and then exit the battle. '''
        if self.pokemon_in:  # return deployed pokemon
            self.game.player.cap_pokemon.add(self.players_pokemon)
        # add the wild pokemon
        self.wild_pokemon.health = TRAINED_POKEMON_HEALTH
        self.wild_pokemon.number = len(self.game.player.cap_pokemon) + 1
        self.game.player.cap_pokemon.add(self.wild_pokemon)
        self.wild_pokemon_in_battle.remove(self.wild_pokemon)
        self.game.pokemon.remove(self.wild_pokemon)
        self.game.all_sprites.remove(self.wild_pokemon)
        self.leave_battle()

    def leave_without_capture(self):
        '''A function which leaves the battle without adding the wild pokemon to the players pokemon. '''
        if self.pokemon_in:
            self.game.player.cap_pokemon.add(self.players_pokemon)
        self.leave_battle()

    def battle_loss_leave(self):
        '''A function to leave the battle when all the player's pokemon die. '''
        self.leave_battle()

    def update(self):
        '''A method to update the battle at every frame, where collisions are checked for betweent he pokeball and pokemon, between the projectiles and wild pokemon, and between the projectiles and the trained pokemon. '''
        self.game.player.get_keys()
        self.game.player.update()
        self.wild_pokemon.update()
        self.projectiles.update()
        self.wild_projectiles.update()
        if self.pokemon_in:
            self.players_pokemon.update()
        # the following if statement allows the trainer to capture a pokemon on contact.
        # if not self.pokemon_in:
        # hits = pg.sprite.spritecollide(self.game.player, self.wild_pokemon_in_battle, True, collide_hit_rect)
        # if hits:
        # self.capture_pokemon_and_leave()
        # the following 2 lines and 2 above enable the wild pokemon to be captured on touch by trained pokemon.
        # if self.pokemon_in:
        # hits = pg.sprite.spritecollide(self.players_pokemon, self.wild_pokemon_in_battle, True, collide_hit_rect)

        # For the attacks and pokeballs from trained pokemon
        hits = pg.sprite.groupcollide(self.wild_pokemon_in_battle, self.projectiles, False, True, collide_hit_rect)
        # print(hits)
        for hit in hits:
            # The sprite
            # print('printing hit: ')
            # print(hit)
            # The projectile
            # print('printing hits[hit]: ')
            # print(hits[hit][0])

            # the following if statement chekcs to see what type of object collided
            if isinstance(hit, Pokemon):
                if isinstance(hits[hit][0], Projectile) and hits[hit][0].type == 'pokeball':
                    if len(self.game.player.cap_pokemon) < MAX_POKEMON_LIMIT - 1:
                        if randrange(0, hit.health) <= 20 or len(self.game.player.cap_pokemon) < 1:
                            self.capture_pokemon_and_leave()
                    else:
                        self.leave_without_capture()

                if isinstance(hits[hit][0], WaterAttack):
                    hit.health -= ATTACK_DAMAGE
                if isinstance(hits[hit][0], FireAttack):
                    hit.health -= ATTACK_DAMAGE
                if isinstance(hits[hit][0], GrassAttack):
                    hit.health -= ATTACK_DAMAGE

        # For the attacks from wild pokemon
        if self.pokemon_in:
            hits = pg.sprite.groupcollide(self.players_pokemon_group, self.wild_projectiles, False, True,
                                          collide_hit_rect)
            for hit in hits:
                # check what type of objects collided
                if isinstance(hit, Pokemon):
                    if isinstance(hits[hit][0], WaterAttack):
                        hit.health -= ATTACK_DAMAGE
                    if isinstance(hits[hit][0], FireAttack):
                        hit.health -= ATTACK_DAMAGE
                    if isinstance(hits[hit][0], GrassAttack):
                        hit.health -= ATTACK_DAMAGE

        # check if wild pokemon is dead:
        if self.wild_pokemon.health < 1:
            self.players_pokemon.kills += 1
            self.game.total_kills += 1
            self.players_pokemon.max_health += 20
            self.players_pokemon.health = self.players_pokemon.max_health
            self.wild_pokemon.kill()
            self.leave_without_capture()

        # check if player's pokemon is dead:
        if self.pokemon_in:
            if self.players_pokemon.health < 1:
                self.players_pokemon.kill()
                self.game.total_kills += 1
                self.game.menu.update()
                if len(self.game.player.cap_pokemon) < 1:
                    self.battle_loss_leave()
                else:
                    self.deploy_pokemon(1)

        self.game.menu.update()

        # if statements to fix any glitch where the player ends up outside the map
        if self.game.player.rect.centerx - self.game.player.rect.width / 2 < 0 or self.game.player.rect.centerx + self.game.player.rect.width / 2 > BATTLE_SCREEN_WIDTH:
            self.game.player.pos = vec(BATTLE_SCREEN_WIDTH / 2, HEIGHT * 0.75)
        if self.game.player.rect.centery - self.game.player.rect.height / 2 < 0 or self.game.player.rect.centery + self.game.player.rect.height / 2 > HEIGHT:
            self.game.player.pos = vec(BATTLE_SCREEN_WIDTH / 2, HEIGHT * 0.75)

    def deploy_pokemon(self, pokemon_index):
        '''A method to deploy a trained pokemon into battle and lock the player's position to inside a tree box. '''
        if self.pokemon_in:
            # return currently deployed pokemon
            if self.players_pokemon.health > 1:
                self.game.player.cap_pokemon.add(self.players_pokemon)
                self.game.menu.update()
            else:
                self.players_pokemon.kill()
        self.pokemon_in = True

        # restore health of players pokemon
        for pokemon in self.game.player.cap_pokemon:
            pokemon.health = pokemon.max_health
            if pokemon.number == pokemon_index:
                self.players_pokemon = pokemon

        # update flags and groups
        self.players_pokemon.pos = vec(self.spawn_pos)
        self.players_pokemon.is_controlled = True
        self.game.player.cap_pokemon.remove(self.players_pokemon)
        self.players_pokemon_group.add(self.players_pokemon)
        self.game.player.pos = vec(self.standby_spot)
        self.game.player.stick = True

    def leave_battle(self):
        '''The method to leave the battle and cleanup, will be called by one of the leave type methods above. '''
        self.game.battle_on = False
        self.fighting = False
        self.game.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        self.game.player.freeze = False
        self.game.player.stick = False
        self.game.player.in_battle = False
        self.game.menu.in_battle = False
        self.game.player.pos = self.game.player.before_battle_pos
        self.pokemon_in = False
        self.game.need_to_delete_battle = True

        # check if all pokemon types are captured
        self.game.captured_names_list = [pokemon.name for pokemon in self.game.player.cap_pokemon]
        if sorted(self.game.captured_names_list) == sorted(POKEMON_LIST):
            print('wowza, you got em all!')
            self.game.playing = False

    def draw(self):
        '''A method to draw all the battle elements to the screen each frame. '''
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.b_map_img, self.b_map_rect)
        # update wild pokemon
        for sprite in self.wild_pokemon_in_battle:
            self.game.screen.blit(sprite.image, sprite.rect)
        self.game.screen.blit(self.game.player.image, self.game.player.rect)
        # blit the cyan hit_rects if debugging
        if self.game.debug_mode:
            for wall in self.battle_walls:
                pg.draw.rect(self.game.screen, CYAN, wall.rect, 1)
            pg.draw.rect(self.game.screen, CYAN, self.game.player.hit_rect, 1)
            for pokemon in self.wild_pokemon_in_battle:
                pg.draw.rect(self.game.screen, CYAN, pokemon.hit_rect, 1)
        self.game.screen.blit(self.game.menu.bg_image, self.game.menu.bg_rect)
        # blit the player and his pokemon
        if self.pokemon_in:
            self.game.screen.blit(self.game.player.image, self.game.player.rect)
            self.game.screen.blit(self.players_pokemon.image, self.players_pokemon.rect)
        # blit all projectiles
        for sprite in self.projectiles:
            self.game.screen.blit(sprite.image, sprite.rect)
        for sprite in self.wild_projectiles:
            self.game.screen.blit(sprite.image, sprite.rect)
        # draw the wild pokemon sprite and health bar
        for sprite in self.wild_pokemon_in_battle:
            if sprite.health < sprite.max_health:
                draw_health_bar(self.game.screen, sprite.pos.x + HEALTH_BAR_OFFSET.x,
                                sprite.pos.y + HEALTH_BAR_OFFSET.y, sprite.health / sprite.max_health)
        # draw the players pokemons sprite and health bar
        if self.pokemon_in and self.players_pokemon.health < self.players_pokemon.max_health:
            draw_health_bar(self.game.screen, self.players_pokemon.pos.x + HEALTH_BAR_OFFSET.x,
                            self.players_pokemon.pos.y + HEALTH_BAR_OFFSET.y,
                            self.players_pokemon.health / self.players_pokemon.max_health)

        pg.display.flip()

    def run(self):
        '''The function to run the battle loop and hold execution from returning to the main game loop. '''
        self.fighting = True
        while self.fighting:
            # keep track of time
            self.dt = self.game.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()


class IntroScreen:
    '''A class to hold the attributes and methods to create an intro screen and an instructions screen.'''

    def __init__(self):
        '''A method to initialize the intro screen with variables and loading data from game '''
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Welcome')
        self.clock = pg.time.Clock()
        self.showing = True
        # need to load all the images used in the game, to make a nice intro
        Game.load_data(self)
        self.show_inst = False
        self.player_x = 0
        self.run()

    def update(self):
        '''A method to update the intro screens. '''
        pg.display.set_caption(str(self.clock.get_fps()))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.showing = False
            # let user change between intructions and intro, and launch game
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.showing = False
                if event.key == pg.K_r:
                    self.show_inst = not self.show_inst

        # draw the respective page
        if self.show_inst:
            self.draw_inst_page()
        else:
            # move the player
            self.player_x = (self.player_x + INTRO_PLAYER_SPEED) % (WIDTH + 60)
            self.draw_main_page()

    def draw_main_page(self):
        '''The fuction to draw the main intro page'''
        self.screen.fill(INTRO_BG_COLOUR)

        # draw the title text
        draw_text2(self.screen, intro_title_font_surface, WIDTH / 2, HEIGHT * 0.28)
        draw_text2(self.screen, intro_name_font_surface, WIDTH / 2, HEIGHT * 0.4)
        draw_text2(self.screen, intro_title_subfont_surface, WIDTH / 2, HEIGHT / 100 * 50)
        draw_text2(self.screen, intro_title_subfont_surface2, WIDTH / 2, HEIGHT / 100 * 55)
        draw_text2(self.screen, intro_title_subfont_surface3, WIDTH / 2, HEIGHT / 100 * 60)

        pg.draw.rect(self.screen, INTRO_DIV_COLOUR,
                     pg.Rect(INTRO_DIV_TOP_X - INTRO_DIV_TOP_WIDTH / 2, INTRO_DIV_TOP_Y, INTRO_DIV_TOP_WIDTH,
                             INTRO_DIV_TOP_THICK))

        self.number_of_images = len(self.pokemon_images)

        # draw all the pokemon images in a circle, each pokemon moving periodically in and out of cirlce
        for num, image in enumerate(self.pokemon_images):
            individual_phase_shift = 2 * pi / self.number_of_images * num
            # radius change will be added to position vecotr length, will vary with time.
            self.radius_change = sin(
                pg.time.get_ticks() / 10000 / pi * 180 + individual_phase_shift) * INTRO_RADIUS_MAX_VAR

            # add vectors and rotate
            image_pos = INTRO_CIRCLE_CENTER + vec(INTRO_CIRCLE_RADIUS + self.radius_change, 0).rotate(
                360 / self.number_of_images * num)

            self.screen.blit(image, pg.Rect(image_pos, (1, 1)))

        self.screen.blit(self.player_img, pg.Rect(self.player_x - 60, INTRO_PLAYER_RUN_HEIGHT, 1, 1))
        pg.display.flip()

    def draw_inst_page(self):
        '''The function to alternately draw the instructions page. '''
        self.screen.fill(INTRO_INST_BG_COLOUR)

        # draw each instrutions line
        for num, line in enumerate(instruction_lines_surfaces):
            draw_text2(self.screen, line, WIDTH / 2, INTRO_INST_TOP_BUFFER - 4 + HEIGHT / 100 * 4.6 * num)

        # draw all the pokemon in two lines, above and below the text.
        for num, image in enumerate(self.pokemon_images):
            self.screen.blit(image, pg.Rect(30 + WIDTH / self.number_of_images * num, INTRO_INST_POKEMON_TOPLINE, 1, 1))
            self.screen.blit(image,
                             pg.Rect(30 + WIDTH / self.number_of_images * num, HEIGHT - INTRO_INST_POKEMON_BOTTOMLINE,
                                     1,
                                     1))

        pg.display.flip()

    def run(self):
        '''The function to run the intro screens, until the user hits space. '''
        self.dt = self.clock.tick(FPS) / 1000
        while self.showing:
            self.update()


# launch the game
if __name__ == '__main__':
    i = IntroScreen()
    g = Game()
    g.new()
    g.run()
    g.trigger_ending()
