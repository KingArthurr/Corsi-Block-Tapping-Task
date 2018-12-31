import pygame
import sys
from time import time
import random
from pygame.locals import *
from pygame.compat import unichr_, unicode_

from View import View
from Board import Board

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
    correct_seq = None
    sequence = None
    clickedseq = None
    player_errors = 0
    WMC = None
    times = [1]
    time_trial = None
    time_start = None

    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Corsi Block Tapping Task")

    screen = pygame.display.get_surface()
    view = View(screen, SCREEN_SIZE, TILE_SIZE);

    def initializeGame(self, CURRENT_SEQUENCELENGTH):
        self.clickedseq = list()
        self.player_errors = 0
        self.board = Board(self.BOARD_SIZE, self.SEQUENCE_LENGTH, self.TILE_SIZE);
        self.createSequence(CURRENT_SEQUENCELENGTH)  
        self.view.draw_trial(self.board.getCopy(), self.clickedseq)
        self.view.draw_sequence(self.getSequence())
        self.correct_seq = False

    def createSequence(self, CURRENT_SEQUENCELENGTH):
        i = CURRENT_SEQUENCELENGTH;
        tiles = self.board.getCopy();

        random.shuffle(tiles);

        self.sequence = list()

        for j in range(i):
            self.sequence.append(tiles[j])

    def getSequence(self):
        return self.sequence

    def gameLoop(self):
        STATE = "welcome"
        CURRENT_SEQUENCELENGTH = 2
        while(True):

            self.view.refreshSurface();

            for event in pygame.event.get():

                # interactive transitionals
                if STATE == "welcome":
                    if event.type == KEYDOWN and event.key == K_SPACE:

                        self.initializeGame(CURRENT_SEQUENCELENGTH)
                        self.time_start = time()
                        STATE = "trial"
                        continue

                if STATE == "trial":
                    
                    if pygame.mouse.get_pressed() == (1,0,0):
                        mouse_loc = pygame.mouse.get_pos()
                        clickedRect = self.board.checkMouseClick(mouse_loc)
                        if clickedRect != None:
                            if (clickedRect.left, clickedRect.top) == self.sequence[len(self.clickedseq)]:
                                self.clickedseq.append((clickedRect.left, clickedRect.top))
                            else:
                                print('youremoron')
                                self.player_errors += 1
                                if self.player_errors > 1:
                                    STATE = "feedback"
                    if self.clickedseq == self.sequence:
                            print("You DID IT HOMIE")
                            self.correct_seq = True
                            CURRENT_SEQUENCELENGTH += 1
                            self.time_trial = time() - self.time_start
                            STATE = "feedback"
        
                    
                        
                if STATE == "feedback":
                    if event.type == KEYDOWN and event.key == K_SPACE:#TODO change to button
                        if CURRENT_SEQUENCELENGTH <= self.SEQUENCE_LENGTH:
                            self.initializeGame(CURRENT_SEQUENCELENGTH)
                            self.time_start = time()
                            STATE = "trial"
                        else: 
                            STATE = "final"
                        continue
                if STATE == "final":
                     if event.type == KEYDOWN and event.key == K_SPACE:#TODO change to button
                        STATE = "quit"
                if event.type == QUIT:
                    STATE = "quit"
                    break

                # Presentitionals
            if STATE == "welcome":
                self.view.draw_welcome()

            if STATE == "trial":
                self.view.draw_trial(self.board.getCopy(), self.clickedseq)
            
            if STATE == "feedback":
                self.view.draw_feedback(self.time_trial, self.correct_seq)


            if STATE == "final":
                self.view.draw_final(self.WMC, sum(self.times)/len(self.times))

            if STATE == "quit":
                pygame.quit()
                sys.exit()





            self.view.updateDisplay();

