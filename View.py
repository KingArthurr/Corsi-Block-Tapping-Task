import pygame
import sys
from pygame.locals import *
from pygame.compat import unichr_, unicode_

''' This class will be used to control the pygame UI and will be used as the Viewer'''

class View:

    ''' Screen size 1000x800
        Tile size 99x99
        Tile coordinate is middle of tile
        Bottom Bar Score, Button (Next, Done)
        Tiles flash color to show sequence
        Tiles become color upon clicking and get sequence number
        Export Hashmap <index, coordinate>  (list of tuples?)   '''

    # Colors abd screen
    col_white = (250, 250, 250)
    col_black = (0, 0, 0)
    col_gray = (220, 220, 220)
    col_red = (250, 165, 0)
    col_green = (0, 200, 0)
    col_blue = (0, 0, 250)
    col_yellow = (250, 250, 0)

    WORDS = ("red", "green", "blue", "black")

    COLORS = {"red": col_red,
              "green": col_green,
              "blue": col_blue,
              "black": col_black}

    KEYS = {"red": K_q,
            "green": K_w,
            "blue": K_e,
            "black": K_r}

    BACKGR_COL = col_gray

    screen = None
    font = None
    font_small = None

    def __init__(self, screen, SCREEN_SIZE, TILE_SIZE):
        self.screen = screen
        self.SCREEN_SIZE = SCREEN_SIZE
        self.TILE_SIZE = TILE_SIZE


        self.screen.fill(self.BACKGR_COL)

        self.font = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 40)

    def refreshSurface(self):
        self.screen.fill(self.BACKGR_COL)

    def updateDisplay(self):
        # Updating the display
        pygame.display.update()

    def draw_welcome(self):
        text_surface = self.font.render("Corsi Block Tapping Task", True, self.col_black, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] / 2.5)
        self.screen.blit(text_surface, text_rectangle)
        text_surface = self.font_small.render("Press Spacebar to continue", True, self.col_black, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] / 2.0)
        self.screen.blit(text_surface, text_rectangle)


    def draw_button(self, xpos, ypos, label, color):

        text = self.font_small.render(label, True, color, self.BACKGR_COL)
        text_rectangle = text.get_rect()
        text_rectangle.center = (xpos, ypos)
        self.screen.blit(text, text_rectangle)

    def draw_trial(self, tiles, sequence):

        for tile in tiles:
            pygame.draw.rect(self.screen, self.col_black, (tile[0], tile[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))
