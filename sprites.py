import pygame as pg
from settings import *

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dim): #TODO finish the collisions
    hits = pg.sprite.spritecollide(sprite, group, False)
    if dim == 'x':
        for hit in hits:
            if hit[0].centerx> sprite.rect.centerx:
                sprite.rect.x = hit[0].x - hit[0].width
            if hit[0].centerx< sprite.rect.centerx:
                sprite.rect.x = hit[0].x + hit[0].width
    if dim == 'y':
        for hit in hits:
            if hit[0].centery> sprite.rect.centery:
                sprite.rect.y = hit[0].y - hit[0].height
            if hit[0].centery< sprite.rect.centery:
                sprite.rect.y = hit[0].y + hit[0].height


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
        self.rot+=self.rot_speed * self.game.dt %360
        if keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)



    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt

        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.groups = self.game.walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pg.Rect(x, y, width, height)




