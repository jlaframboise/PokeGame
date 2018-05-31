from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
import pygame as pg

vec = pg.math.Vector2


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
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

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 100, 100)
        self.camera = Camera(self.map1.width, self.map1.height)
        for obj in self.map1.tmxdata.objects:  #TODO make players based on map
            obj_center = vec(obj.x, obj.y)
            if obj.name == 'wall':
                Wall(self, obj.x, obj.y, obj.width, obj.height)
        self.debug_mode = False

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

    def draw_grid(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.map1_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply_rect(sprite.rect))
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1  )
        for wall in self.walls:
            if self.debug_mode:
                pg.draw.rect(self.screen, CYAN, self.camera.apply(wall), 1)

        pg.display.flip()
        #if self.debug_mode:



    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.debug_mode = not self.debug_mode


g = Game()

while True:
    g.new()
    g.run()
