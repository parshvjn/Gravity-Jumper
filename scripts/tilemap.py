import pygame
from consts import *

PHYSICS_TILES = {'grass', 'stone'}
NEIGHBOR_OFFSETS = [(-1,0), (-1,-1), (0, -1), (1,-1), (1,0), (0,0), (-1, 1), (0,1), (1,1)]
class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.tile_size = tile_size
        self.game = game
        self.tilemap = {"9;7": {"type": "stone", "variant": 1, "pos": [9, 7]}, "6;7": {"type": "stone", "variant": 0, "pos": [6, 7]}, "7;7": {"type": "stone", "variant": 1, "pos": [7, 7]}, "8;7": {"type": "stone", "variant": 1, "pos": [8, 7]}, "10;7": {"type": "stone", "variant": 1, "pos": [10, 7]}, "11;7": {"type": "stone", "variant": 1, "pos": [11, 7]}, "12;7": {"type": "stone", "variant": 1, "pos": [12, 7]}, "13;7": {"type": "stone", "variant": 1, "pos": [13, 7]}, "14;7": {"type": "stone", "variant": 2, "pos": [14, 7]}, "14;8": {"type": "stone", "variant": 4, "pos": [14, 8]}, "13;8": {"type": "stone", "variant": 5, "pos": [13, 8]}, "12;8": {"type": "stone", "variant": 5, "pos": [12, 8]}, "11;8": {"type": "stone", "variant": 5, "pos": [11, 8]}, "10;8": {"type": "stone", "variant": 5, "pos": [10, 8]}, "9;8": {"type": "stone", "variant": 5, "pos": [9, 8]}, "8;8": {"type": "stone", "variant": 5, "pos": [8, 8]}, "7;8": {"type": "stone", "variant": 5, "pos": [7, 8]}, "6;8": {"type": "stone", "variant": 6, "pos": [6, 8]}}
        self.offGridtiles = []
    
    def render(self, surf, offset = (0,0)):
        for x in range(offset[0] // self.tile_size, (offset[0]+ surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1]+ surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size - offset[0], tile['pos'][1]*self.tile_size - offset[1]))
                    # pygame.draw.rect(surf, (255,255,255), pygame.Rect(tile['pos'][0]*self.tile_size - offset[0], tile['pos'][1]*self.tile_size - offset[1], self.tile_size, self.tile_size))
        # self.drawGrid()
    
    def tiles_around(self, pos): #just checking neighboring tiles for collisions with player because why would we need to check every tile
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # convert pixel position to grid position
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap: # checking if there is a surface collision and not just air around player
                tiles.append(self.tilemap[check_loc])
        return tiles #return all tiles around player (not air)

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES: #check if the tiles around it are the part of the ones we want collisions with
                rects.append(pygame.Rect(tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def drawGrid(self):
        for x in range(0, WINDOW_WIDTH, self.tile_size):
            pygame.draw.line(self.game.display, (255,255,255), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, self.tile_size):
            pygame.draw.line(self.game.display, (255,255,255), (0, y), (WINDOW_WIDTH, y))
