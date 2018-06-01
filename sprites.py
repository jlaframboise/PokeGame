import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import choice

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
        self.in_battle = False

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
        if not self.in_battle:
            collide_with_walls(self, self.game.walls, 'x')
        elif self.in_battle:
            collide_with_walls(self, self.game.battle.battle_walls, 'x')
        self.hit_rect.centery = self.pos.y
        if not self.in_battle:
            collide_with_walls(self, self.game.walls, 'y')
        elif self.in_battle:
            collide_with_walls(self, self.game.battle.battle_walls, 'y')
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


class Battle_Wall(pg.sprite.Sprite):
    def __init__(self, battle, x, y, width, height):
        self.battle = battle
        self.groups = self.battle.battle_walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pg.Rect(x, y, width, height)


class Pokemon(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.pokemon
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = vec(x, y)
        self.spawn_pos = self.pos
        self.image = self.game.turtle_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.vel = vec(0, 0)
        self.last_moved = pg.time.get_ticks()
        self.rect.center = self.pos
        self.rot = 0
        self.in_battle = False

    def move(self):
        self.rot = choice([0, 90, 180, 270])
        self.vel = vec(POKEMON_SPEED, 0).rotate(self.rot)

    def update(self):
        if pg.time.get_ticks() - self.last_moved > POKEMON_MOVE_DELAY:
            self.move()
            self.last_moved = pg.time.get_ticks()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        if not self.in_battle:
            collide_with_walls(self, self.game.walls, 'x')
        elif self.in_battle:
            collide_with_walls(self, self.game.battle.battle_walls, 'x')
        self.hit_rect.centery = self.pos.y
        if not self.in_battle:
            collide_with_walls(self, self.game.walls, 'y')
        elif self.in_battle:
            collide_with_walls(self, self.game.battle.battle_walls, 'y')
        self.rect = self.hit_rect
        self.pos = self.rect.center
