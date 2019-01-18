import datetime
import random
import sys
from time import time

import matplotlib
import pandas
import pygame

matplotlib.use("Agg")

import pylab
import matplotlib.backends.backend_agg as agg
from matplotlib.ticker import MaxNLocator

SCREEN_SIZE = (1000, 800)  # (Screen width, Screen Height)
SEQUENCE_LENGTH = 9  # Max Sequence Length
ALLOW_ERRORS = 1  # Max Allowed Errors

""" This class is takes care of all the game logic and will be used as the Controller.  """


class Game:
    """Initialise Game()"""

    def __init__(self, SCREEN_SIZE=(1000, 800),  # (Width, Height) default=(1000,800)
                 SEQUENCE_LENGTH=9,  # Max Sequence Length default=9
                 ALLOW_ERRORS=1):  # Max Allowed Errors default=1
        """Initialize game settings"""
        self.SCREEN_SIZE = SCREEN_SIZE  # (Width, Height)
        self.SEQUENCE_LENGTH = SEQUENCE_LENGTH  # Max Sequence Length
        self.ALLOWED_ERRORS = ALLOW_ERRORS  # Max Allowed Errors

        """Set Tile Size to Smallest ScreenSize(X,Y) / Maximum Sequence Lenght - 1"""
        self.TILE_SIZE = (min(self.SCREEN_SIZE) / self.SEQUENCE_LENGTH - 1,  # Tile Width
                          min(self.SCREEN_SIZE) / self.SEQUENCE_LENGTH - 1)  # Tile Height

        """Global variables set up for boxinputboxes"""
        # FIXME add inputboxes for every added question
        # (self.input<Name> = InputBox(self.SCREEN_SIZE[0] * 4 / 7, self.SCREEN_SIZE[1] * <Int> / 40, 200, 32))
        self.inputID = InputBox(self.SCREEN_SIZE[0] * 4 / 7,  # X Coordinate
                                self.SCREEN_SIZE[1] * 7 / 40,  # Y Coordinate
                                200,  # Width
                                32)  # Height
        self.inputAge = InputBox(self.SCREEN_SIZE[0] * 4 / 7,  # X Coordinate
                                 self.SCREEN_SIZE[1] * 11 / 40,  # Y Coordinate
                                 200,  # Width
                                 32)  # Height
        self.inputGender = InputBox(self.SCREEN_SIZE[0] * 4 / 7,  # X Coordinate
                                    self.SCREEN_SIZE[1] * 15 / 40,  # Y Coordinate
                                    200,  # Width
                                    32)  # Height
        # FIXME add extra inputboxes to list
        # self.input<Name>
        self.input_boxes = [self.inputID, self.inputAge, self.inputGender]  # List <InputBox>
        self.spaceready = False  # Boolean

        """Initialize global variables"""

        self.board = None  # Board
        self.correct_seq = None  # Boolean
        self.sequence = None  # List<(Tile X, Tile Y)>
        self.clickedseq = None  # List<(Tile X, Tile Y)>
        self.player_errors = 0  # Int
        self.WMC = 0  # Int
        self.times = []  # List<Float>
        self.time_trial = None  # Float
        self.time_start = None  # Float
        self.resultsRaw = []  # Dictionairy<Header,Result>
        self.results = []  # Dictionairy<Header,Result>

        self.initials = None  # Text
        self.age = 0  # Int
        self.gender = None  # Text

        self.startTime = None  # Float
        self.endTime = None  # Float

        """Create PyGame screen"""
        """Initialize pygame"""
        pygame.init()
        """Set display size to SCREEN_SIzE"""
        pygame.display.set_mode(self.SCREEN_SIZE)
        """Set display caption to Corsi Block Tapping Task"""
        pygame.display.set_caption("Corsi Block Tapping Task")
        """Get display Surface"""
        screen = pygame.display.get_surface()  # Surface

        """Initialise View.py to control the screen"""
        self.view = View(screen,  # Surface
                         self.SCREEN_SIZE,  # (Screen Width, Screen Height)
                         self.TILE_SIZE)  # (Tile Width, Tile Height)

        """Start main game loop"""
        self.gameLoop()

    """Initialize Trial of length of current sequence"""

    def initializeTrial(self, CURRENT_SEQUENCELENGTH):  # Int
        """"Clean clickedseq by assigning new clean list()"""
        self.clickedseq = list()  # List<(Tile X, Tile Y)>

        """Clean board by creating new Board()"""
        self.board = Board(self.SCREEN_SIZE,  # (Screen Width, Screen Heigth)
                           self.SEQUENCE_LENGTH,  # Int
                           self.TILE_SIZE)  # (Tile Width, Tile Heigth)

        """Create a new sequence of length of current sequence"""
        self.createSequence(CURRENT_SEQUENCELENGTH)  # Int

        """Tell View.py to draw the trial and show the sequence"""
        self.view.draw_trial(self.board.getCopy(), self.clickedseq)  # (Board, # List<(Tile X, Tile Y)>)
        self.view.draw_sequence(self.getSequence())  # (List<(Tile X, Tile Y)>)

        """Set correct_seq to False to indicate player has not yet entered the correct sequence"""
        self.correct_seq = False  # Boolean

    """Create a sequence of length of given variable CURRENT_SEQUENCELENGTH"""

    def createSequence(self, CURRENT_SEQUENCELENGTH):  # Int
        """Get copy of the tiles in the board from Board.py"""
        tiles = self.board.getCopy()  # List<(Tile X, Tile Y)>

        """Shuffle them to always select a random tile"""
        random.shuffle(tiles)  # Random(List<(Tile X, Tile Y)>)

        """Clean sequence by assigning new clean list()"""
        self.sequence = list()  # List<(Tile X, Tile Y)>

        """Add CURRENT_SEQUENCELENGTH amount of tiles from randomized tiles list to sequence"""
        # For every number from 0 to CURRENT_SEQUENCELENGTH
        for j in range(CURRENT_SEQUENCELENGTH):
            self.sequence.append(tiles[j])  # (Tile X, Tile Y)

    """Getter method that returns sequence list"""

    def getSequence(self):
        return self.sequence  # List<(Tile X, Tile Y)>

    """Check if button on location (x,y) with width w and height h is pressed"""

    def button_pressed(self, x,  # X Coordinate
                       y,  # Y Coordinate
                       w,  # Width
                       h):  # Heigth
        """Create clicked boolean and set to False"""
        clicked = False  # Boolean

        """Get mouse pointer position and pressed mouse buttons"""
        mouse = pygame.mouse.get_pos()  # (Mouse X, Mouse Y)
        click = pygame.mouse.get_pressed()  # (Mouse left bit, Mouse middle bit, Mouse right bit)

        """Check if the mouse cursor is on the button"""
        # If X Coordinate + Width > Mouse X > X Coordinate and Y Coordinate + Height > Mouse Y > Y Coordinate
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            """Check if left mouse button had been pressed"""
            # If Mouse left bit equals 1
            if click[0] == 1:
                """If so, set clicked to True"""
                clicked = True  # Boolean

        return clicked  # Boolean

    """Save the results of the Game to CSV files"""

    def saveResults(self):
        """Creates name for file including the results (averages)"""
        fileraw = "CorsiBlockTapping_results.csv"  # Filename String
        """creates data frame of results (averages)"""
        df = pandas.DataFrame(self.results)  # DataFrame(Dictionairy<Header,Result>)
        """Opens the CSV file and store it as variable f"""
        f = open(fileraw, "a")  # File(String, append)
        """If the file is empty"""
        # If the read/write pointer position equals 0
        if f.tell() == 0:
            """Store the data including the headers"""
            df.to_csv(fileraw,  # Filename String
                      sep=',',  # Saperator String
                      encoding='utf-8',  # Encoding String
                      index=False,  # Index Boolean
                      mode='a')  # Mode append
        else:
            """Else: store the data without the headers"""
            df.to_csv(fileraw,  # Filename String
                      sep=',',  # Saperator String
                      encoding='utf-8',  # Encoding String
                      index=False,  # Index Boolean
                      header=False,  # Header Boolean
                      mode='a')  # Mode append
        """"Close file"""
        f.close()

        """Creates name for file including the raw_results"""
        fileraw = "CorsiBlockTapping_raw.csv"  # Filename String
        """Creates data frame of raw_results"""
        df = pandas.DataFrame(self.resultsRaw)  # DataFrame(Dictionairy<Header,Result>)
        """Opens the CSV file and store it as variable f"""
        f = open(fileraw, "a")  # File(String, append)
        """If the file is empty"""
        # If the read/write pointer position equals 0
        if f.tell() == 0:
            """Store the data including the headers"""
            df.to_csv(fileraw,  # Filename String
                      sep=',',  # Separator String
                      encoding='utf-8',  # Encoding String
                      index=False,  # Index Boolean
                      mode='a')  # Mode append
        else:
            """Else: store the data without the headers"""
            df.to_csv(fileraw,  # Filename String
                      sep=',',  # Separator String
                      encoding='utf-8',  # Encoding String
                      index=False,  # Index Boolean
                      header=False,  # Header Boolean
                      mode='a')  # Mode append
            """"Close file"""
        f.close()

    """"Checks if input is given by the participant, before starting experiment"""

    def checkInputCompleted(self):
        """If the input in box Input ID contains only letters"""
        if self.inputID.getValue().isalpha():  # Boolean
            """Set global variable initials to the input given by participant"""
            self.initials = self.inputID.getValue()  # String
        """If the input in box Input Age contains only digits"""
        if self.inputAge.getValue().isdigit():  # Boolean
            """Set global variable age to the input given by participant"""
            self.age = int(self.inputAge.getValue())  # Int
        """If the input in box Input gender is f"""
        if self.inputGender.getValue().lower() == 'f':  # Boolean
            """Set global variable gender to female"""
            self.gender = "female"  # String
        """If the input in box Input Gender is m"""
        if self.inputGender.getValue().lower() == 'm':  # Boolean
            """Set global varialbe gender to male"""
            self.gender = "male"  # String

        """If all inputs are according their requirements, so only letters, digits or f/m, 
        then this will return true, otherwise false"""
        return self.initials is not None and self.age != 0 and self.gender is not None  # Boolean

    """Main game loop to handle game logic"""

    def gameLoop(self):
        """Set STATE to welcome"""
        STATE = "welcome"  # String

        """ Set CURRENT_SEQUENCELENGTH to 2"""
        CURRENT_SEQUENCELENGTH = 2  # Int

        """Start main game loop"""
        while True:

            """Clean screen from previous loop"""
            self.view.refreshSurface()

            """Get event list from pygame and do for every event in list:"""
            for event in pygame.event.get():

                """Transitionals"""

                """If in welcome state"""
                if STATE == "welcome":  # String
                    """If start trial button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),  # Y Coordinate
                                           150,  # Width
                                           75):  # Heigth
                        """Set STATE to trial"""
                        STATE = "Questions"  # String

                        """Go to next event in event list"""
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),  # Y Coordinate
                                           150,  # Width
                                           75):  # Heigth
                        """Set STATE to quit"""
                        STATE = "quit"  # String

                        """Go to next event in event list"""
                        continue

                """If Questions state"""
                if STATE == "Questions":
                    """For every box in inputboxes do:"""
                    # For every InputBox in List<InputBox>
                    for box in self.input_boxes:
                        """Handle the event for this box, so provide when clicked to light up, 
                        or when backspace delete character and when keypress add character"""
                        box.handle_event(event)  # (Event)
                        """"Store the returned boolean. If input is according requirements: yes or no"""
                        spaceready = self.checkInputCompleted()  # Boolean

                    """If button is pressed and the input is according requirements"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                                           150,  # Width \ Height
                                           75) \
                            and spaceready:  # Boolean
                        """Initialize new trial with CURRENT_SEQUENCELENGTH"""
                        self.initializeTrial(CURRENT_SEQUENCELENGTH)  # (Int)

                        """Set starttime of experiment to current time"""
                        self.startTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')  # Datetime

                        """"Set starttime of current trial to current time"""
                        self.time_start = time()  # Float

                        """Set STATE to trial"""
                        STATE = "trial"  # String
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                                           150,  # Width
                                           75):  # Heigth
                        """Set STATE to quit"""
                        STATE = "quit"  # String

                        """Go to next event in event list"""
                        continue

                """If in trial state"""
                if STATE == "trial":
                    """If left mouse button is pressed"""
                    # If Mouse left bit equals 1
                    if pygame.mouse.get_pressed()[0] == 1:
                        """Get tile that has been clicked from Board.py"""
                        clickedRect = self.board.checkMouseClick(pygame.mouse.get_pos())  # Rect ((Mouse X, Mouse Y))
                        """If a tile has been clicked"""
                        if clickedRect is not None:
                            """If clicked tile was supposed to be clicked"""
                            # If Rect X, Rect Y equals current(Tile X, Tile Y) from List<(Tile X, Tile Y)>
                            if (clickedRect.left, clickedRect.top) == self.sequence[len(self.clickedseq)]:
                                """Add tile to clickedseq list"""
                                self.clickedseq.append((clickedRect.left, clickedRect.top))  # (Rect X, Rect Y)

                                """If clicked tile was not supposed to be clicked"""
                            elif (clickedRect.left, clickedRect.top) in self.clickedseq:
                                pass
                            else:
                                """Calculate time used to complete this trial"""
                                self.time_trial = time() - self.time_start  # Float

                                """Add time to list of trial times"""
                                self.times.append(self.time_trial)  # Float

                                """Add Initials, Age, Gender, Start time, Seq len, trial time and completed=False 
                                as dictonary to list ResultsRaw"""
                                self.resultsRaw.append({
                                    'Initials': self.initials,  # String
                                    'Age': self.age,  # Int
                                    'Gender': self.gender,  # String
                                    'Start time': self.startTime,  # Datetime
                                    'Seq len': CURRENT_SEQUENCELENGTH,  # Int
                                    'Trial time': self.time_trial,  # Float
                                    'Completed': False  # Boolean
                                })

                                """Add 1 to amount of errors made"""
                                self.player_errors += 1  # Int

                                """Set STATE to feedback"""
                                STATE = "feedback"  # String

                                """Go to next event in event list"""
                                continue

                        """If the sequence that has been clicked is the same as the trial sequence"""
                        # If List<(Tile X, Tile Y)> equals List<(Tile X, Tile Y)>
                        if self.clickedseq == self.sequence:
                            """Set correct_seq to True to indicate the player had entered the correct sequence"""
                            self.correct_seq = True  # Boolean

                            """Calculate time used to complete this trial"""
                            self.time_trial = time() - self.time_start  # Float

                            """Add time to list of trial times"""
                            self.times.append(self.time_trial)

                            """Add Initials, Age, Gender, Start time, Seq len, trial time and completed=True 
                            as dictonary to list ResultsRaw"""
                            self.resultsRaw.append({
                                'Initials': self.initials,  # String
                                'Age': self.age,  # Int
                                'Gender': self.gender,  # String
                                'Start time': self.startTime,  # Datetime
                                'Seq len': CURRENT_SEQUENCELENGTH,  # Int
                                'Trial time': self.time_trial,  # Float
                                'Completed': True  # Boolean
                            })

                            """Increase CURRENT_SEQUENCELENGTH by one for the next trial"""
                            CURRENT_SEQUENCELENGTH += 1  # Int

                            """Reset amount of player errors for the next trial"""
                            self.player_errors = 0  # Int

                            """Set STATE to feedback"""
                            STATE = "feedback"  # String

                            """Go to the next event in event list"""
                            continue

                """If in feedback state"""
                if STATE == "feedback":
                    """If next trial button is pressed and player has not made more than one error"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                                           150,  # Width \ Heigth
                                           75) \
                            and self.player_errors <= self.ALLOWED_ERRORS:  # Int < Int

                        """If not all trials have been completed"""
                        if CURRENT_SEQUENCELENGTH <= self.SEQUENCE_LENGTH:  # Int < Int
                            """Initialize new trial with CURRENT_SEQUENCELENGTH"""
                            self.initializeTrial(CURRENT_SEQUENCELENGTH)  # (Int)

                            """Set starttime of current trial to current time"""
                            self.time_start = time()  # Float

                            """Set STATE to trial"""
                            STATE = "trial"  # String

                            """Go to the next event in event list"""
                            continue

                            """If all trials have been completed"""
                        else:
                            """Set endtime of experiment to current time"""
                            self.endTime = datetime.datetime.now()  # Datetime

                            """Set STATE to final"""
                            STATE = "final"  # String

                            """Go to the next event in event list"""
                            continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if (self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),  # X Coordinate
                                            self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),  # Y Coordinate
                                            150,  # Width
                                            75)  # Heigth
                        and self.player_errors <= self.ALLOWED_ERRORS) \
                            or (self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (200 / 2),  # X Coordinate
                                                    self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),  # Y Coordinate
                                                    200,  # Width
                                                    100)  # Heigth
                                and self.player_errors > self.ALLOWED_ERRORS):
                        """Set endtime of experiment to current time"""
                        self.endTime = datetime.datetime.now()  # Datetime

                        """Set STATE to final"""
                        STATE = "final"  # String

                        """Go to the next event in event list"""
                        continue

                """If in result state"""
                if STATE == "results":
                    """If quit button is pressed"""
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 3 / 4 - (100 / 2),  # Y Coordinate
                                           200,  # Width
                                           100):  # Heigth
                        """State becomes final"""
                        STATE = "final"  # String

                        """Go to the next event in event list"""
                        continue

                """If in final state"""
                if STATE == "final":
                    """If results button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] / 2 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 3 / 5 - (100 / 2),  # Y Coordinate
                                           200,  # Width
                                           75):  # Heigth
                        """State becomes results"""
                        STATE = "results"

                        """Go to the next event in event list"""
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (150 / 2),  # X Coordinate
                                           self.SCREEN_SIZE[1] * 3 / 4 - (100 / 2),  # Y Coordinate
                                           200,  # Width
                                           100):  # Heigth
                        """Create panda dataframe of resultsRaw and store it in variable df"""
                        df = pandas.DataFrame(self.resultsRaw)  # DataFrame

                        """Check if all values in dataframe are completed"""
                        df = df[df.Completed != False]  # DataFrame

                        """Pick the largest completed sequence length, so that is the WMC of the participant"""
                        wmc = df['Seq len'].max()  # Int

                        """Calculate the average time of the trials and store it as avgtime"""
                        avgtime = df["Trial time"].mean()  # Float

                        """Add Initials, Age, Gender, Start time,End time, WMC and Average trial time 
                        as dictonary to list results (averages)"""
                        self.results.append({
                            'Initials': self.initials,  # String
                            'Age': self.age,  # Int
                            'Gender': self.gender,  # String
                            'Start time': self.startTime,  # Datetime
                            'End time': self.endTime,  # Datetime
                            'WMC': wmc,  # Int
                            'Avg trial time': avgtime  # Float
                        })

                        """Save the results of the Game to CSV file"""
                        self.saveResults()

                        """Set STATE to quit"""
                        STATE = "quit"  # String

                        """Go to the next event in event list"""
                        continue

                        """If exit system button is clicked"""
                    if event.type == pygame.QUIT:
                        """Set STATE to quit"""
                        STATE = "quit"  # String

                        """Go to the next event in event list"""
                        continue

            """End of for loop"""

            """Presentitionals"""

            """If in welcome state"""
            if STATE == "welcome":
                """Tell View.py to draw the welcome screen"""
                self.view.draw_welcome()

            """If in Questions state"""
            if STATE == "Questions":
                """Tell View.py to draw Question screen"""
                self.view.draw_question(self.input_boxes)  # (List<InputBox>)

            """If in trial state"""
            if STATE == "trial":
                """Tell View.py to draw the trial with current board from Board.py and clicked sequence"""
                self.view.draw_trial(self.board.getCopy(),  # (List<(Tile X, Tile Y)>
                                     self.clickedseq)  # List<(Tile X, Tile Y)>)

            """If in feedback state"""
            if STATE == "feedback":
                """Tell View.py to draw the feedback screen with trial time and if clicked sequence was correct"""
                self.view.draw_feedback(self.time_trial,  # float
                                        self.correct_seq,  # Boolean
                                        self.player_errors > self.ALLOWED_ERRORS)  # Boolean

            """If in final state"""
            if STATE == "final":
                """Tell View.py to draw the final screen with WMC and average trial time"""
                self.view.draw_final(pandas.DataFrame(self.resultsRaw))  # (DataFrame)
            """If in results state"""
            if STATE == "results":
                """Tell View.py to draw the results"""
                self.view.draw_results(pandas.DataFrame(self.resultsRaw))  # (DataFrame)

            """If in quite state"""
            if STATE == "quit":
                """Close screen"""
                pygame.display.quit()

                """Exit pygame"""
                pygame.quit()

                """Exit programm"""
                sys.exit()

            """Update pygame display"""
            self.view.updateDisplay()


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

    """Draws text"""

    def draw_text(self, text, div1, div2, small):
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
        self.draw_text("Your average completion time is " + str(resultsRaw['Trial time'].mean()) + " s",  # Text
                       2.0,  # Div1 X
                       2.5,  # Div2 Y
                       True)  # Small Boolean

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
                    pygame.Rect(tile[0], tile[1], TILE_SIZE[0],
                                TILE_SIZE[1]))  # Rect(Tile X, Tile Y, Tile Width, Tile Height)

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
        new_tile = pygame.Rect(tile[0] - 1, tile[1] - 1,  # Rect(Tile X - 1, Tile Y - 1,
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


""" Class to create and handle InputBoxes"""


class InputBox:

    def __init__(self, x,  # X Coordinate
                 y,  # Y Coordinate
                 w,  # Width
                 h,  # Heigth
                 text=''):  # Text

        """Initialize pygame"""
        pygame.init()

        """Initialise colors used for screen"""
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')  # Color(name)
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')  # Color(name)

        """Set fonts"""
        self.FONT = pygame.font.Font(None, 32)  # (object/filename, size)

        """Create InputBox rectangle"""
        self.rect = pygame.Rect(x, y, w, h)  # Rect(X, Y, Width, Height)

        """Set color"""
        self.color = self.COLOR_INACTIVE  # Color(name)

        """Set Text"""
        self.text = text  # Text

        """Create new Surface from Text"""
        self.txt_surface = self.FONT.render(text,  # Text
                                            True,  # Antialias
                                            self.color)  # Text color (R,G,B)

        """Set active to False"""
        self.active = False  # Boolean

    """Handles InputBox event"""

    def handle_event(self, event):  # Event
        """If mousebutton has been clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN:  # Boolean Event.Type = MouseButtonDown
            """ If the user clicked on the input box"""
            if self.rect.collidepoint(event.pos):  # Boolean(Mouse X, Mouse Y)
                """ Toggle the active variable """
                self.active = not self.active  # Boolean
                """If user has not clicked on the input box"""
            else:
                """Set active to False"""
                self.active = False  # Boolean

            """ Change the current color of the input box """
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE  # Color(name)

        """If a key has been pressed"""
        if event.type == pygame.KEYDOWN:  # Boolean Event.Type = KeyDown
            """if the InputBox has been selected"""
            if self.active:  # Boolean
                """If pressed key is BackSpace"""
                if event.key == pygame.K_BACKSPACE:  # Boolean Event.Key = BackSpace
                    """Remove one character from the text"""
                    self.text = self.text[:-1]  # Text
                    """If any other button has been pressed"""
                else:
                    """Add pressed key unicode to text"""
                    self.text += event.unicode  # Text

                """ Re-render the text """
                self.txt_surface = self.FONT.render(self.text,  # Text
                                                    True,  # Antialias
                                                    self.color)  # Text color (R,G,B)

    """Return the InputBox Text"""

    def getValue(self):
        return self.text  # Text

    """Update the InputBox"""

    def update(self):
        """ Resize the box if the text is too long. """
        width = max(200, self.txt_surface.get_width() + 10)  # Width
        self.rect.w = width  # Width


"""Init Game instance, automatically runs game"""
Game(SCREEN_SIZE,  # (Screen width, Screen Height)
     SEQUENCE_LENGTH,  # Max Sequence Length
     ALLOW_ERRORS),  # Max Allowed Errors
