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
    """Initialize game settings"""
    # TODO SET GAME PARAMETERS
    SCREEN_SIZE = (1000, 800)
    SEQUENCE_LENGTH = 9
    ALLOWED_ERRORS = 1

    TILE_SIZE = (min(SCREEN_SIZE) / SEQUENCE_LENGTH - 1,
                 min(SCREEN_SIZE) / SEQUENCE_LENGTH - 1)

    """Initialize global variables"""
    board = None
    correct_seq = None
    sequence = None
    clickedseq = None
    player_errors = 0
    WMC = None
    times = []
    time_trial = None
    time_start = None
    resultsRaw = []
    results = []

    initials = None
    age = 0
    gender = None

    startTime = None
    endTime = None

    # Setup input boxes TODO comment
    inputID = InputBox(SCREEN_SIZE[0] * 4 / 7, SCREEN_SIZE[1] * 7 / 40, 200, 32)
    inputAge = InputBox(SCREEN_SIZE[0] * 4 / 7, SCREEN_SIZE[1] * 11 / 40, 200, 32)
    inputGender = InputBox(SCREEN_SIZE[0] * 4 / 7, SCREEN_SIZE[1] * 15 / 40, 200, 32)
    input_boxes = [inputID, inputAge, inputGender]
    spaceready = False

    """Initialise Game()"""

    def __init__(self):
        """Create PyGame screen"""
        pygame.init()
        pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Corsi Block Tapping Task")
        screen = pygame.display.get_surface()

        """Initialise View.py to control the screen"""
        self.view = View(screen, self.SCREEN_SIZE, self.TILE_SIZE)

    """Initialize Trial of length of current sequence"""

    def initializeTrial(self, CURRENT_SEQUENCELENGTH):
        """"Clean clickedseq by assigning new clean list()"""
        self.clickedseq = list()

        """Clean board by creating new Board()"""
        self.board = Board(self.SCREEN_SIZE, self.SEQUENCE_LENGTH, self.TILE_SIZE)

        """Create a new sequence of length of current sequence"""
        self.createSequence(CURRENT_SEQUENCELENGTH)

        """Tell View.py to draw the trial and show the sequence"""
        self.view.draw_trial(self.board.getCopy(), self.clickedseq)
        self.view.draw_sequence(self.getSequence())

        """Set correct_seq to False to indicate player has not yet entered the correct sequence"""
        self.correct_seq = False

    """Create a sequence of length of given variable CURRENT_SEQUENCELENGTH"""

    def createSequence(self, CURRENT_SEQUENCELENGTH):
        """Get copy of the tiles in the board from Board.py"""
        tiles = self.board.getCopy()

        """Shuffle them to always select a random tile"""
        random.shuffle(tiles)

        """Clean sequence by assigning new clean list()"""
        self.sequence = list()

        """Add CURRENT_SEQUENCELENGTH amount of tiles from randomized tiles list to sequence"""
        for j in range(CURRENT_SEQUENCELENGTH):
            self.sequence.append(tiles[j])

    """Getter method that returns sequence list"""

    def getSequence(self):
        return self.sequence

    """Check if button on location (x,y) with width w and height h is pressed"""

    def button_pressed(self, x, y, w, h):
        """Create clicked boolean and set to False"""
        clicked = False

        """Get mouse pointer position and pressed mouse buttons"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        """Check if the mouse cursor is on the button"""
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            """Check if left mouse button had been pressed"""
            if click[0] == 1:
                """If so, set clicked to True"""
                clicked = True

        return clicked

    """Save the results of the Game to CSV file"""
    # TODO IMRPOVE
    def saveResults(self):
        fileraw = "CorsiBlockTapping_results.csv"
        df = pandas.DataFrame(self.results)
        f = open(fileraw, "a")
        if f.tell() == 0:
            df.to_csv(fileraw, sep='\t', encoding='utf-8', index=False, mode='a')
        else:
            df.to_csv(fileraw, sep='\t', encoding='utf-8', index=False, header=False, mode='a')
        f.close()

        fileraw = "CorsiBlockTapping_raw.csv"
        df = pandas.DataFrame(self.resultsRaw)
        f = open(fileraw, "a")
        if f.tell() == 0:
            df.to_csv(fileraw, sep='\t', encoding='utf-8', index=False, mode='a')
        else:
            df.to_csv(fileraw, sep='\t', encoding='utf-8', index=False, header=False, mode='a')
        f.close()

    def checkInputCompleted(self):  # TODO fix
        if self.inputID.getValue().isalpha():
            self.initials = self.inputID.getValue()
        if self.inputAge.getValue().isdigit():
            self.age = int(self.inputAge.getValue())
        if self.inputGender.getValue().lower() == 'f':
            self.gender = "female"
        if self.inputGender.getValue().lower() == 'm':
            self.gender = "male"

        # return True
        return self.initials is not None and self.age != 0 and self.gender is not None

    """Main game loop to handle game logic"""

    def gameLoop(self):
        """Set STATE to welcome"""
        STATE = "welcome"

        """ Set CURRENT_SEQUENCELENGTH to 2"""
        CURRENT_SEQUENCELENGTH = 2

        """Start main game loop"""
        while True:

            """Clean screen from previous loop"""
            self.view.refreshSurface()

            """Get event list from pygame and do for every event in list:"""
            for event in pygame.event.get():

                """Transitionals"""

                """If in welcome state"""
                if STATE == "welcome":
                    """If start trial button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),
                                           150, 75):
                        """Set STATE to trial"""
                        STATE = "Questions"

                        """Go to next event in event list"""
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 3 / 5 - (75 / 2),
                                           150, 75):
                        """Set STATE to quit"""
                        STATE = "quit"

                        """Go to next event in event list"""
                        continue

                if STATE == "Questions":  # TODO fix & comment
                    for box in self.input_boxes:
                        box.handle_event(event)
                        spaceready = self.checkInputCompleted()

                    # is the spacebar pressed?
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                                           150, 75) \
                            and spaceready:
                        """Initialize new trial with CURRENT_SEQUENCELENGTH"""
                        self.initializeTrial(CURRENT_SEQUENCELENGTH)

                        """Set starttime of experiment to current time"""
                        self.startTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                        """Set starttime of current trial to current time"""
                        self.time_start = time()
                        STATE = "trial"
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                                           150, 75):
                        """Set STATE to quit"""
                        STATE = "quit"

                        """Go to next event in event list"""
                        continue

                """If in trial state"""
                if STATE == "trial":
                    """If left mouse button is pressed"""
                    if pygame.mouse.get_pressed()[0] == 1:
                        """Get tile that has been clicked from Board.py"""
                        clickedRect = self.board.checkMouseClick(pygame.mouse.get_pos())

                        """If a tile has been clicked"""
                        if clickedRect is not None:
                            """If clicked tile was supposed to be clicked"""
                            if (clickedRect.left, clickedRect.top) == self.sequence[len(self.clickedseq)]:
                                """Add tile to clickedseq list"""
                                self.clickedseq.append((clickedRect.left, clickedRect.top))

                                """If clicked tile was not supposed to be clicked"""
                            else:
                                """Calculate time used to complete this trial"""
                                self.time_trial = time() - self.time_start

                                """Add time to list of trial times"""
                                self.times.append(self.time_trial)

                                """Add 2-tuple of WMC and trial time to seqLength_Times_List"""  # TODO commenting
                                self.resultsRaw.append({
                                    'Initials': self.initials,
                                    'Age': self.age,
                                    'Gender': self.gender,
                                    'Start time': self.startTime,
                                    'Seq len': CURRENT_SEQUENCELENGTH,
                                    'Trial time': self.time_trial,
                                    'Completed': False
                                })

                                """Add 1 to amount of errors made"""
                                self.player_errors += 1

                                """Set STATE to feedback"""
                                STATE = "feedback"

                                """Go to next event in event list"""
                                continue

                    """If the sequence that has been clicked is the same as the trial sequence"""
                    if self.clickedseq == self.sequence:
                        """Set correct_seq to True to indicate the player had entered the correct sequence"""
                        self.correct_seq = True

                        """Calculate time used to complete this trial"""
                        self.time_trial = time() - self.time_start

                        """Add time to list of trial times"""
                        self.times.append(self.time_trial)

                        """Add 2-tuple of WMC and trial time to seqLength_Times_List"""  # TODO commenting
                        self.resultsRaw.append({
                            'Initials': self.initials,
                            'Age': self.age,
                            'Gender': self.gender,
                            'Start time': self.startTime,
                            'Seq len': CURRENT_SEQUENCELENGTH,
                            'Trial time': self.time_trial,
                            'Completed': True
                        })

                        """Increase CURRENT_SEQUENCELENGTH by one for the next trial"""
                        CURRENT_SEQUENCELENGTH += 1

                        """Reset amount of player errors for the next trial"""
                        self.player_errors = 0

                        """Set STATE to feedback"""
                        STATE = "feedback"

                        """Go to the next event in event list"""
                        continue

                """If in feedback state"""
                if STATE == "feedback":
                    """If next trial button is pressed and player has not made more than one error"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 3 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                                           150, 75) \
                            and self.player_errors <= self.ALLOWED_ERRORS:

                        """If not all trials have been completed"""
                        if CURRENT_SEQUENCELENGTH <= self.SEQUENCE_LENGTH:
                            """Initialize new trial with CURRENT_SEQUENCELENGTH"""
                            self.initializeTrial(CURRENT_SEQUENCELENGTH)

                            """Set starttime of current trial to current time"""
                            self.time_start = time()

                            """Set STATE to trial"""
                            STATE = "trial"

                            """Go to the next event in event list"""
                            continue

                            """If all trials have been completed"""
                        else:
                            """Set endtime of experiment to current time"""
                            self.endTime = datetime.datetime.now()

                            """Set STATE to final"""
                            STATE = "final"

                            """Go to the next event in event list"""
                            continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if (self.button_pressed(self.SCREEN_SIZE[0] * 2 / 3 - (150 / 2),
                                            self.SCREEN_SIZE[1] * 4 / 5 - (75 / 2),
                                            150, 75)
                        and self.player_errors <= self.ALLOWED_ERRORS) \
                            or (self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (200 / 2),
                                                    self.SCREEN_SIZE[1] * 4 / 5 - (100 / 2),
                                                    200, 100)
                                and self.player_errors > self.ALLOWED_ERRORS):
                        """Set endtime of experiment to current time"""
                        self.endTime = datetime.datetime.now()

                        """Set STATE to final"""
                        STATE = "final"

                        """Go to the next event in event list"""
                        continue


                """If in result state"""
                if STATE == "results":
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 3 / 4 - (100 / 2),
                                           200, 100):
                        STATE = "final"
                    continue

                """If in final state"""
                if STATE == "final":
                    """If results button is pressed"""
                    if self.button_pressed(self.SCREEN_SIZE[0] / 2 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 3 / 5 - (100 / 2),
                                           200, 75, ):
                        STATE = "results"
                        continue

                    """If quit button is pressed"""
                    # FIXME BUTTON POSITIONS HARDCODED, ALSO ADD CHANGES IN View.py
                    if self.button_pressed(self.SCREEN_SIZE[0] * 1 / 2 - (150 / 2),
                                           self.SCREEN_SIZE[1] * 3 / 4 - (100 / 2),
                                           200, 100):
                        """"""  # TODO commenting
                        df = pandas.DataFrame(self.resultsRaw)
                        df = df[df.Completed != False]
                        wmc = df['Seq len'].max()
                        avgtime = df["Trial time"].mean()
                        self.results.append({
                            'Initials': self.initials,
                            'Age': self.age,
                            'Gender': self.gender,
                            'Start time': self.startTime,
                            'End time': self.endTime,
                            'WMC': wmc,
                            'Avg trial time': avgtime
                        })

                        """Save the results of the Game to CSV file"""
                        self.saveResults()

                        """Set STATE to quit"""
                        STATE = "quit"

                        """Go to the next event in event list"""
                        continue

                """If exit system button is clicked"""
                if event.type == pygame.QUIT:
                    """Set STATE to quit"""
                    STATE = "quit"

                    """Go to the next event in event list"""
                    continue

            """End of for loop"""

            """Presentitionals"""

            """If in welcome state"""
            if STATE == "welcome":
                """Tell View.py to draw the welcome screen"""
                self.view.draw_welcome()

            if STATE == "Questions":  # TODO fix
                # draw the welcome message (scroll down for the function)
                self.view.draw_question(self.input_boxes, self.spaceready)

            """If in trial state"""
            if STATE == "trial":
                """Tell View.py to draw the trial with current board from Board.py and clicked sequence"""
                self.view.draw_trial(self.board.getCopy(), self.clickedseq)

            """If in feedback state"""
            if STATE == "feedback":
                """Tell View.py to draw the feedback screen with trial time and if clicked sequence was correct"""
                self.view.draw_feedback(self.time_trial, self.correct_seq, self.player_errors > self.ALLOWED_ERRORS)

            """If in final state"""
            if STATE == "final":
                """Tell View.py to draw the final screen with WMC and average trial time"""
                self.view.draw_final(pandas.DataFrame(self.resultsRaw))

            """"""  # TODO comment
            if STATE == "results":
                self.view.draw_results(pandas.DataFrame(self.resultsRaw))

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
