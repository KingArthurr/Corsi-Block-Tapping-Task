from time import time

import pygame

""" This class will be used to control the pygame UI and will be used as the Viewer"""


class View:
    """Initialise colors used for screen"""
    col_red = (200, 0, 0)
    col_green = (0, 200, 0)
    col_yellow = (250, 250, 0)
    col_darkblue = (0, 0, 139)
    col_bright_green = (0, 255, 0)
    col_bright_red = (255, 0, 0)

    BACKGR_COL = (250, 250, 250)

    """Initialise global variables"""
    screen = None
    font = None
    font_small = None

    """Initialise View()"""

    def __init__(self, screen, SCREEN_SIZE, TILE_SIZE):
        """Set screen, SCREEN_SIZE and TILE_SIZE as given"""
        self.screen = screen
        self.SCREEN_SIZE = SCREEN_SIZE
        self.TILE_SIZE = TILE_SIZE

        """Set the screens backgroundcolour to BACKGR_COL"""
        self.screen.fill(self.BACKGR_COL)

        """Set fonts"""
        self.font = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 40)

    """Draw the welcome screen"""

    def draw_welcome(self):
        """Draw welcome screen title"""
        text_surface = self.font.render("Corsi Block Tapping Task",
                                        True,
                                        self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / 4)
        self.screen.blit(text_surface, text_rectangle)

        """Draw Start button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Start",
                         self.SCREEN_SIZE[0] / 3 - (150 / 2),
                         self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),
                         150, 75,
                         self.col_green, self.col_bright_green)

        """Draw Quit button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Quit",
                         self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),
                         self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),
                         150, 75,
                         self.col_red, self.col_bright_red)

    """Draw the trial with given board and clicked sequence"""

    def draw_trial(self, tiles, clickedseq):
        """For each tile in tiles list do:"""
        for tile in tiles:
            """Draw tile on screen"""
            pygame.draw.rect(self.screen, self.col_darkblue,
                             (tile[0], tile[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

        """For each clicked tile in clickedseq list do:"""
        for click in clickedseq:
            """Draw tile on screen with different colour, overriding old tile"""
            pygame.draw.rect(self.screen, self.col_yellow,
                             (click[0], click[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

    """Show the given sequence"""

    def draw_sequence(self, sequence):
        """For each tile in sequence list do:"""
        for seq in sequence:
            """Set time_start to the current time"""
            time_start = time()

            """Draw tile on screen with different colour, overriding old tile"""
            pygame.draw.rect(self.screen, self.col_yellow,
                             (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

            """Update pygame display to show changes"""
            self.updateDisplay()

            """Start loop"""
            while True:
                """If one second has been reached or passed"""
                if time() - time_start >= 1:
                    """Draw tile on screen with original colour, overriding changed tile"""
                    pygame.draw.rect(self.screen, self.col_darkblue,
                                     (seq[0], seq[1], self.TILE_SIZE[0], self.TILE_SIZE[1]))

                    """Update pygame display to show changes"""
                    self.updateDisplay()

                    """Break out of while loop"""
                    break

    """Draw the feedback screen with trial time and if clicked sequence was correct"""

    def draw_feedback(self, time, correct, errors_reached):
        """If player completed the sequence"""
        if correct:
            """Set text"""
            text_surface = self.font_small.render("You had the correct sequence of blocks",
                                                  True,
                                                  self.col_darkblue, self.BACKGR_COL)

            """If player did not complete the sequence"""
        elif not correct:
            """Set text"""
            text_surface = self.font_small.render("You had an incorrect sequence of blocks",
                                                  True,
                                                  self.col_darkblue, self.BACKGR_COL)

        """"Draw text"""
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] * 1 / 5)
        self.screen.blit(text_surface, text_rectangle)

        """Draw completion time of the sequence"""
        text_surface = self.font_small.render("Your completion time was: " + str(time) + " seconds",
                                              True,
                                              self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] * 2 / 5)
        self.screen.blit(text_surface, text_rectangle)

        """If maximum amount of errors has been reached"""
        if errors_reached:
            """Draw notification"""
            text_surface = self.font_small.render("Maximum amount of errors reached",
                                                  True,
                                                  self.col_darkblue, self.BACKGR_COL)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] * 3 / 5)
            self.screen.blit(text_surface, text_rectangle)

            """Draw quit button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Quit",
                             self.SCREEN_SIZE[0] / 2 - (200 / 2),
                             self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),
                             200, 100,
                             self.col_red, self.col_bright_red)

            """If maximum amount of errors has not been reached"""
        else:
            """Draw Next trial button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Next trial",
                             self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),
                             self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                             150, 75,
                             self.col_green, self.col_bright_green)

            """Draw Quit button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Quit",
                             self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),
                             self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                             150, 75,
                             self.col_red, self.col_bright_red)

    """Draw the final screen with WMC and average trial time"""

    def draw_final(self, WMC=0, avgTime=1):
        """Draw WMC score"""
        text_surface = self.font_small.render("You have a WMC of " + str(WMC),
                                              True,
                                              self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] * 1 / 4)
        self.screen.blit(text_surface, text_rectangle)

        """Draw average completion time"""
        text_surface = self.font_small.render("Your average completion time is " + str(int(avgTime * 1000)) + " ms",
                                              True,
                                              self.col_darkblue, self.BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0, self.SCREEN_SIZE[1] * 2 / 4)
        self.screen.blit(text_surface, text_rectangle)

        """Draw Quit button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Quit",
                         self.SCREEN_SIZE[0] / 2 - (150 / 2),
                         self.SCREEN_SIZE[1] * 3 / 4 - (100 / 2),
                         200, 100,
                         self.col_red, self.col_bright_red)

    def draw_button(self, msg, x, y, w, h, ic, ac):
        """Get current mouse position"""
        mouse = pygame.mouse.get_pos()

        """If mouse position is on a button"""
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            """Draw rectangle in bright colour"""
            pygame.draw.rect(self.screen, ac,
                             (x, y, w, h))

            """Set text to msg with bright colour background"""
            text_surface = self.font_small.render(msg,
                                                  True,
                                                  self.col_darkblue, ac)

            """If mouse position is not on a button"""
        else:
            """Draw rectagle with normal colour"""
            pygame.draw.rect(self.screen, ic,
                             (x, y, w, h))

            """Set text to msg with normal colour"""
            text_surface = self.font_small.render(msg,
                                                  True,
                                                  self.col_darkblue, ic)

        """Draw text with msg and set background"""
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text_surface, text_rectangle)

    """Clean screen by filling with BACKGR_COL"""

    def refreshSurface(self):
        self.screen.fill(self.BACKGR_COL)

    """Update pygame display"""

    def updateDisplay(self):
        pygame.display.update()
