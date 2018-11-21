import pygame
import sys
from time import time
import random
from pygame.locals import *
from pygame.compat import unichr_, unicode_

from View import View
from Board import Board
from Player import Player
from Util import Util


''' This class is takes care of all the game logic and will be used as the Controller.  '''

class Game:

    ''' init Board + Player
        Start view
        Play game (while loop)
        Communication between View and Model

        Sequence randomizer (could be in Util) '''

    SCREEN_SIZE = (1000, 800)
    BOARD_SIZE = (1000, 700)
    TILE_SIZE = (99, 99)
    SEQUENCE_LENGTH = 9

    board = None
    player = None

    sequence = None

    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Corsi Block Tapping Task")

    screen = pygame.display.get_surface()
    view = View(screen, SCREEN_SIZE, TILE_SIZE);

    def initializeGame(self):
        self.board = Board(self.BOARD_SIZE, self.SEQUENCE_LENGTH, self.TILE_SIZE);
        self.player = Player();

    def createSequence(self, CURRENT_SEQUENCELENGTH):
        i = CURRENT_SEQUENCELENGTH + 1;
        tiles = self.board.getCopy();

        random.shuffle(tiles);

        self.sequence = list()

        for j in range(i):
            self.sequence.append(tiles[j])

    def getSequence(self):
        return self.sequence

    def gameLoop(self):
        STATE = "welcome"
        while(True):

            self.view.refreshSurface();





            for event in pygame.event.get():

                # interactive transitionals
                if STATE == "welcome":
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.initializeGame()
                        self.createSequence(CURRENT_SEQUENCELENGTH=1) #TODO unhardcode
                        STATE = "trial"
                        continue

                if STATE == "trial":
                    if event.type == KEYDOWN and event.key == K_SPACE: #TODO change to button

                        #TODO remove placeholder
                        self.initializeGame()
                        self.createSequence(CURRENT_SEQUENCELENGTH=1)  # TODO unhardcode


                        STATE = "trial"
                        continue

                if event.type == QUIT:
                    STATE = "quit"
                    break

                # Presentitionals
            if STATE == "welcome":
                self.view.draw_welcome()


            if STATE == "trial":
                self.view.draw_trial(self.board.getCopy(), self.getSequence())

            if STATE == "quit":
                pygame.quit()
                sys.exit()





            self.view.updateDisplay();

