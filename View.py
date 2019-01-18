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

<<<<<<< HEAD
    """Draws text"""
    def draw_text (self, text, div1, div2, small):
        """If text needs to be small"""
        if small: 
            """Render text and store it as variable text_surface"""
            text_surface = self.font_small.render(text,  # Text
                                        True,  # Antialias
                                        self.col_darkblue,  # Text color (R,G,B)
                                        self.BACKGR_COL)  # Background color (R.G.B)
            """Get the rectangle around the text of text_surface and store it as varaible text_rectangle"""
            text_rectangle = text_surface.get_rect()  # Rect
            """Center the rectangle with text around x and y coordinates"""
            text_rectangle.center = (self.SCREEN_SIZE[0] / div1,  # Center X
                                 self.SCREEN_SIZE[1] / div2)  # Center Y
            """Draw text on rectangle on screen"""
            self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)
            """If text does not have to be small"""
        else:
            """Render text and store it as variable text_surface"""
            text_surface = self.font.render(text,  # Text
                                        True,  # Antialias
                                        self.col_darkblue,  # Text color (R,G,B)
                                        self.BACKGR_COL)  # Background color (R.G.B)
            """Get the rectangle around the text of text_surface and store it as varaible text_rectangle"""
            text_rectangle = text_surface.get_rect()  # Rect
            """Center the rectangle with text around x and y coordinates"""
            text_rectangle.center = (self.SCREEN_SIZE[0] / div1,  # Center X
                                 self.SCREEN_SIZE[1] / div2)  # Center Y
            """Draw text on rectangle on screen"""
            self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)
            
