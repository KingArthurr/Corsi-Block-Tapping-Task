import random
import itertools

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

        while len(self.tiles) != SEQUENCE_LENGTH:
            tile = self.getRandomCoordinate(BOARD_SIZE)
            if self.noCollision(tile, self.tiles, BOARD_SIZE, TILE_SIZE):
                self.tiles.append(tile)


    def getCopy(self):
        return self.tiles

    def getRandomCoordinate(self, BOARD_SIZE):
        x = random.randint(0,BOARD_SIZE[0])
        y = random.randint(0, BOARD_SIZE[1])
        return (x, y)

    def noCollision(self, tile, tiles, BOARD_SIZE, TILE_SIZE):
        #TODO
        bool = True

        x_range = range(tile[0] - (TILE_SIZE[0]/2), tile[0] + (TILE_SIZE[0]/2) + 1);
        y_range = range(tile[1] - (TILE_SIZE[1] / 2), tile[1] + (TILE_SIZE[1] / 2) + 1);

        print(x_range)
        print(BOARD_SIZE[0])
        tuples = list(itertools.product(x_range, y_range))

        if any(x_range) < 0 or any(x_range) > BOARD_SIZE[0] or any(y_range) < 0 or any(y_range) > BOARD_SIZE[1]:
            bool = False

        return bool