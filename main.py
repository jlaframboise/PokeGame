from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
import pygame as pg
from menu import *

vec = pg.math.Vector2


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.map1 = TiledMap(path.join(map_folder, 'map1.tmx'))
        self.map1_img = self.map1.make_map()
        self.map_rect = self.map1_img.get_rect()
        self.turtle_img = pg.image.load(path.join(img_folder, TURTLE_IMG)).convert_alpha()
        self.fire_penguin_img = pg.image.load(path.join(img_folder, FIRE_PENGUIN_IMG)).convert_alpha()
        self.leafcoon_img = pg.image.load(path.join(img_folder, LEAFCOON_IMG)).convert_alpha()
        self.woterpitter_img = pg.image.load(path.join(img_folder, WOTERPITTER_IMG)).convert_alpha()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pokemon = pg.sprite.Group()

        self.camera = Camera(self.map1.width, self.map1.height)
        for obj in self.map1.tmxdata.objects:  # TODO make players based on map
            obj_center = vec(obj.x, obj.y)
            if obj.name == 'wall':
                Wall(self, obj.x, obj.y, obj.width, obj.height)
            if obj.type == 'pokemon':
                if obj.name == 'leafcoon':
                    Leafcoon(self, obj.x, obj.y)
                elif obj.name == 'firepenguin':
                    FirePenguin(self, obj.x, obj.y)
                elif obj.name == 'woterpitter':
                    Woterpitter(self, obj.x, obj.y)
            if obj.name == 'player':
                self.player = Player(self, obj.x, obj.y)
        self.debug_mode = False

        self.menu = Menu(self)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        pass

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.pokemon, True, collide_hit_rect)
        if hits:
            self.on_contact_pokemon(hits[0])

    def on_contact_pokemon(self, pokemon):
        print('Collided with pokemon!')
        self.player.before_battle_pos = self.player.pos
        battle = Battle(self, pokemon)

    def draw_grid(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.map1_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply_rect(sprite.rect))
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        for wall in self.walls:
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply(wall), 1)
        self.screen.blit(self.menu.bg_image, self.menu.bg_rect)
        pg.display.flip()
        # if self.debug_mode:

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.debug_mode = not self.debug_mode


class Battle:
    def __init__(self, game, pokemon):
        self.game = game
        game.battle = self
        self.wild_pokemon = pokemon
        self.sprites_in_battle = pg.sprite.Group()
        self.sprites_in_battle.add(self.wild_pokemon)
        self.battle_walls = pg.sprite.Group()
        self.load_battle_data()
        self.game.player.pos = self.spawn_pos
        self.game.player.in_battle = True
        self.wild_pokemon.in_battle = True
        self.game.menu.in_battle = True
        self.run()

    def load_battle_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        self.b_map = TiledMap(path.join(map_folder, 'b_map.tmx'))
        self.b_map_img = self.b_map.make_map()
        self.b_map_rect = self.b_map_img.get_rect()

        # BATTLE_SCREEN_WIDTH = self.b_map.tmxdata.tilewidth * self.b_map.tmxdata.width
        self.game.screen = pg.display.set_mode((BATTLE_SCREEN_WIDTH + MENU_WIDTH, HEIGHT))
        for obj in self.b_map.tmxdata.objects:
            if obj.name == 'trained_pokemon':
                self.spawn_pos = vec(obj.x, obj.y)
            if obj.name == 'wild_pokemon':
                self.wild_pokemon.pos = vec(obj.x, obj.y)
            if obj.name == 'wall':
                Battle_Wall(self, obj.x, obj.y, obj.width, obj.height)
        self.game.player.rot = 90

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.game.debug_mode = not self.game.debug_mode

    def update(self):
        self.game.player.get_keys()
        self.game.player.update()
        self.wild_pokemon.update()
        hits = pg.sprite.spritecollide(self.game.player, self.sprites_in_battle, True, collide_hit_rect)
        if hits:
            self.game.player.cap_pokemon.add(self.wild_pokemon)
            self.sprites_in_battle.remove(self.wild_pokemon)
            self.game.pokemon.remove(self.wild_pokemon)
            self.game.all_sprites.remove(self.wild_pokemon)
            self.leave_battle()
            self.game.menu.update()
        self.game.menu.update()

    def leave_battle(self):
        self.fighting = False
        self.game.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        self.game.player.in_battle = False
        self.game.menu.in_battle = False
        self.game.player.pos = self.game.player.before_battle_pos

    def draw(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.b_map_img, self.b_map_rect)
        for sprite in self.sprites_in_battle:
            self.game.screen.blit(sprite.image, sprite.rect)
        self.game.screen.blit(self.game.player.image, self.game.player.rect)
        if self.game.debug_mode:
            for wall in self.battle_walls:
                pg.draw.rect(self.game.screen, CYAN, wall.rect, 1)
            pg.draw.rect(self.game.screen, CYAN, self.game.player.hit_rect, 1)
            for pokemon in self.sprites_in_battle:
                pg.draw.rect(self.game.screen, CYAN, pokemon.hit_rect, 1)
        self.game.screen.blit(self.game.menu.bg_image, self.game.menu.bg_rect)

        pg.display.flip()

    def run(self):
        # game loop
        self.fighting = True
        while self.fighting:
            self.dt = self.game.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()


g = Game()

while True:
    g.new()
    g.run()
