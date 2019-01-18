import pygame

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
