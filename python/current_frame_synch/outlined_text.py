import pygame

# thanks to PoDuck (Timm Simpkins) for this: 
# https://github.com/PoDuck/pygame_outlined_text

class OutlinedText(object):
    def __init__(
            self,
            text,
            outline_width,
            font,
            foreground_color=(255, 255, 255),
            background_color=(0, 0, 0)
    ):
        """
        Outline text for pygame.
        :param text: bytes or unicode text
        :param outline_width: outline width in pixels
        :param foreground_color: foreground color of text defaults to white
        :param background_color: background color of text defaults to black
        """
        self.text = text
        self.foreground = foreground_color
        self.background = background_color
        self.outline_width = outline_width
        self.font = font
        self.text_surface = self.font.render(self.text, False, self.foreground)        
        self.text_outline_surface = self.font.render(self.text, False, self.background)

        # There is no good way to get an outline with pygame, so we draw
        # the text at 8 points around the main text to simulate an outline.
        self.directions = [
            (self.outline_width, self.outline_width),
            (0, self.outline_width),
            (-self.outline_width, self.outline_width),
            (self.outline_width, 0),
            (-self.outline_width, 0),
            (self.outline_width, -self.outline_width),
            (0, -self.outline_width),
            (-self.outline_width, -self.outline_width)
        ]

    def get_width(self):
        """
        Get width of text including border.
        :return: width of text, including border.
        """
        return self.text_surface.get_width() + self.outline_width * 2

    def change_text(self, text):
        """
        Changes text to "text"
        :param text: New text
        """
        self.text = text
        self._update_text()

    def change_foreground_color(self, color):
        """
        Changes foreground color
        :param color: New foreground color
        """
        self.foreground = color
        self._update_text()

    def change_outline_color(self, color):
        """
        Changes the outline color
        :param color: New outline color
        """
        self.background = color
        self._update_text()

    def _update_text(self):
        """
        "protected" function to replace the text surface with a new one based on updated values.
        """
        self.text_surface = self.font.render(self.text, False, self.foreground)
        self.text_outline_surface = self.font.render(self.text, False, self.background)

    def render(self, text):
        self.change_text(text)

        # create a surface that will contain the outlined text
        surface = pygame.Surface((self.text_outline_surface.get_width() + self.outline_width * 2,
                                  self.text_outline_surface.get_height() + self.outline_width * 2))
        # blit outline images to screen
        for direction in self.directions:
            surface.blit(
                self.text_outline_surface,
                (
                    self.outline_width - direction[0],
                    self.outline_width - direction[1]
                )
            )
        
        # blit foreground image to the screen
        surface.blit(self.text_surface, (self.outline_width, self.outline_width))

        return surface