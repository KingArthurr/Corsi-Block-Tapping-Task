import random
import pygame

''' Class used for controlling the board.
    Takes care of creating and plotting tiles etc.
    Used as Model   '''


class Board:
    ''' coordinates 1000x700
        Tile size 99x99
        Tile coordinate is middle of tile
        Export initial sequence plot Hashmap <index, coordinate>  (list of tuples?)
        Collision prevention (borders + other tiles)    '''
    
    '''Initalize board by provide list with tile coordinates and list of rectangles'''
    def __init__(self, SCREEN_SIZE, SEQUENCE_LENGTH, TILE_SIZE):
        '''Make a list for the tiles, which contains the x and y coordinates of tiles'''
        self.tiles = list()
        '''Make a list for the rectangles, which contains the rectangle objects of tiles'''
        self.rects = list()
        '''While loop to ensure that the amount of rectangles is equal to the SEQUENCE_LENGTH'''
        while len(self.tiles) != SEQUENCE_LENGTH:
            '''Get random coordinates for a tile'''
            tile = self.getRandomCoordinate(SCREEN_SIZE, TILE_SIZE)
            '''The random coordinate of the tile is checked with the list of rectangles (other tiles) if there is no collision'''
            if self.noCollision(tile, TILE_SIZE):
                '''The tile does not have collision with tiles in rectangle list, so added to list tiles'''
                self.tiles.append(tile)
                '''The tile does not have collision with tiles in rectangle list, so added to rectangle list'''
                self.rects.append(pygame.Rect(tile[0], tile[1], TILE_SIZE[0], TILE_SIZE[1]))
    
    '''Returns list of tiles'''
    def getCopy(self):
        return self.tiles
    
    '''Returns random coordinates which are on the screen and have a tilesize length distance from the borders'''
    def getRandomCoordinate(self, SCREEN_SIZE, TILE_SIZE):
        '''Gives a random x-coordinate for a tile, within the range (0 + tile width) till (screen x max - tile width). This to be able to display a tile as a whole'''
        x = random.randint(0 + TILE_SIZE[0], SCREEN_SIZE[0] - TILE_SIZE[0])
        '''Gives a random y-coordinate for a tile, within the range (0 + tile height) till (screen y max - tile height). This to be able to display a tile as a whole'''
        y = random.randint(0 + TILE_SIZE[1], SCREEN_SIZE[1] - TILE_SIZE[1])
        return (x, y)
    
    '''Returns boolean if tile (rectangle) collides with the other tiles in list''' 
    def noCollision(self, tile, TILE_SIZE):
        '''Create a new rectangle object with the random coordinates of the tile checked for collision. The +1 is added to the tile width and tile height to have at least one pixel between two tiles'''
        new_tile = pygame.Rect(tile[0], tile[1], TILE_SIZE[0] + 1, TILE_SIZE[1] + 1)
        '''The function collideslistall gives back a list containing which rectangles collide. A boolean is returned if that list equals an empty list, in other words if tiles collide'''
        return new_tile.collidelistall(self.rects) == []
    
    '''Returns the rectangle, if mouseclick is on a rectangle and returns None if no rectangle is cllicked'''
    def checkMouseClick(self, mouse_loc):
        '''Iterate over the list with rectangles'''
        for rect in self.rects:
            '''Checks if mouse location is on a rectangle'''
            if rect.collidepoint(mouse_loc):
                '''Returns clicked rectangle'''
                return rect
        ''''Returns None, because no rectangle clicked'''
        return None
