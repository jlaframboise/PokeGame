import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import choice

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dim):
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
        self.cap_pokemon = pg.sprite.Group()
        self.freeze = False
        self.last_shot = 0
        self.stick = False

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
        if keys[pg.K_SPACE] and self.in_battle:
            now = pg.time.get_ticks()
            if now - self.last_shot > POKEBALL_DELAY:
                self.last_shot = now
                Projectile(self.game, self.pos, self.rot, self.in_battle)

    def update(self):
        if not self.freeze:
            self.get_keys()
            self.rot += (self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.player_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if not self.stick:
                self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'x')
            elif self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'x')
            self.hit_rect.centery = self.pos.y
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'y')
            elif self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'y')
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
        self.groups = self.battle.battle_walls, self.battle.all_battle_walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pg.Rect(x, y, width, height)

class Permeable_Battle_Wall(Battle_Wall):
    def __init__(self,battle, x, y, width, height):
        super().__init__(battle, x, y, width, height)
        self.battle.battle_walls.remove(self)
        self.battle.permeable_battle_walls.add(self)



class Pokemon(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.pokemon
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.spawn_pos = self.pos
        self.image = self.game.turtle_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.last_moved = pg.time.get_ticks()
        self.rect.center = self.pos
        self.rot = 0
        self.in_battle = False
        self.freeze = False
        self.is_controlled = False
        self.health = 100
        # Uncomment the following line if a pokemon is to be added by default
        # self.number = 1

    def move(self):
        # The following code is enables control of all pokemon with the ijkl keys.
        if self.is_controlled:
            self.vel = vec(0, 0)
            keys = pg.key.get_pressed()
            if keys[pg.K_i]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-90)
            if keys[pg.K_j]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-180)
            if keys[pg.K_k]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-270)
            if keys[pg.K_l]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-360)
        else:

            self.rot = choice([0, 90, 180, 270])
            self.vel = vec(POKEMON_SPEED, 0).rotate(self.rot)

    def update(self):
        self.freeze = False
        if not self.freeze:

            if self.is_controlled:
                self.move()
            else:
                if pg.time.get_ticks() - self.last_moved > POKEMON_MOVE_DELAY:
                    self.move()
                    self.last_moved = pg.time.get_ticks()

            self.pos += self.vel * self.game.dt

            self.hit_rect.centerx = self.pos.x
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'x')
            if self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'x')
            self.hit_rect.centery = self.pos.y
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'y')
            if self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'y')

            self.rect.center = self.hit_rect.center


class FirePenguin(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'fire'
        self.image = self.game.fire_penguin_img


class Leafcoon(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'grass'
        self.image = self.game.leafcoon_img


class Woterpitter(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'water'
        self.image = self.game.woterpitter_img


class Beary(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'fairy'
        self.image = self.game.beary_img


class Floataphant(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'flying'
        self.image = self.game.floataphant_img


class Rocky(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'rock'
        self.image = self.game.rocky_img


class Flamingo(Pokemon):
    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'psychic'
        self.image = self.game.flamingo_img


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, in_battle):
        self.game = game
        self.pos = vec(pos)
        self.dir = dir
        self.groups = game.all_sprites, game.battle.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = self.pos
        self.vel = vec(PROJECTILE_SPEED, 0).rotate(-self.dir)
        self.spawn_time = pg.time.get_ticks()
        self.in_battle = in_battle

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if not self.in_battle:
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.kill()
        else:
            if pg.sprite.spritecollideany(self, self.game.battle.battle_walls):
                self.kill()

        if pg.time.get_ticks() - self.spawn_time > POKEBALL_LIFETIME:
            self.kill()
