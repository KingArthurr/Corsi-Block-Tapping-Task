import datetime
import random
import sys
from time import time

import pandas
import pygame

from Board import Board
from InputBox import InputBox
from View import View

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
