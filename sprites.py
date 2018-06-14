# sprites.py
# Jacob Laframboise
# June 14th, 2018
# This file holds the classes for all the sprites, and the collide with walls function

import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import choice

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dim):
    '''A function to reset the x and y coords of a spirte to a valid location when moving paced them inside a wall object. '''
    if dim == 'x':  # if in the x directions
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # move the x position to a valid spot
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # stop sprite in x direction
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dim == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # move the y position to a valid spot
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # stop the sprite in the y direction
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    '''A class to hold the methods and attributes of the player/ trainer. '''

    def __init__(self, game, x, y):
        '''A function to initialize the player object. '''
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
        '''A function to modify motion based on keyboard state. '''
        self.vel = vec(0, 0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        # rotate player with A and D
        if keys[pg.K_a]:
            if self.game.battle_on and self.game.battle.pokemon_in:
                self.rot_speed = ROTATION_SPEED / 2
            else:
                self.rot_speed = ROTATION_SPEED
        if keys[pg.K_d]:
            if self.game.battle_on and self.game.battle.pokemon_in:
                self.rot_speed = -ROTATION_SPEED / 2
            else:
                self.rot_speed = -ROTATION_SPEED

        # move the player forward
        if keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        # move backward
        if keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 1.5, 0).rotate(-self.rot)
        # shoot a pokeball
        if keys[pg.K_SPACE] and self.in_battle:
            now = pg.time.get_ticks()
            if now - self.last_shot > POKEBALL_DELAY:
                self.last_shot = now
                self.game.pokeballs_used += 1
                Projectile(self.game, self.pos, self.rot, self.in_battle)

    def update(self):
        '''A function to update the player if he is not frozen or stuck. '''
        if not self.freeze:
            self.get_keys()
            self.rot += (self.rot_speed * self.game.dt) % 360
            # rotate player img
            self.image = pg.transform.rotate(self.game.player_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            # if stuck, player does all but move
            if not self.stick:
                self.pos += self.vel * self.game.dt

            # move the hit_rect in the x direction, then check for collisions which will adjust its position
            self.hit_rect.centerx = self.pos.x
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'x')
            elif self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'x')

            # move the hit_rect in the y direction, then check for collisions which will adjust its position
            self.hit_rect.centery = self.pos.y
            if not self.in_battle:
                collide_with_walls(self, self.game.walls, 'y')
            elif self.in_battle:
                collide_with_walls(self, self.game.battle.all_battle_walls, 'y')

            # set the player's position to the hit_rect position after modification by collisions
            self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    '''A class to make walls, only holding their rect. '''

    def __init__(self, game, x, y, width, height):
        self.game = game
        self.groups = self.game.walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # create rect
        self.rect = pg.Rect(x, y, width, height)


class Battle_Wall(pg.sprite.Sprite):
    '''A class of walls that is meant to be used in a battle, not in the main game. '''

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
    '''A child class of battle wall that pokeballs can pass though, so the player can shoot out of his box. '''

    def __init__(self, battle, x, y, width, height):
        super().__init__(battle, x, y, width, height)
        self.battle.battle_walls.remove(self)
        self.battle.permeable_battle_walls.add(self)


