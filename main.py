from sprites import *
from settings import *
from tilemap import *
from random import choice, randint, uniform
import sys
from os import path
import pygame as pg
from menu import *

vec = pg.math.Vector2

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, col, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    outline_rect = pg.Rect(x, y, HEALTH_LENGTH, HEALTH_HEIGHT)
    fill_rect = pg.Rect(x, y, HEALTH_LENGTH * pct, HEALTH_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.battle_on = False
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
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pokemon = pg.sprite.Group()

        self.camera = Camera(self.map1.width, self.map1.height)
        for obj in self.map1.tmxdata.objects:
            obj_center = vec(obj.x + obj.width / 2, obj.y + obj.height / 2)
            if obj.name == 'wall':
                Wall(self, obj.x, obj.y, obj.width, obj.height)
            if obj.type == 'pokemon':
                obj.name = choice(POKEMON_LIST)
                if obj.name == 'Leafcoon':
                    Leafcoon(self, obj_center.x, obj_center.y)
                elif obj.name == 'FirePenguin':
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
        pg.display.set_caption(str(self.clock.get_fps()))
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.pokemon, True, collide_hit_rect)
        if hits:
            self.on_contact_pokemon(hits[0])

    def on_contact_pokemon(self, pokemon):
        self.player.before_battle_pos = vec(self.player.pos)
        battle = Battle(self, pokemon)

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

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.debug_mode = not self.debug_mode
                if event.key == pg.K_f:
                    self.player.freeze = not self.player.freeze


