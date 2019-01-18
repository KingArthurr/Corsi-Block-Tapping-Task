from Game import Game

""" Contains main function for starting the program."""

"""Set game settings"""
SCREEN_SIZE = (1000, 800)  # (Screen width, Screen Height)
SEQUENCE_LENGTH = 9  # Max Sequence Length
ALLOW_ERRORS = 1  # Max Allowed Errors

"""Init Game instance, automatically runs game"""
Game(SCREEN_SIZE,  # (Screen width, Screen Height)
     SEQUENCE_LENGTH,  # Max Sequence Length
     ALLOW_ERRORS),  # Max Allowed Errors