class Pokemon(pg.sprite.Sprite):
    '''A class to hold the methods and attributes of pokemon objects. '''

    def __init__(self, game, x, y):
        '''A function to setup the initial values for the pokemon object. '''
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
        self.health = WILD_POKEMON_HEALTH
        self.max_health = self.health
        self.last_attacked = pg.time.get_ticks()
        self.name = 'Turtle'
        self.type = 'grass'
        self.kills = 0
        # Uncomment the following line if a pokemon is to be added by default
        # self.number = 1

    def move(self):
        '''A method to enable control of pokemon with the ijkl keys if that pokemon's is_controlled flag is True.'''
        if self.is_controlled:
            self.vel = vec(0, 0)
            keys = pg.key.get_pressed()
            # set velocity based on keyboard state
            if keys[pg.K_i]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-90)
            if keys[pg.K_j]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-180)
            if keys[pg.K_k]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-270)
            if keys[pg.K_l]:
                self.vel = vec(POKEMON_SPEED, 0).rotate(-360)
            # make the pokemon attack
            if keys[pg.K_m] and self.in_battle:
                now = pg.time.get_ticks()
                if now - self.last_attacked > TRAINED_ATTACK_DELAY:
                    self.game.attacks_used += 1
                    # get vecotr from pokemon to wild pokemon
                    attack_vector = self.game.battle.wild_pokemon.pos - self.pos
                    # perform right type attack
                    if self.type == 'water':
                        WaterAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                    if self.type == 'fire':
                        FireAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                    if self.type == 'grass':
                        GrassAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                    self.last_attacked = now
        else:
            # if the pokemon is not controlled, move randomly
            self.rot = choice([0, 90, 180, 270])
            self.vel = vec(POKEMON_SPEED, 0).rotate(self.rot)

    def update(self):
        '''A function to update the pokemon each frame based on if it is in game or battle, wild or trained. '''
        self.freeze = False
        if not self.freeze:

            if self.is_controlled:
                self.move()
            else:
                # after a delay, call move again
                if pg.time.get_ticks() - self.last_moved > POKEMON_MOVE_DELAY:
                    self.move()
                    self.last_moved = pg.time.get_ticks()
                # if there is a players pokemon to attack, attack
                if self.game.battle_on:
                    if self.game.battle.pokemon_in:
                        now = pg.time.get_ticks()
                        if now - self.last_attacked > WILD_ATTACK_DELAY:
                            # get vector to trained pokemon
                            attack_vector = self.game.battle.players_pokemon.pos - self.pos
                            # select correct attack
                            if self.type == 'water':
                                WildWaterAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                            if self.type == 'grass':
                                WildGrassAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                            if self.type == 'fire':
                                WildFireAttack(self.game, self.pos, attack_vector.angle_to(X_AXIS), self.in_battle)
                            self.last_attacked = now

            # add velocity to position
            self.pos += self.vel * self.game.dt

            # do collisions  in battle or in game.
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
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'fire'
        self.image = self.game.fire_penguin_img
        self.name = 'FlamingPingu'


class Leafcoon(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'grass'
        self.image = self.game.leafcoon_img
        self.name = 'Leafcoon'


class Woterpitter(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'water'
        self.image = self.game.woterpitter_img
        self.name = 'Woterpitter'


class Beary(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'grass'
        self.image = self.game.beary_img
        self.name = 'Beary'


class Floataphant(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'water'
        self.image = self.game.floataphant_img
        self.name = 'Floataphant'


class Rocky(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'fire'
        self.image = self.game.rocky_img
        self.name = 'Rocky'


class Flamingo(Pokemon):
    '''A child class of Pokemon with a different type, name, image. '''

    def __init__(self, game, x, y):
        Pokemon.__init__(self, game, x, y)
        self.type = 'water'
        self.image = self.game.flamingo_img
        self.name = 'Flamingo'


class Projectile(pg.sprite.Sprite):
    '''A class of objects to control and implement projectiles. Will hold attributes and methods to support motion and collisions. '''

    def __init__(self, game, pos, dir, in_battle):
        '''A method to initialize the projectiles with initial values. '''
        self.type = 'pokeball'
        self.game = game
        self.pos = vec(pos)
        self.dir = dir
        self.groups = game.all_sprites, game.battle.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.pokeball_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = self.pos
        self.vel = vec(PROJECTILE_SPEED, 0).rotate(-self.dir)
        self.spawn_time = pg.time.get_ticks()
        self.in_battle = in_battle

    def update(self):
        '''The function to update th projectile, by adding velocity ot position, and check collisions with walls or battle walls. '''
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        # check for collisions with walls, kill self if so
        if not self.in_battle:
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.kill()
        else:
            if pg.sprite.spritecollideany(self, self.game.battle.battle_walls):
                self.kill()
        # don't let them travel forever
        if pg.time.get_ticks() - self.spawn_time > POKEBALL_LIFETIME:
            self.kill()


class WaterAttack(Projectile):
    '''A child class of Projectile, with a new image and a type. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.type = 'attack'
        self.image = self.game.water_attack_img


class WildWaterAttack(WaterAttack):
    '''A child class of WaterAttack, with different groups for colliding with the player's pokemon instead of themselves. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.game.battle.projectiles.remove(self)
        self.game.battle.wild_projectiles.add(self)


class FireAttack(Projectile):
    '''A child class of Projectile, with a new image and a type. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.type = 'attack'
        self.image = self.game.fire_attack_img


class WildFireAttack(FireAttack):
    '''A child class of FireAttack, with different groups for colliding with the player's pokemon instead of themselves. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.game.battle.projectiles.remove(self)
        self.game.battle.wild_projectiles.add(self)


class GrassAttack(Projectile):
    '''A child class of Projectile, with a new image and a type. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.type = 'attack'
        self.image = self.game.grass_attack_img


class WildGrassAttack(GrassAttack):
    '''A child class of GrassAttack, with different groups for colliding with the player's pokemon instead of themselves. '''

    def __init__(self, game, pos, dir, in_battle):
        super().__init__(game, pos, dir, in_battle)
        self.game.battle.projectiles.remove(self)
        self.game.battle.wild_projectiles.add(self)
