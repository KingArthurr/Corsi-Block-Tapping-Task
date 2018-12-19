import pygame
import sys
from pygame.locals import *
from time import time, ctime
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


    def draw_trial(self, tiles, clickedseq):
        for tile in tiles:
            pygame.draw.rect(self.screen, self.col_black, (tile[0], tile[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

        for click in clickedseq:
            pygame.draw.rect(self.screen, self.col_yellow, (click[0], click[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))



    def draw_sequence(self, sequence):
        for seq in sequence:
            time_start = time()
            pygame.draw.rect(self.screen, self.col_yellow, (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))
            self.updateDisplay();
            bool = True
            while bool:
                if time() - time_start == 1:
                    pygame.draw.rect(self.screen, self.col_black,
                                     (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))
                    self.updateDisplay();
                    bool = False

    def draw_final(self, WMC = 0, avgTime = 1):
        text_surface = self.font_small.render("You have a WMC of " + str(WMC) + "s", True, self.col_black, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 150)
        self.screen.blit(text_surface, text_rectangle)

        text_surface = self.font_small.render("Your average completion time is " + str(int(avgTime * 1000)) + "ms", True, self.col_black, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 300)
        self.screen.blit(text_surface, text_rectangle)
