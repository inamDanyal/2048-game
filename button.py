import pygame as pg

pg.init()  # Initialising pygame

WHITE = (255, 255, 255)  # Default colour of the button
GRAY = (200, 200, 200)  # Default colour of the shadow


class Button:

    def __init__(self, screen, width: int, height: int, x: int, y: int, fontSize: int):
        """
        Initalises the button class
        :param screen: the screen
        :param width: the width of the button
        :param height: the height of the button
        """

        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.x_boundary = width
        self.y_boundary = height
        self.font = pg.font.SysFont('rockwell', fontSize)

    def draw_button(self, text: str, text_colour: tuple, highlighted_colour: tuple, shadow_colour: tuple):
        """
        Draws the buttons onto the screen
        :param text: the text that will go onto the button
        :param text_colour: the colour of the text
        :param highlighted_colour: the colour of the button when the mouse hovers over it
        :param shadow_colour: the colour of the buttons shadow
        :return: a functional button
        """

        rect = pg.Rect(self.x, self.y, self.width, self.height)
        shadow = pg.Rect(self.x + 10, self.y + 10, self.width, self.height)

        # Drawing the shadow first
        pg.draw.rect(self.screen, GRAY, shadow)

        # Drawing the actual button on top of the shadow
        pg.draw.rect(self.screen, WHITE, rect)

        # bliting the text onto the buttons
        self.screen.blit(self.font.render(text, True, text_colour), (self.x + 40, self.y + 20))

        mouse = pg.mouse.get_pos()  # Gets the position of the mouse

        # if the mouse hovers over the button it will slightly enlarge and change colours
        # Enlarges the text, shadow, and the button itself
        if self.x + self.x_boundary > mouse[0] > self.x and self.y + self.y_boundary > mouse[1] > self.y:
            pg.draw.rect(self.screen, shadow_colour, (self.x+10, self.y+10, self.width * 1.1, self.height * 1.1))
            pg.draw.rect(self.screen, highlighted_colour, (self.x, self.y, self.width * 1.1, self.height * 1.1))
            self.screen.blit(self.font.render(text, True, WHITE), (self.x+40 * 1.1, self.y+20 * 1.1))

    def check_clicked(self):
        """
        Will check if the buttons are clicked and if they are, it will return True
        :return: will return True
        """

        mouse = pg.mouse.get_pos()  # Gets the mouse position
        click = pg.mouse.get_pressed()  # Checks if the mouse is clicked

        if self.x + self.x_boundary > mouse[0] > self.x and self.y + self.y_boundary > mouse[1] > self.y:
            if click[0] == 1:
                return True

    def function(self, action=None):
        """
        Will check if the buttons are clicked and if they are, it will start the respective loop
        :param action: The loop that will start upon clicking the button
        :return: Will start a new loop
        """

        if self.check_clicked():
            action()

class InputBox:

    def __init__(self, x: int, y: int, width :int, height:int, text='') -> None:
        """
        Initialises the inputbox class
        :param x: the x coordinate of the input box
        :param y: the y coodinate of the input box
        :param width: the width of the input box
        :param height: the height of the input box
        :param text: the text that will be entered into the box
        """

        self.width = width
        self.height = height

        self.inactiveColour = (255, 255, 255)
        self.activeColour = (100, 100, 100)

        self.rect = pg.Rect(x, y, width, height)
        self.colour = self.inactiveColour
        self.text = text
        self.textSurface = pg.font.Font.render(text, True, self.colour)
        self.active = False
    
    def toggle(self, event, action=None):
        """
        Toggles the button and allows you to enter text into it
        :param event: checks for key events 
        :param action: the function that needs to be triggered
        """
        
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pos()

        # If there is a click inside of thebounds of the input box then select the box
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            if click[0] == 1:
                self.active = True
        
        # If there is a click outside of the bounds of the input box then unselect the box
        if self.x + self.width < mouse[0] < self.x and self.y + self.height < mouse[1] < self.y:
            if click[0] == 1:
                self.active = False
        
        # If the box is selected then change the colour
        if self.active:
            self.colour = self.activeColour
            
            # If a key is pressed
            if event.type == pg.KEYDOWN:
                
                # If enter is pressed then run the function
                if event.key == pg.K_RETURN:
                    action()
                
                # If the backspace key is pressed then slice off the last character of the string
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                
                # If any other key is pressed
                else:
                    # Then add the characters onto the end of the string
                    self.text += event.unicode
                    
                    # Update the rendering of the box
                    self.textSurface = pg.font.Font.render(self.text, True, self.colour)
    
    def update(self):
        """
        Resize the box if the input text is too long
        :return: None
        """
        width = max(200, self.textSurface.get_width()+10)
        self.rect.w = width
    
    def draw(self, screen):
        """
        Will blit the rect and the text onto the screen 
        :return: None
        """
        # Blit the Rect onto the screen
        pg.draw.rect(screen, self.colour, self.rect, 2)

        # Blit the text onto the screen
        screen.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
