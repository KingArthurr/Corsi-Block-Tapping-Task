from time import time

import matplotlib
import pygame


matplotlib.use("Agg")

import pylab
import matplotlib.backends.backend_agg as agg
from matplotlib.ticker import MaxNLocator

""" This class will be used to control the pygame UI and will be used as the Viewer"""


class View:
    """Initialise View()"""

    def __init__(self, screen,  # Surface
                 SCREEN_SIZE,  # (Screen Width, Screen Heigth)
                 TILE_SIZE):  # (Tile Width, Tile Heigth)
        """Initialise colors used for screen"""
        self.col_red = (200, 0, 0)  # (R,G,B)
        self.col_green = (0, 200, 0)  # (R,G,B)
        self.col_yellow = (255, 255, 0)  # (R,G,B)
        self.col_darkblue = (0, 0, 139)  # (R,G,B)
        self.col_bright_green = (0, 255, 0)  # (R,G,B)
        self.col_bright_red = (255, 0, 0)  # (R,G,B)
        self.col_bright_yellow = (200, 200, 0)  # (R,G,B)

        self.BACKGR_COL = (250, 250, 250)  # (R,G,B)

        """Set fonts"""
        self.font = pygame.font.Font(None, 80)  # (object/filename, size)
        self.font_small = pygame.font.Font(None, 40)  # (object/filename, size)
        self.font_tiny = pygame.font.Font(None, 20)  # (object/filename, size)

        """Set screen, SCREEN_SIZE and TILE_SIZE as given"""
        self.screen = screen  # Surface
        self.SCREEN_SIZE = SCREEN_SIZE  # (Screen Width, Screen Heigth)
        self.TILE_SIZE = TILE_SIZE  # (Tile Width, Tile Heigth)

        """Set the screens backgroundcolour to BACKGR_COL"""
        self.screen.fill(self.BACKGR_COL)  # Color (R,G,B)

    """Draw the welcome screen"""

    def draw_welcome(self):
        """Draw welcome screen title"""
        text_surface = self.font.render("Corsi Block Tapping Task",  # Text
                                        True,  # Antialias
                                        self.col_darkblue,  # Text color (R,G,B)
                                        self.BACKGR_COL)  # Background color (R.G.B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2,  # Center X
                                 self.SCREEN_SIZE[1] / 4)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw Start button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Start",  # Text
                         self.SCREEN_SIZE[0] / 3 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),  # Y Coordinate
                         150,  # Width
                         75,  # Heigth
                         self.col_green,  # Inactive color (R,G,B)
                         self.col_bright_green)  # Active color (R,G,B)

        """Draw Quit button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Quit",  # Text
                         self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),  # Y Coordinate
                         150,  # Width
                         75,  # Heigth
                         self.col_red,  # Inactive color (R,G,B)
                         self.col_bright_red)  # Active color (R,G,B)

    """"""  # TODO comment

    def draw_question(self, input_boxes):  # List<InputBoxes> 
        """Draw title"""
        text_surface = self.font.render("First some questions",  # Text
                                        True,  # Antialias
                                        self.col_darkblue,  # Text color (R,G,B)
                                        self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 1 / 10)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw Initials Question"""
        text_surface = self.font_small.render("Initials (letters only)",  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] * 2 / 7,  # Center X
                                 self.SCREEN_SIZE[1] * 2 / 10)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw Age Question"""
        text_surface = self.font_small.render("Age",  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] * 2 / 7,  # Center X
                                 self.SCREEN_SIZE[1] * 3 / 10)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw Gender Question"""
        text_surface = self.font_small.render("Gender (M/F)",  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] * 2 / 7,  # Center X
                                 self.SCREEN_SIZE[1] * 4 / 10)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """For every box in input_boxes list"""
        # InputBox in List<InputBox>
        for box in input_boxes:
            """Update the box"""
            box.update()  # InputBox.update()
            """Draw the box on the screen"""
            box.draw(self.screen)  # #InputBox.draw(Surface)

        """Draw Start button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Start",  # Text
                         self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                         150,  # Width
                         75,  # Heigth
                         self.col_green,  # Inactive color (R,G,B)
                         self.col_bright_green)  # Active color (R,G,B)

        """Draw Quit button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Quit",  # Text
                         self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                         150,  # Width
                         75,  # Heigth
                         self.col_red,  # Inactive color (R,G,B)
                         self.col_bright_red)  # Active color (R,G,B)

    """Draw the trial with given board and clicked sequence"""

    def draw_trial(self, tiles,  # List<(Tile X, Tile Y)>
                   clickedseq):  # List<(Clicked Tile X, Clicked Tile Y)>
        """Draw instructions"""
        text_surface = self.font_small.render("Click on the tiles in order of the shown sequence",  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 19 / 20)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Get current mouse position"""
        mouse = pygame.mouse.get_pos()  # (Mouse X, Mouse Y)

        """For each tile in tiles list do:"""
        # (Tile X, Tile Y) in List<(Tile X, Tile Y)>
        for tile in tiles:
            """If mouse position is on a tile"""
            # Tile X + Tile Width > Mouse X > Tile width
            # and Tile X + Tile Heigth > Mouse Y > Tile Heigth
            if tile[0] + self.TILE_SIZE[0] > mouse[0] > tile[0] \
                    and tile[1] + self.TILE_SIZE[1] > mouse[1] > tile[1]:
                """Draw rectangle in bright colour"""
                pygame.draw.rect(self.screen,  # Surface
                                 self.col_bright_yellow,  # Color (R,G,B)
                                 (tile[0], tile[1],  # Rect X,Y
                                  self.TILE_SIZE[0], self.TILE_SIZE[1]))  # Rect W,H
                """If mouse position is not on a button"""
            else:
                """Draw rectagle with normal colour"""
                pygame.draw.rect(self.screen,  # Surface
                                 self.col_darkblue,  # Color (R,G,B)
                                 (tile[0], tile[1],  # Rect X,Y
                                  self.TILE_SIZE[0], self.TILE_SIZE[1]))  # Rect W,H

        """For each clicked tile in clickedseq list do:"""
        for click in clickedseq:
            """Draw tile on screen with different colour, overriding old tile"""
            pygame.draw.rect(self.screen,  # Surface
                             self.col_yellow,  # Color (R,G,B)
                             (click[0], click[1],  # Rect X,Y
                              self.TILE_SIZE[0], self.TILE_SIZE[1]))  # Rect W,H
        self.updateDisplay()

    """Show the given sequence"""

    def draw_sequence(self, sequence):  # List<(Tile X, Tile Y)>
        """Check if this is the first sequence of the game"""
        # if length of List<(Tile X, Tile Y)> <= 2
        if len(sequence) <= 2:
            """Set timer to allow player to read instructions before showing the sequence"""
            time_start = time()  # Float seconds since the epoch, in UTC
            while True:
                """If five seconds have passed"""
                if time() - time_start > 5:
                    """Break out of while loop"""
                    break

        """For each tile in sequence list do:"""
        # (Tile X, Tile Y) in List<(Tile X, Tile Y)>
        for seq in sequence:
            """Draw tile on screen with different colour, overriding old tile"""
            pygame.draw.rect(self.screen,  # Surface
                             self.col_yellow,  # Color (R,G,B)
                             (seq[0], seq[1],  # Rect X,Y
                              self.TILE_SIZE[0], self.TILE_SIZE[1]))  # Rect W,H

            """Update pygame display to show changes"""
            self.updateDisplay()

            """Set time_start to the current time"""
            time_start = time()  # Float seconds since the epoch, in UTC

            """Start loop"""
            while True:
                """If one second has been reached or passed"""
                if time() - time_start >= 1:
                    """Draw tile on screen with original colour, overriding changed tile"""
                    pygame.draw.rect(self.screen,  # Surface
                                     self.col_darkblue,  # Color (R,G,B)
                                     (seq[0], seq[1],  # Rect X,Y
                                      self.TILE_SIZE[0], self.TILE_SIZE[1]))  # Rect W,H

                    """Update pygame display to show changes"""
                    self.updateDisplay()

                    """Break out of while loop"""
                    break

    """Draw the feedback screen with trial time and if clicked sequence was correct"""

    def draw_feedback(self, time,  # Completion time
                      correct,  # Boolean sequence completed
                      errors_reached):  # Boolean maximum amount of errors reached
        """If player completed the sequence"""
        if correct:
            """Set text"""
            text_surface = self.font_small.render("You had the correct sequence of blocks",  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  self.BACKGR_COL)  # Background color (R,G,B)

            """If player did not complete the sequence"""
        elif not correct:
            """Set text"""
            text_surface = self.font_small.render("You had an incorrect sequence of blocks",  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  self.BACKGR_COL)  # Background color (R,G,B)

        """"Draw text"""
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 1 / 5)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw completion time of the sequence"""
        text_surface = self.font_small.render("Your completion time was: " + str(time) + " seconds",  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 2 / 5)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """If maximum amount of errors has been reached"""
        # Boolean == True
        if errors_reached:
            """Draw notification"""
            text_surface = self.font_small.render("Maximum amount of errors reached",  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  self.BACKGR_COL)  # Background color (R,G,B)
            text_rectangle = text_surface.get_rect()  # Rect
            text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                     self.SCREEN_SIZE[1] * 3 / 5)  # Center Y
            self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

            """Draw quit button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Quit",  # Text
                             self.SCREEN_SIZE[0] / 2 - (200 / 2),  # X Coordinate
                             self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),  # Y Coordinate
                             200,  # Width
                             100,  # Height
                             self.col_red,  # Inactive color (R,G,B)
                             self.col_bright_red)  # Active color (R,G,B)

            """If maximum amount of errors has not been reached"""
        else:
            """Draw Next trial button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Next trial",  # Text
                             self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),  # X Coordinate
                             self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                             150,  # Width
                             75,  # Height
                             self.col_green,  # Inactive color (R,G,B)
                             self.col_bright_green)  # Active color (R,G,B)

            """Draw Quit button"""
            # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
            self.draw_button("Quit",  # Text
                             self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                             self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                             150,  # Width
                             75,  # Height
                             self.col_red,  # Inactive color (R,G,B)
                             self.col_bright_red)  # Active color (R,G,B)

    """Draw the final screen with WMC and average trial time"""

    def draw_final(self, resultsRaw=[]):  # Dictionairy<Header,Result>
        """Draw WMC score"""
        text_surface = self.font_small.render("You have a WMC of " + str(resultsRaw['Seq len'].max()),  # Text
                                              True,  # Antialias
                                              self.col_darkblue,  # Text color (R,G,B)
                                              self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 1 / 5)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw average completion time"""
        text_surface = self.font_small.render(
            "Your average completion time is " + str(resultsRaw['Trial time'].mean()) + " s",  # Text
            True,  # Antialias
            self.col_darkblue,  # Text color (R,G,B)
            self.BACKGR_COL)  # Background color (R,G,B)
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 2 / 5)  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

        """Draw Results button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("See statistics",  # Text
                         self.SCREEN_SIZE[0] / 2 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 3 / 5 - (100 / 2),  # Y Coordinate
                         200,  # Width
                         75,  # Heigth
                         self.col_green,  # Inactive color (R,G,B)
                         self.col_bright_green)  # Active color (R,G,B)

        """Draw Quit button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Save & Quit",  # Text
                         self.SCREEN_SIZE[0] / 2 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),  # Y Coordinate
                         200,  # Width
                         100,  # Heigth
                         self.col_red,  # Inactive color (R,G,B)
                         self.col_bright_red)  # Active color (R,G,B)

    def draw_results(self, resultsRaw="ERROR"):  # DataFrame
        """Draw Plot from Datframe"""
        """Create figure"""
        fig = pylab.figure(figsize=[self.SCREEN_SIZE[0] / 150,  # Figure size width (Inches)
                                    self.SCREEN_SIZE[1] / 150],  # Figure size height (Inches)
                           dpi=100  # Resolution 100 dots per inch
                           )  # Figure

        """Get Axes from the figure"""
        ax = fig.gca()  # Axes

        """Plot Seq len on X axis and Trial time on Y axis"""
        ax.plot(resultsRaw['Seq len'].tolist(),  # List<X>
                resultsRaw['Trial time'].tolist(),  # List<Y>
                'bo')  # Using blue circle marker

        """Set Y label to Trial Time"""
        ax.set_ylabel('Trial time')

        """Set X label to Sequence length"""
        ax.set_xlabel('Sequence length')

        """Set title to Trial time for each sequence"""
        ax.set_title('Trial time for each sequence')

        """Force X axis to use integers"""
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        """Call the draw and print fig methods, creates the renderers, etc"""
        canvas = agg.FigureCanvasAgg(fig)

        """Draw the figure using the renderer."""
        canvas.draw()

        """Get the canvas renderer"""
        renderer = canvas.get_renderer()

        """Get the image as an RGB byte string."""
        raw_data = renderer.tostring_rgb()  # String

        """Draw Figure"""
        """Create new Surface from RGB byte string"""
        surf = pygame.image.fromstring(raw_data,  # RBG byte string
                                       canvas.get_width_height(),  # Size (Width,Height)
                                       "RGB")  # Format RGB
        text_rectangle = surf.get_rect()  # Rect
        text_rectangle.center = (self.SCREEN_SIZE[0] / 2.0,  # Center X
                                 self.SCREEN_SIZE[1] * 2 / 5)  # Center Y
        self.screen.blit(surf, text_rectangle)  # (Surface source, Rect area)

        """Draw Back button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Back",  # Text
                         self.SCREEN_SIZE[0] / 2 - (150 / 2),  # X Coordinate
                         self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),  # Y Coordinate
                         200,  # Width
                         100,  # Heigth
                         self.col_red,  # Inactive color (R,G,B)
                         self.col_bright_red)  # Active color (R,G,B)

    """Draws a button"""

    def draw_button(self, msg,  # Text
                    x,  # X Coordinate
                    y,  # Y Coordinate
                    w,  # Width
                    h,  # Heigth
                    ic,  # Inactive color (R,G,B)
                    ac):  # Active color (R,G,B)
        """Get current mouse position"""
        mouse = pygame.mouse.get_pos()  # (Mouse X, Mouse Y)

        """If mouse position is on a button"""
        # X + Width > Mouse X > width
        # and X + Heigth > Mouse Y > Heigth
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            """Draw rectangle in bright colour"""
            pygame.draw.rect(self.screen,  # Surface
                             ac,  # Color (R,G,B)
                             (x, y,  # Rect X,Y
                              w, h))  # Rect W,H

            """Set text to msg with bright colour background"""
            text_surface = self.font_small.render(msg,  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  ac)  # Background color (R,G,B)

            """If mouse position is not on a button"""
        else:
            """Draw rectagle with normal colour"""
            pygame.draw.rect(self.screen,  # Surface
                             ic,  # Color (R,G,B)
                             (x, y,  # Rect X,Y
                              w, h))  # Rect W,H

            """Set text to msg with normal colour"""
            text_surface = self.font_small.render(msg,  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  ic)  # Background color (R,G,B)

        """Draw text with msg and set background"""
        text_rectangle = text_surface.get_rect()  # Rect
        text_rectangle.center = ((x + (w / 2)),  # Center X
                                 (y + (h / 2)))  # Center Y
        self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

    """Clean screen by filling with BACKGR_COL"""

    def refreshSurface(self):
        self.screen.fill(self.BACKGR_COL)  # Color (R,G,B)

    """Update pygame display"""

    def updateDisplay(self):
        pygame.display.update()
