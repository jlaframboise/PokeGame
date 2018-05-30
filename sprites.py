import pygame as pg
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dim):  # TODO finish the collisions
    if dim == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dim == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rot = 0
        self.rot_speed = 0

    def get_keys(self):

        self.vel = vec(0, 0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rot_speed = ROTATION_SPEED
        if keys[pg.K_d]:
            self.rot_speed = -ROTATION_SPEED

        if keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 1.5, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot += (self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


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
