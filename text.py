import pygame as pg

pg.init()


class Text:

    def __init__(self):
        pass

    @staticmethod
    def draw_text(screen, text, x, y, font_size):
        """
        Will draw text onto the screen
        :param screen: the screen that the text needs to be drawn on
        :param text: the text you want to be drawn onto the screen
        :param x: the x co-ordinate of where you want the text drawn
        :param y: the y co-ordinate of where you want the text drawn
        :param font_size: the font size of the the text you want drawn
        """

        font = pg.font.SysFont('Courier', font_size)

        screen.blit(font.render(text, True, (255, 255, 255)), (x, y))

    @staticmethod
    def draw_2048(screen, x, y, font_size, colour, secondColour):
        """
        Will draw a decorative 2048 on the menu screen
        """

        text = str(2048)

        font = pg.font.SysFont('rockwell', font_size)

        screen.blit(font.render(text, True, colour), (x, y))
        screen.blit(font.render(text, True, secondColour), (x - 5, y - 5))

    def draw_win(self, screen):
        """
        draws YOU WIN onto the screen
        """

        text = "YOU WIN"
        x = 280  # x pos of the text
        y = 180  # y pos of the text
        font_size = 100
        self.draw_text(screen, text, x, y, font_size)

    def draw_lose(self, screen):
        """
        draws YOU LOSE onto the screen
        """

        text = "YOU LOSE"
        x = 270  # x pos of the text
        y = 180  # y pos of the text
        font_size = 100
        self.draw_text(screen, text, x, y, font_size)

    def draw_score(self, screen, score):
        """
        draws your SCORE onto the screen
        """

        text = "Your score was: " + str(score)
        x = 200  # x pos of the text
        y = 300  # y pos of the text
        font_size = 50
        self.draw_text(screen, text, x, y, font_size)
