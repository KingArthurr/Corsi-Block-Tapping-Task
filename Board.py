import random

from pygame import Rect

""" Class used for controlling the board. Takes care of creating and plotting tiles etc. Used as Model   """


class Board:
    """Initalize board by provide list with tile coordinates and list of rectangles"""

    def __init__(self, SCREEN_SIZE,  # (Screen Width, Screen Heigth)
                 SEQUENCE_LENGTH,  # Int
                 TILE_SIZE):  # (Tile Width, Tile Heigth)
        """Make a list for the tiles, which contains the x and y coordinates of tiles"""
        self.tiles = list()  # Empty List

        """Make a list for the rectangles, which contains the rectangle objects of tiles"""
        self.rects = list()  # Empty List

        """While loop to ensure that the amount of rectangles is equal to the SEQUENCE_LENGTH"""
        # While length of List doest not equal Int
        while len(self.tiles) != SEQUENCE_LENGTH:
            """Get random coordinates for a tile. Screensize is edited to allow for instructions at the bottom"""
            tile = self.getRandomCoordinate((SCREEN_SIZE[0], SCREEN_SIZE[1] * 0.9), TILE_SIZE)  # (Tile X, Tile Y)

            """The random coordinate of the tile is checked with the list of rectangles (other tiles) 
                if there is no collision"""
            if self.noCollision(tile, TILE_SIZE):  # Boolean ((Tile X, Tile Y),(Tile Width, Tile Heigth))
                """The tile does not have collision with tiles in rectangle list, so added to list tiles"""
                self.tiles.append(tile)  # (Tile X, Tile Y)

                """The tile does not have collision with tiles in rectangle list, so added to rectangle list"""
                self.rects.append(
                    Rect(tile[0], tile[1], TILE_SIZE[0], TILE_SIZE[1]))  # Rect(Tile X, Tile Y, Tile Width, Tile Height)

    """Returns list of tiles"""

    def getCopy(self):
        return self.tiles  # List<(Tile X, Tile Y)>

    """Returns random coordinates which are on the screen and have a tilesize length distance from the borders"""

    def getRandomCoordinate(self, SCREEN_SIZE,  # (Screen Width, Screen Heigth)
                            TILE_SIZE):  # (Tile Width, Tile Heigth)
        """Gives a random x-coordinate for a tile"""
        # Random value between 1 + Tile Width and Screen Width - 1 - Tile Width
        x = random.randint(1 + TILE_SIZE[0], SCREEN_SIZE[0] - 1 - TILE_SIZE[0])  # Int

        """Gives a random y-coordinate for a tile"""
        # Random value between 1 + Tile Height and Screen Height - 1 - Tile Height
        y = random.randint(1 + TILE_SIZE[1], SCREEN_SIZE[1] - 1 - TILE_SIZE[1])  # Int

        """return random coordinates"""
        return (x, y)  # (Tile X, Tile Y)

    """Returns boolean if tile (rectangle) collides with the other tiles in list"""

    def noCollision(self, tile,  # (Tile X, Tile Y)
                    TILE_SIZE):  # (Tile Width, Tile Height)
        """Create a new rectangle object with the random coordinates of the tile checked for collision.
            Location and size are changed to create a 1 pixel buffer between the rectangles."""
        new_tile = Rect(tile[0] - 1, tile[1] - 1,  # Rect(Tile X - 1, Tile Y - 1,
                        TILE_SIZE[0] + 2, TILE_SIZE[1] + 2)  # Tile Width + 2, Tile Height + 2)

        """The function collideslistall gives back a list containing which rectangles collide. 
            A boolean is returned if that list equals an empty list, in other words if tiles collide"""
        return new_tile.collidelistall(self.rects) == []  # Boolean

    """Returns the rectangle, if mouseclick is on a rectangle and returns None if no rectangle is cllicked"""

    def checkMouseClick(self, mouse_loc):  # (Mouse X, Mouse Y)
        """Iterate over the list with rectangles"""
        # for Rect in List<Rect>
        for rect in self.rects:
            """Checks if mouse location is on a rectangle"""
            if rect.collidepoint(mouse_loc):
                """Returns clicked rectangle"""
                return rect  # Rect

        """Returns None, because no rectangle clicked"""
        return None  # None
