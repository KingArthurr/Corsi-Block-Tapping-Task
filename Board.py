import random
import pygame

''' Class used for controlling the board.
    Takes care of creating and plotting tiles etc.
    Used as Model   '''


class Board:
    ''' coordiantes 1000x700
        Tile size 99x99
        Tile coordinate is middle of tile
        Export initial sequence plot Hashmap <index, coordinate>  (list of tuples?)
        Collision prevention (borders + other tiles)    '''

    def __init__(self, BOARD_SIZE, SEQUENCE_LENGTH, TILE_SIZE):
        self.tiles = list()
        self.rects = list()
        while len(self.tiles) != SEQUENCE_LENGTH:
            tile = self.getRandomCoordinate(BOARD_SIZE, TILE_SIZE)
            if self.noCollision(tile, TILE_SIZE):
                self.tiles.append(tile)
                self.rects.append(pygame.Rect(tile[0], tile[1], TILE_SIZE[0], TILE_SIZE[1]))

    def getCopy(self):
        return self.tiles

    def getRandomCoordinate(self, BOARD_SIZE, TILE_SIZE):
        x = random.randint(0 + TILE_SIZE[0], BOARD_SIZE[0] - TILE_SIZE[0])
        y = random.randint(0 + TILE_SIZE[1], BOARD_SIZE[1] - TILE_SIZE[1])
        return (x, y)

    def noCollision(self, tile, TILE_SIZE):
        new_tile = pygame.Rect(tile[0], tile[1], TILE_SIZE[0], TILE_SIZE[1])
        return new_tile.collidelistall(self.rects) == []

    def checkMouseClick(self, mouse_loc):
        for rect in self.rects:
            if rect.collidepoint(mouse_loc):
                return rect
        return None
