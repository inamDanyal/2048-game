import random
import pygame as pg
from position import Position
from vector import Vector
from squares import Square
from text import Text
import copy

"""
random : random is used for the probabilities of the square spawns, 90% for a tile value of 2 and 10% for a value of 4
pygame : pygame is used to render the game 
Position : Position is used to track the positions of the squares as well help with the colisions and movements
Vector : Vector is used to turn a tuple into a Vector it is used to make the tiles move by the vector of the coverted tuple
Square : Square is used to create the squares as well as move the squares 
WinLose : WinLose is used when you win or lose the game, if you win it will display the You Win screen and if you lose it will display the You Lose screen
Text : Text is used to render text onto the screen, like the score and the square values
copy : Used to create copies of the 2D arrays in order to allow previous move functionality
"""

"""
The GameBoard class is where all of the game logic is held, this where the game-board itself is stored and worked on.

In this class all of the movement of the blocks is carried out and all of the back end computation of the game is done 
this class doesn't contain any pygame as it would interfere with the AI.

This class doesn't inherit anything
"""


class GameBoard:

    def __init__(self):

        # This is the current board, will get updated per move to match the current game state
        # Starts the same as the defaultBoard
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [2, 2, 0, 0]]

        # Default board, this is the board that every game should start with
        self.defaultBoard = [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [2, 2, 0, 0]]

        # Empty board, this board will be used to reset the previous board whenever the game is reset
        # And will be how the previousBoard is initialised
        self.emptyBoard = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

        # Making the previous board a copy of the empty board at the start of the game
        self.previousBoard = copy.deepcopy(self.emptyBoard)

        # Stack of previous boards, will be used to undo moves
        # Not yet implemented
        self.previousBoards = []

        # Amount of rows and columns
        self.boardSize = 4
        self.rows = range(self.boardSize)
        self.columns = range(self.boardSize)

        # Representation of the board
        self.objects = []
        self.previousObjects = []
        self.tempObjects = []

        # Convert the board to array of objects
        self.convert_board_to_objects()

        # Tracks the score
        self.previousScore = 0
        self.currentScore = 0
        self.temp = 0

        # Is True when the player has made a move, used to check the game state
        self.hasMoved = False

    def changeBoardSize(self):
        """
        Changes the size of the arrays depending on the board size
        :return:
        """

        # If the board size is 5x5 then it will add another row and column
        if self.boardSize == 5:

            self.board = [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [2, 2, 0, 0, 0],
                          [0, 0, 0, 0, 0]]

            self.defaultBoard = [[0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [2, 2, 0, 0, 0],
                                 [0, 0, 0, 0, 0]]

            self.previousBoard = [[0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0]]
            
            # Resets the border size for the squares that are already on the board
            for square in self.objects:
                square.border = 5

        # If the board size is 6x6 then it will add two more rows and columns
        if self.boardSize == 6:

            self.board = [[0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [2, 2, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0]]

            self.defaultBoard = [[0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0],
                                 [2, 2, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0]]

            self.previousBoard = [[0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [2, 2, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0]]
            
            # Resets the border size for the squares that are already on the board
            for square in self.objects:
                square.border = 6

    def convert_board_to_objects(self):
        """
        loops through the 2D array board and for any spaces that are not 0 it will add a square with the
        corresponding number to the board
        :return: none
        """

        for row in self.rows:
            for column in self.columns:

                number = self.defaultBoard[row][column]

                if number != 0:
                    self.add(Square(number, (row, column), self.boardSize))

    def add(self, square: Square):
        """
        Add a square to the board
        :param square: Instance of the square
        :return:
        """

        self.objects.append(square)

    def get(self, position: Position) -> Square | None:
        """
        Used to get a square at a position
        :param position: Position of the square
        :return: The square instance
        """
        for square in self.objects:

            if position.compare(square):
                return square

        return

    def get_all(self, position: Position) -> list:
        """
        Used to get all the objects at this position
        :param position: Position of the objects
        :return: List of objects
        """

        temp = []

        for square in self.objects:

            if position.compare(square):
                temp.append(square)

        return temp

    def get_empty_spaces(self) -> list:
        """
        Loop through the board to find an empty spaces
        :return: List of positions where there is empty space
        """
        empty_spaces = []

        for y in self.columns:
            for x in self.rows:

                square = self.get(Position((x, y)))

                # If the square is None
                if square is None:
                    coords = (x, y)
                    empty_spaces.append(Position(coords))

        random.shuffle(empty_spaces)
        return empty_spaces

    def check_location(self, square: Square, vector: Vector, squares_to_ignore: list, squares_to_add: list):
        """
        If there is two squares at the location reverse the other square
        Continue to reverse all squares
        :param squares_to_ignore: The list of squares to ignore
        :param squares_to_add: the list of squares to add
        :param square: Square that has been reversed
        :param vector: Vector that was applied
        """

        # Get squares at new location
        list_of_squares = self.get_all(square)

        # If there is only one square, return
        if len(list_of_squares) == 1:
            return

        # If the numbers are equal
        if int(list_of_squares[0].number) == int(list_of_squares[1].number):
            squares_to_ignore.append(list_of_squares[0])
            squares_to_ignore.append(list_of_squares[1])

            self.combine_squares(list_of_squares[0], list_of_squares[1], squares_to_add)
            return

        # Remove square to get the square that was there first
        list_of_squares.remove(square)

        # Move that square back
        vector.inverse(list_of_squares[0])

        return self.check_location(list_of_squares[0], vector, list_of_squares, squares_to_add)

    def combine_squares(self, square1: Square, square2: Square, squares_to_add: list):
        """
        Used to combine two squares
        :param squares_to_add: List of squares to add after checking collisions
        :param square1: The first square
        :param square2: The second square
        """
        number = int(square1.number) + int(square2.number)

        coords = (square1.x, square1.y)
        squares_to_add.append(Square(number, (coords[0], coords[1]), self.boardSize))
        return squares_to_add

    def move_all(self, vector: Vector):  # vector: Vector, specifies that this is vector class
        """
        Used to move all the objects and check for collisions
        :param vector: Vector to apply to the objects
        """

        self.hasMoved = False

        # Move all the squares
        for square in self.objects:
            square.move(vector)

        squares_to_ignore = []
        squares_to_add = []

        # Check for collisions
        for square in self.objects:

            if square in squares_to_ignore:
                continue

            # Get the squares in this position
            # Will return 1-2 squares
            list_of_squares = self.get_all(square)

            # If there is only one square, there has been no collisions
            if len(list_of_squares) == 1:
                continue

            # If they are different numbers
            if int(list_of_squares[0].number) != int(list_of_squares[1].number):

                # If it has moved
                if (square.before_x, square.before_y) != (square.x, square.y):

                    # reverse the square
                    vector.inverse(square)

                    self.check_location(square, vector, squares_to_ignore, squares_to_add)

                continue

            # Otherwise, combine the squares
            squares_to_ignore.append(list_of_squares[0])
            squares_to_ignore.append(list_of_squares[1])

            self.combine_squares(list_of_squares[0], list_of_squares[1], squares_to_add)

        for square in squares_to_add:

            list_of_squares = self.get_all(square)

            if len(list_of_squares) > 1:
                self.objects.remove(list_of_squares[1])
            self.objects.remove(list_of_squares[0])

            self.add(square)

            # Updates the current the Score
            self.currentScore += square.number

        self.hasMoved = True

    def spawn(self) -> bool:
        """ Checks board for a random space
        and spawns either a 2 or a 4 in it through random choice
        :return: True there are no empty spaces
        """

        # Get random empty position
        position = self.get_empty_spaces()

        # Will return true if there are no empty spaces
        if len(position) == 0:
            return True

        # List of numbers in order to do probability
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Random number is selected
        probability = random.choice(numbers)

        # If the random number is less than or equal to 9 then generate a 2 at the empty position
        # A 2 will spawn 90% of the time
        if probability <= 9:
            self.add(Square(2, (position[0].x, position[0].y), self.boardSize))

        # If the random number is equal to 10 then generate a 4 at the empty position
        # A 4 will spawn 10% of the time
        if probability == 10:
            self.add(Square(4, (position[0].x, position[0].y), self.boardSize))

    def checkWin(self):
        """
        Checks if the game has been won
        :return:
        """

        for square in self.objects:

            if square.number == 2048:
                print("You WIn")

                return True

    def save_score(self):
        """
        Saves the previous score, should be called after every move
        :return: The current score from the previous move
        """

        # The previous score is equal to the score
        self.previousScore = self.temp

        # Score is equal to the current score
        self.temp = self.currentScore

        return self.previousScore

    def reset_board(self):
        """
        Resets the board
        :return:
        """

        # Removes all the squares from the board
        for square in self.objects:
            self.objects.remove(square)

        # Adds the first 2 squares back onto the board
        for row in self.rows:
            for column in self.columns:

                number = self.defaultBoard[row][column]

                if number != 0:
                    self.add(Square(number, (row, column), self.boardSize))

        # Starts empty
        self.previousBoard = copy.deepcopy(self.emptyBoard)

        # Resets the score
        self.previousScore = 0
        self.currentScore = 0

        # Empties the list of previous boards
        self.previousBoards = []

        print("Board and Score has been reset")

        return True

    def undo_move(self):
        """
        Makes the previous board into the current one, should be called after pressing the undo_move button
        :return: The board before the current move was made
        """

        # Empties the board of all the squares
        for square in self.objects:
            self.objects.remove(square)

        # Adds the Squares from the previous board onto the current board
        for row in self.rows:
            for column in self.columns:

                number = self.previousBoard[row][column]

                if number != 0:
                    self.add(Square(number, (row, column), self.boardSize))

        # Sets the current board to be equal to the board we just reverted to
        self.board = copy.deepcopy(self.previousBoard)

        # Undoes the score increase
        self.currentScore = self.previousScore

    def updateBoardArray(self):
        """
        Updates the 2D array, this will be used to undo moves
        :return:
        """

        # Copies the board before any changes are made to it, this is the previous state of the board
        # This is the only way to copy a 2D array without numpy
        self.previousBoard = copy.deepcopy(self.board)

        for row in self.rows:
            for column in self.columns:

                # Sets the value of every space in the 2D array to 0
                self.board[row][column] = 0

        print("----------------")
        for square in self.objects:

            # print(square.number, "| (", "x: ", square.x, ",", "y: ", square.y, ")")

            for _ in self.rows:
                for _ in self.columns:

                    self.board[square.x][square.y] = square.number

        # Updates the stack of previous boards with the newest instance of the previous board
        self.previousBoards.append(self.previousBoard)

        print("current board = ", self.board)
        print("previous board = ", self.previousBoard)

    def getHeuristic(self):
        """
        This method is used to calculate the heutristic score which will be used by the AI to decide what moves to make
        :return: The heuristic score
        """

        # The most optimal way for the board to be organized
        perfect_snake = [[2, 2 ** 2, 2 ** 3, 2 ** 4],
                         [2 ** 8, 2 ** 7, 2 ** 6, 2 ** 5],
                         [2 ** 9, 2 ** 10, 2 ** 11, 2 ** 12],
                         [2 ** 16, 2 ** 15, 2 ** 14, 2 ** 13]]

        # Variable to track the heuristic score
        h = 0

        for x in range(4):
            for y in range(4):

                # How the Heutristic score is calculated
                h += self.board[x][y] * perfect_snake[x][y]

        return h


# Initialising pygame for the RenderGameBoard class
pg.init()

"""
The RenderGameBoard class is where all of the pygame methods are stored for the GameBoard class.

this renders all the game-board and shows all of the changes being made to it on a move by move basis. 
it displays the score, the game-board itself, anything that needs to render anything for the GameBoard class is done 
in this class

In order to do this it inherits from the GameBoard class to make things easier to render, It also inherits from the
WinLose to render the to win and lose screen depending on the current game state.
"""


class RenderGameBoard(GameBoard, Text):

    def __init__(self):
        super().__init__()

    def draw(self, screen):
        """
        Draws the board
        :param screen: The current instance of the screen
        :return:
        """

        font = pg.font.SysFont('Arial', 30)

        size = 150
        padding = 2

        # reduces the square size if the board is a 5x5
        if self.boardSize == 5:
            size = 120

        # reduces the square size further if the board is a 6x6
        if self.boardSize == 6:
            size = 100

        for row in range(self.boardSize):
            for column in range(self.boardSize):

                y = (column * (size + padding))
                x = (row * (size + padding))

                # Default text positions for a 4x4 grid
                new_x = x + 70
                new_y = y + 64

                # Changes the text position if the board size is 5 
                if self.boardSize == 5:
                    new_x = x + 50
                    new_y = y + 44
                
                # Changes the text position if the board size is 6 
                if self.boardSize == 6:
                    new_x = x + 20
                    new_y = y + 14

                rect = pg.Rect(x, y, size, size)

                # Get the square at this location
                square = self.get(Position((column, row)))

                if square is not None:
                    pg.draw.rect(screen, self.get_colour(square.number), rect)
                    text_surface = font.render(str(square.number), True, (100, 100, 100))
                    screen.blit(text_surface, (new_x, new_y))

                else:
                    pg.draw.rect(screen, (255, 255, 255), rect)

    def get_game_state(self, screen):
        """
        Checks if you have won or lost
        :param screen: the screen
        :return:
        """

        # Checks if you have won, if you have it will display the WIN screen
        for square in self.objects:

            # Checks if you have won
            if square.number == 2048:
                print("YOU WIN")

                # Displays the YOU WIN screen
                # self.you_win_screen(screen, self.currentScore)

        # Checks if you have lost, if you have it will show the LOSE screen
        # In progress

    def draw_current_score(self, screen):
        """
        Draws the score next to the board
        :param screen: the screen
        """

        text = "Score: " + str(self.currentScore)

        self.draw_text(screen, text, 610, 200, 40)

    @staticmethod
    def get_colour(number) -> tuple:
        """ Assigns colours to the blocks with the corresponding numbers,
        :param number: The number on the rectangle
        :return: Tuple of the rectangle colour
        """

        if number == 2:
            return 244, 222, 172

        if number == 4:
            return 0, 200, 0

        if number == 8:
            return 0, 180, 20

        if number == 16:
            return 0, 150, 50

        if number == 32:
            return 0, 100, 100

        if number == 64:
            return 0, 50, 150

        if number == 128:
            return 0, 0, 200

        if number == 256:
            return 0, 0, 200

        if number == 512:
            return 0, 0, 200

        if number == 1024:
            return 0, 0, 200

        if number == 2048:
            return 0, 0, 200

        if number == 4096:
            return 0, 0, 200

        return 220, 220, 220