class Battle:
    def __init__(self, game, pokemon):
        self.game = game
        self.game.battle_on = True
        game.battle = self
        self.wild_pokemon = pokemon
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
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        self.b_map = TiledMap(path.join(map_folder, 'b_map.tmx'))
        self.b_map_img = self.b_map.make_map()
        self.b_map_rect = self.b_map_img.get_rect()

        # BATTLE_SCREEN_WIDTH = self.b_map.tmxdata.tilewidth * self.b_map.tmxdata.width
        self.game.screen = pg.display.set_mode((BATTLE_SCREEN_WIDTH + MENU_WIDTH, HEIGHT))
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
        if len(self.game.player.cap_pokemon) > 0:
            self.deploy_pokemon(1)
        else:
            self.game.player.pos = self.spawn_pos

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.game.debug_mode = not self.game.debug_mode
                if event.key == pg.K_f:
                    self.game.player.freeze = not self.game.player.freeze
                if event.key == pg.K_1:
                    self.deploy_pokemon(1)
                if event.key == pg.K_c:
                    self.players_pokemon.is_controlled = not self.players_pokemon.is_controlled
                if event.key == pg.K_g:
                    self.game.player.stick = not self.game.player.stick

    def capture_pokemon_and_leave(self):
        if self.pokemon_in:
            self.game.player.cap_pokemon.add(self.players_pokemon)
        self.wild_pokemon.health = TRAINED_POKEMON_HEALTH
        self.wild_pokemon.number = len(self.game.player.cap_pokemon) + 1
        self.game.player.cap_pokemon.add(self.wild_pokemon)
        self.wild_pokemon_in_battle.remove(self.wild_pokemon)
        self.game.pokemon.remove(self.wild_pokemon)
        self.game.all_sprites.remove(self.wild_pokemon)
        self.leave_battle()
        self.game.menu.update()

    def leave_without_capture(self):
        if self.pokemon_in:
            self.game.player.cap_pokemon.add(self.players_pokemon)
        self.leave_battle()
        self.game.menu.update()

    def battle_loss_leave(self):
        self.leave_battle()
        self.game.menu.update()

    def update(self):
        self.game.player.get_keys()
        self.game.player.update()
        self.wild_pokemon.update()
        self.projectiles.update()
        self.wild_projectiles.update()
        if self.pokemon_in:
            self.players_pokemon.update()
        #the following if statement allows the trainer to capture a pokemon on contact.
        #if not self.pokemon_in:
            #hits = pg.sprite.spritecollide(self.game.player, self.wild_pokemon_in_battle, True, collide_hit_rect)
            #if hits:
                #self.capture_pokemon_and_leave()
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

            if isinstance(hit, Pokemon):

                if isinstance(hits[hit][0], Projectile) and hits[hit][0].type == 'pokeball':
                    self.capture_pokemon_and_leave()
                if isinstance(hits[hit][0], WaterAttack):
                    hit.health -= ATTACK_DAMAGE
                if isinstance(hits[hit][0], FireAttack):
                    hit.health -= ATTACK_DAMAGE
                if isinstance(hits[hit][0], GrassAttack):
                    hit.health -= ATTACK_DAMAGE
                    # print('enemy: {}, me: {}'.format(hit.health, self.players_pokemon.health))
        # For the attacks from wild pokemon
        if self.pokemon_in:
            hits = pg.sprite.groupcollide(self.players_pokemon_group, self.wild_projectiles, False, True,
                                          collide_hit_rect)
            for hit in hits:
                if isinstance(hit, Pokemon):
                    if isinstance(hits[hit][0], WaterAttack):
                        hit.health -= ATTACK_DAMAGE
                    if isinstance(hits[hit][0], FireAttack):
                        hit.health -= ATTACK_DAMAGE
                    if isinstance(hits[hit][0], GrassAttack):
                        hit.health -= ATTACK_DAMAGE

        # check if wild pokemon is dead:
        if self.wild_pokemon.health < 1:
            self.wild_pokemon.kill()
            self.leave_without_capture()

        # check if player's pokemon is dead:
        if self.pokemon_in:
            if self.players_pokemon.health < 1:
                self.players_pokemon.kill()
                self.game.menu.update()
                if len(self.game.player.cap_pokemon) < 1:
                    self.battle_loss_leave()
                else:
                    self.deploy_pokemon(1)

        self.game.menu.update()

    def deploy_pokemon(self, pokemon_index):

        if self.pokemon_in:
            if self.players_pokemon.health > 1:
                self.game.player.cap_pokemon.add(self.players_pokemon)
                self.game.menu.update()
            else:
                self.players_pokemon.kill()
        self.pokemon_in = True

        for pokemon in self.game.player.cap_pokemon:
            pokemon.health = TRAINED_POKEMON_HEALTH
            if pokemon.number == pokemon_index:
                self.players_pokemon = pokemon

        self.players_pokemon.pos = vec(self.spawn_pos)
        self.players_pokemon.is_controlled = True
        self.game.player.cap_pokemon.remove(self.players_pokemon)
        self.players_pokemon_group.add(self.players_pokemon)
        self.game.player.pos = vec(self.standby_spot)
        self.game.player.stick = True

    def leave_battle(self):
        self.game.battle_on = False
        self.fighting = False
        self.game.screen = pg.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
        self.game.player.freeze = False
        self.game.player.stick = False
        self.game.player.in_battle = False
        self.game.menu.in_battle = False
        self.game.player.pos = self.game.player.before_battle_pos
        self.pokemon_in = False

    def draw(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.b_map_img, self.b_map_rect)
        for sprite in self.wild_pokemon_in_battle:
            self.game.screen.blit(sprite.image, sprite.rect)
        self.game.screen.blit(self.game.player.image, self.game.player.rect)
        if self.game.debug_mode:
            for wall in self.battle_walls:
                pg.draw.rect(self.game.screen, CYAN, wall.rect, 1)
            pg.draw.rect(self.game.screen, CYAN, self.game.player.hit_rect, 1)
            for pokemon in self.wild_pokemon_in_battle:
                pg.draw.rect(self.game.screen, CYAN, pokemon.hit_rect, 1)
        self.game.screen.blit(self.game.menu.bg_image, self.game.menu.bg_rect)
        if self.pokemon_in:
            self.game.screen.blit(self.game.player.image, self.game.player.rect)
            self.game.screen.blit(self.players_pokemon.image, self.players_pokemon.rect)
        for sprite in self.projectiles:
            self.game.screen.blit(sprite.image, sprite.rect)
        for sprite in self.wild_projectiles:
            self.game.screen.blit(sprite.image, sprite.rect)
        for sprite in self.wild_pokemon_in_battle:
            if sprite.health < WILD_POKEMON_HEALTH:
                draw_health_bar(self.game.screen, sprite.pos.x, sprite.pos.y, sprite.health / WILD_POKEMON_HEALTH)
        if self.pokemon_in and self.players_pokemon.health < TRAINED_POKEMON_HEALTH:
            draw_health_bar(self.game.screen, self.players_pokemon.pos.x, self.players_pokemon.pos.y,
                            self.players_pokemon.health / TRAINED_POKEMON_HEALTH)

        pg.display.flip()

    def run(self):
        # game loop
        self.fighting = True
        while self.fighting:
            self.dt = self.game.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()



class IntroScreen:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Welcome')
        self.clock = pg.time.Clock()
        self.showing = True
        Game.load_data(self)
        self.run()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.showing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.showing = False

        self.draw()


    def draw(self):
        self.screen.fill(BLUE)
        draw_text(self.screen, TITLE, 60, RED, WIDTH/2, HEIGHT/3)
        self.number_of_images = len(self.pokemon_images)
        for num, image in enumerate(self.pokemon_images):
            image_pos = INTRO_CIRCLE_CENTER + vec(INTRO_RADIUS, 0).rotate(360 / self.number_of_images * num)
            self.screen.blit(image, pg.Rect((image_pos), (1,1)))


        pg.display.flip()

    def run(self):
        self.clock.tick(FPS)
        while self.showing:
            self.update()


i = IntroScreen()

g = Game()

while True:
    g.new()
    g.run()
