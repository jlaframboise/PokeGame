# tilemap.py
# Jacob Laframboise
# June 14th, 2018
# This file holds the classes for the Map creation, and the camera


import pytmx
from settings import *
import pygame as pg


def collide_hit_rect(one, two):
    '''A function to return more information on the two colliding objects in a collision. '''
    return one.hit_rect.colliderect(two.rect)


class TiledMap:
    '''A class to render the map based on the tiled map file. '''

    def __init__(self, filename):
        '''A method to initialize the class object with important info. '''
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        '''A method to render the map image onto a surface tile by tile. '''
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            # if the object is a layer
            if isinstance(layer, pytmx.TiledTileLayer):
                # blit every tile in the layer
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,
                                     (x * self.tmxdata.tilewidth,
                                      y * self.tmxdata.tileheight))

    def make_map(self):
        ''' A method to call the render method on a surface. '''
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    '''A class to hold the important methods for the camera to display elements with an offset relative to the player, to keep things on screen '''

    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        '''Applies the offset to a sprite'''
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        '''Applies the offset to a rect. '''
        return rect.move(self.camera.topleft)

    def update(self, target):
        '''Updates the offset based on the position of the target. '''
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(x, -(self.width - WIDTH))
        y = max(y, -(self.height - HEIGHT))

        self.camera = pg.Rect(x, y, self.width, self.height)