=======
>>>>>>> 23fa4dee3af7796d9f4519c18795fbe10c6748f3
    """Draws welcome screen"""

    def draw_welcome(self):
        """Draw welcome screen title"""
        self.draw_text("Corsi Block Tapping Task",  # Text
                       2,  # Div1 X
                       4,  # Div2 Y
                       False)  # Small Boolean
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

    """Draws question screen"""

    def draw_question(self, input_boxes):  # List<InputBoxes> 
        """Draw title"""
        self.draw_text("First some questions",  # Text
                       2,  # Div1 X
                       10,  # Div2 Y
                       True)  # Small Boolean

        """Draw Initials Question"""
        self.draw_text("Initials (letters only)",  # Text
                       3.5,  # Div1 X
                       5,  # Div2 Y
                       True)  # Small Boolean

        """Draw Age Question"""
        self.draw_text("Age",  # Text
                       3.5,  # Div1 X
                       3.33,  # Div2 Y
                       True)  # Small Boolean

        """Draw Gender Question"""
        self.draw_text("Gender (M/F)",  # Text
                       3.5,  # Div1 X
                       2.5,  # Div2 Y
                       True)  # Small Boolean

        """For every box in input_boxes list"""
        # InputBox in List<InputBox>
        for box in input_boxes:
            """Update the box"""
            box.update()  # InputBox.update()
            """Draw the box on the screen"""
            self.draw_inputbox(box)  # (InputBox)

        """Draw Start button"""
        # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN Game.py
        self.draw_button("Start",  # Text
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

    """Draw the trial with given board and clicked sequence"""

    def draw_trial(self, tiles,  # List<(Tile X, Tile Y)>
                   clickedseq):  # List<(Clicked Tile X, Clicked Tile Y)>
        """Draw instructions"""
        self.draw_text("Click on the tiles in order of the shown sequence",  # Text
                       2.0,  # Div1 X
                       1.05,  # Div2 Y
                       True)  # Small Boolean

        """For each tile in tiles list do:"""
        # (Tile X, Tile Y) in List<(Tile X, Tile Y)>
        for tile in tiles:
            """Draw the tiles"""
            self.draw_button(" ",  # Text
                             tile[0],  # X Coordinate
                             tile[1],  # Y Coordinate
                             self.TILE_SIZE[0],  # Width
                             self.TILE_SIZE[1],  # Height
                             self.col_darkblue,  # Inactive color (R,G,B)
                             self.col_bright_yellow)  # Active color (R,G,B)

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
            """Draw feedback text"""

            self.draw_text("You had the correct sequence of blocks",  # Text
                           2.0,  # Div1 X
                           5,  # Div2 Y
                           True)  # Small Boolean

            """If player did not complete the sequence"""
        elif not correct:
            """Draw feedback text"""
            self.draw_text("You had an incorrect sequence of blocks",  # Text
                           2.0,  # Div1 X
                           5,  # Div2 Y
                           True)  # Small Boolean

        """Draw completion time of the sequence"""
        self.draw_text("Your completion time was: " + str(time) + " seconds",  # Text
                       2.0,  # Div1 X
                       2.5,  # Div2 Y
                       True)  # Small Boolean

        """If maximum amount of errors has been reached"""
        # Boolean == True
        if errors_reached:
            """Draw notification"""
            self.draw_text("Maximum amount of errors reached",  # Text
                           2.0,  # Div1 X
                           1.667,  # Div2 Y
                           True)  # Small Boolean

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
        self.draw_text("You have a WMC of " + str(resultsRaw['Seq len'].max()),  # Text
                       2.0,  # Div1 X
                       5,  # Div2 Y
                       True)  # Small Boolean

        """Draw average completion time"""
<<<<<<< HEAD
        self.draw_text("Your average completion time is " + str(resultsRaw['Trial time'].mean()) + " s", 2.0, 2.5, True)
=======
        self.draw_text("Your average completion time is " + str(resultsRaw['Trial time'].mean()) + " s",  # Text
                       2.0,  # Div1 X
                       2.5,  # Div2 Y
                       True)  # Small Boolean
>>>>>>> 23fa4dee3af7796d9f4519c18795fbe10c6748f3

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

    """Draws text"""

    def draw_text(self, text,  # Text
                  div1,  # Div1 X
                  div2,  # Div2 Y
                  small):  # Small Boolean
        """If text needs to be small"""
        if small:
            """Render text and store it as variable text_surface"""
            text_surface = self.font_small.render(text,  # Text
                                                  True,  # Antialias
                                                  self.col_darkblue,  # Text color (R,G,B)
                                                  self.BACKGR_COL)  # Background color (R.G.B)
            """Get the rectangle around the text of text_surface and store it as varaible text_rectangle"""
            text_rectangle = text_surface.get_rect()  # Rect
            """Center the rectangle with text around x and y coordinates"""
            text_rectangle.center = (self.SCREEN_SIZE[0] / div1,  # Center X
                                     self.SCREEN_SIZE[1] / div2)  # Center Y
            """Draw text on rectangle on screen"""
            self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)
            """If text does not have to be small"""
        else:
            """Render text and store it as variable text_surface"""
            text_surface = self.font.render(text,  # Text
                                            True,  # Antialias
                                            self.col_darkblue,  # Text color (R,G,B)
                                            self.BACKGR_COL)  # Background color (R.G.B)
            """Get the rectangle around the text of text_surface and store it as varaible text_rectangle"""
            text_rectangle = text_surface.get_rect()  # Rect
            """Center the rectangle with text around x and y coordinates"""
            text_rectangle.center = (self.SCREEN_SIZE[0] / div1,  # Center X
                                     self.SCREEN_SIZE[1] / div2)  # Center Y
            """Draw text on rectangle on screen"""
            self.screen.blit(text_surface, text_rectangle)  # (Surface source, Rect area)

    """Clean screen by filling with BACKGR_COL"""

    """Draw the InputBox on given Surface"""

    def draw_inputbox(self, box):  # Surface
        """Blit the text"""
        self.screen.blit(box.txt_surface, (box.rect.x + 5, box.rect.y + 5))  # (Surface source, Rect area)

        """Blit the rect"""
        pygame.draw.rect(self.screen,  # Surface
                         box.color,  # Color (R,G,B)
                         box.rect,  # Rect(X,Y,W,H)
                         2)  # Thickness edge

    def refreshSurface(self):
        self.screen.fill(self.BACKGR_COL)  # Color (R,G,B)

    """Update pygame display"""

    def updateDisplay(self):
        pygame.display.update()
