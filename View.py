import pygame
from time import time

''' This class will be used to control the pygame UI and will be used as the Viewer'''


class View:
    """ Screen size 1000x800
        Tile size 99x99
        Tile coordinate is middle of tile
        Bottom Bar Score, Button (Next, Done)
        Tiles flash color to show sequence
        Tiles become color upon clicking and get sequence number
        Export Hashmap <index, coordinate>  (list of tuples?)   """

    # Colors abd screen
    col_white = (250, 250, 250)
    col_black = (0, 0, 0)
    col_gray = (220, 220, 220)
    col_red = (200, 0, 0)
    col_green = (0, 200, 0)
    col_blue = (0, 0, 250)
    col_yellow = (250, 250, 0)
    col_darkblue = (0, 0, 139)
    col_bright_green = (0, 255, 0)
    col_bright_red = (255, 0, 0)

    BACKGR_COL = col_white

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
        text_surface = self.font.render("Corsi Block Tapping Task", True, self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] / 4.0)
        self.screen.blit(text_surface, text_rectangle)

        self.draw_button("Start", 200, 450, 150, 75, self.col_green, self.col_bright_green, 40)
        self.draw_button("Quit", 600, 450, 150, 75, self.col_red, self.col_bright_red, 40)

    def draw_trial(self, tiles, clickedseq):
        for tile in tiles:
            pygame.draw.rect(self.screen, self.col_darkblue, (tile[0], tile[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

        for click in clickedseq:
            pygame.draw.rect(self.screen, self.col_yellow, (click[0], click[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

    def draw_sequence(self, sequence):
        for seq in sequence:
            time_start = time()
            pygame.draw.rect(self.screen, self.col_yellow, (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))
            self.updateDisplay()
            timeBool = True
            while timeBool:
                if time() - time_start >= 1:
                    pygame.draw.rect(self.screen, self.col_darkblue,
                                     (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))
                    self.updateDisplay()
                    timeBool = False

    def draw_feedback(self, time, correct, errors_reached):
        if correct:
            text_surface = self.font_small.render("You had the correct sequence of blocks", True, self.col_darkblue,
                                                  self.BACKGR_COL)
        elif not correct:
            text_surface = self.font_small.render("You had an incorrect sequence of blocks", True, self.col_darkblue,
                                                  self.BACKGR_COL)

        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 150)
        self.screen.blit(text_surface, text_rectangle)

        text_surface = self.font_small.render("Your completion time was: " + str(time) + " seconds", True,
                                              self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 300)
        self.screen.blit(text_surface, text_rectangle)

        if errors_reached:
            text_surface = self.font_small.render("Maximum amount of errors reached", True,
                                              self.col_darkblue, self.BACKGR_COL)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 400)
            self.screen.blit(text_surface, text_rectangle)

        if not errors_reached:
            self.draw_button("Next trial", 200, 450, 150, 75, self.col_green, self.col_bright_green, 30)
        self.draw_button("Quit", 600, 450, 150, 75, self.col_red, self.col_bright_red, 40)

    def draw_button(self, msg, x, y, w, h, ic, ac, textsize):
        mouse = pygame.mouse.get_pos()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", textsize)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.col_darkblue)
        return textSurface, textSurface.get_rect()

    def draw_final(self, WMC=0, avgTime=1):
        text_surface = self.font_small.render("You have a WMC of " + str(WMC), True, self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 150)
        self.screen.blit(text_surface, text_rectangle)

        text_surface = self.font_small.render("Your average completion time is " + str(int(avgTime * 1000)) + " ms",
                                              True, self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, 300)
        self.screen.blit(text_surface, text_rectangle)

        self.draw_button("Quit", 400, 450, 200, 100, self.col_red, self.col_bright_red, 45)
