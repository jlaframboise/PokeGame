import pygame as pg
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.image = game.player_img
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.rot = 0
        self.rot_speed = 0

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.vel = vec(0,0)
        self.rot_speed = 0
        if keys[pg.K_a]:
            self.rot_speed = ROTATION_SPEED
        if keys[pg.K_d]:
            self.rot_speed = -ROTATION_SPEED
        self.rot+=self.rot_speed * self.game.dt
        if keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)



    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos



