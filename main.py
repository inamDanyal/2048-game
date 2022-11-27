from server import Server
import time
from client import Client
import sys
from algorithm import Algorithm
from algorithm import Move
import multiprocessing as mp
# import threading
from gameboard import *
from button import Button
from button import InputBox


# Initialising the classes
s = Server()
t = Text()
l = RenderGameBoard()
c = Client()
al = Algorithm()
g = GameBoard()
m = Move()

"""
pygame : Used to create the graphical interface, imported from logic  
logic : Used to create the board and all of the game logic is done inside of this class
time : Used to set delays between some events 
client : Used to join other servers for multiplayer capability
button : Used to create and draw functional buttons
text : Used to write text onto the various screens
sys : Used to give functionality to the quit button 
algorithm : Contains the AI algorithm which returns the best move to make in any given state of the game board
logic : is imported to initialise variables for the main file, it is done in this file to prevent the main file from
        getting too long and messy
Button : is imported to initialise buttons here instead of in the main file to prevent the main file form getting too 
         cluttered and messy
"""

# Initialising pygame
pg.init()

# Initialising pygame fonts
pg.font.init()

# The width of the screen
WIDTH = 1000

# The height of the screen
HEIGHT = 600

# Size of the screen
size = (WIDTH, HEIGHT)

# Making the screen variable
screen = pg.display.set_mode(size)

# turing the screen into a surface
surface = pg.Surface([WIDTH, HEIGHT])

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (50, 255, 100)
DARK_GREEN = (80, 255, 40)
RED = (255, 80, 80)
DARK_RED = (255, 40, 40)
BLUE = (100, 100, 255)
DARK_BLUE = (50, 50, 255)

# Directions with vectors
left = (0, -1)
right = (0, 1)
up = (-1, 0)
down = (1, 0)

# Frames per second
fps = pg.time.Clock()

# Initialising the buttons
# Button(screen, width: int, height: int, x: int, y: int, fontSize: int)
play_button = Button(screen, 200, 100, 450, 100, 50)
multiplayer_button = Button(screen, 400, 100, 275, 310, 50)
quit_button = Button(screen, 200, 100, 450, 400, 50)
reset_button = Button(screen, 230, 100, 670, 430, 50)
undoMove_button = Button(screen, 230, 100, 670, 300, 50)

start_server_button = Button(screen, 420, 100, 295, 100, 50)
join_server_button = Button(screen, 400, 100, 295, 250, 50)

single_player_button = Button(screen, 400, 100, 275, 75, 50)
AI_button = Button(screen, 200, 100, 450, 250, 50)

# customGame_button = Button(screen, 350, 100, 335, 250, 50)

fourbyfour_button = Button(screen, 200, 100, 432, 120, 50)
fiveByFive_button = Button(screen, 200, 100, 432, 220, 50)
sixBySix_button = Button(screen, 200, 100, 432, 320, 50)

# Initialising the input box
input = InputBox(200, 200, 200, 50)


# class for all the game loops
class GameLoops(RenderGameBoard, Text, Client):

    def __init__(self):
        super().__init__()

        self.screen = screen

        # The text inputted into dialog boxes
        self.inputText = ''

    def multiplayer(self):
        """
        This method will allow the player to either start a multiplayer session as a host or to join one as a client
        :return:
        """

        run = True
        while run:

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            self.screen.fill(BLACK)

            # Drawing the networking buttons
            start_server_button.draw_button("START SERVER", BLACK, BLUE, DARK_BLUE)
            join_server_button.draw_button("JOIN SERVER", BLACK, BLUE, DARK_BLUE)

            # Giving functionality to the networking buttons
            if start_server_button.check_clicked():
                # mp.Process(target=s.start_server).start()
                self.server_loop()

            join_server_button.function(self.join_loop)

            pg.display.update()

    def join_loop(self):

        # Assigning the command to a variable to make it easier to use
        keys = pg.key.get_pressed()

        run = True
        while run:

            user_text = ''

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False
                input.toggle()

            # print("staring connection (client)")
            input.draw()
            input.update()
           

            # Starts the connection to the server and handles the rest of the client functions
            # c.main_conn()

            pg.display.flip()

    def server_loop(self):
        """
        This the event loop when you want to start a server
        :return: none
        """

        run = True
        while run:

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            self.screen.fill(BLACK)

            t.draw_text(screen, "Your IP is: " + s.HOST, 320, 50, 25)
            t.draw_text(screen, "Server is up and running", 200, 200, 40)
            t.draw_text(screen, "Awaiting connection...", 260, 250, 40)

            # threading.Thread(target=s.start_server(), args=()).start()  # threading

            # p1 = mp.Process(target=s.start_server).start()

            pg.display.update()

    @staticmethod
    def exit_game():
        """
        Exits the game
        """
        sys.exit()

    def main_game(self):
        """
        main game loop
        :return: draws the board to the screen and allows you to play the game
        """

        # Setting the caption in the window to say 2048
        pg.display.set_caption("2048")

        run = True
        while run:

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False
                    if event.key == pg.K_c:
                        for _ in range(3):
                            self.reset_board()

            # Assigning the command to a variable to make it easier to use
            keys = pg.key.get_pressed()

            # Setting the caption in the window to say 2048
            pg.display.set_caption("2048")

            # Fills the screen to Black
            self.screen.fill(BLACK)

            # Update the board
            self.draw(self.screen)

            # Draws the score
            self.draw_current_score(self.screen)

            # Draws the reset button and gives it functionality
            reset_button.draw_button("RESET", BLACK, GREEN, DARK_GREEN)
            reset_button.function(self.reset_board)

            # Draws the undo move button and gives it functionality
            undoMove_button.draw_button("UNDO", BLACK, GREEN, DARK_GREEN)
            undoMove_button.function(self.undo_move)

            # Gets the current state of the board to check if you have won or lost
            # self.get_game_state(self.screen)

            # If the game has been won then show the YOU WIN screen
            if self.checkWin():
                self.you_win_screen()

            # setting keys pressed to if not false to go into a for loop so that each key is pressed 4 times
            # before being able to make another move

            if (keys[pg.K_LEFT], keys[pg.K_RIGHT], keys[pg.K_UP], keys[pg.K_DOWN]) != (False, False, False, False):
                # Move 6 times, loops 5 times so that the blocks on all board sizes can reach the opposite side without the need of for loops
                # The borderSize in the Squares class prevents the tiles to go off the board 
                for _ in range(5):
                    time.sleep(0.09)

                    # Update the board
                    self.draw(screen)

                    # Update screen
                    pg.display.flip()

                    if keys[pg.K_LEFT]:  # move Left
                        self.move_all(Vector(left))

                    if keys[pg.K_RIGHT]:  # move Right
                        self.move_all(Vector(right))

                    if keys[pg.K_UP]:  # move Up
                        self.move_all(Vector(up))

                    if keys[pg.K_DOWN]:  # move Down
                        self.move_all(Vector(down))

            if keys[pg.K_LEFT]:

                # Spawns a new block after every move
                self.spawn()

                # Updates the previous score after every move
                self.save_score()

                # Updates the 2D array representation of the board, used to allow Undo move functionality
                self.updateBoardArray()

                # print("currentScore = ", self.currentScore, "previousScore", self.previousScore)
                msg = {"COMMAND": "MOVE", "MOVE": {"DIRECTION": "LEFT"}}  # message that will be sent to the server
                # c.send(msg)  # sends the message to the server
                print("-------------------------")
                print("MOVED LEFT")

            if keys[pg.K_RIGHT]:

                # Spawns a new block after every move
                self.spawn()

                # Updates the previous score after every move
                self.save_score()

                # Updates the 2D array representation of the board, used to allow Undo move functionality
                self.updateBoardArray()

                # print("currentScore = ", self.currentScore, "previousScore", self.previousScore)
                msg = {"COMMAND": "MOVE", "MOVE": {"DIRECTION": "RIGHT"}}  # message that will be sent to the server
                # c.send(msg)  # sends the message to the server
                print("-------------------------")
                print("MOVED RIGHT")

            if keys[pg.K_UP]:

                # Spawns a new block after every move
                self.spawn()

                # Updates the previous score after every move
                self.save_score()

                # Updates the 2D array representation of the board, used to allow Undo move functionality
                self.updateBoardArray()

                # print("currentScore = ", self.currentScore, "previousScore", self.previousScore)
                msg = {"COMMAND": "MOVE", "MOVE": {"DIRECTION": "UP"}}  # message that will be sent to the server
                # c.send(msg)  # sends the message to the server
                print("-------------------------")
                print("MOVED UP")

            if keys[pg.K_DOWN]:

                # Spawns a new block after every move
                self.spawn()

                # Updates the previous score after every move
                self.save_score()

                # Updates the 2D array representation of the board, used to allow Undo move functionality
                self.updateBoardArray()

                # print("currentScore = ", self.currentScore, "previousScore", self.previousScore)
                msg = {"COMMAND": "MOVE", "MOVE": {"DIRECTION": "DOWN"}}  # message that will be sent to the server
                # c.send(msg)  # sends the message to the server
                print("-------------------------")
                print("MOVED DOWN")

            # Update screen
            pg.display.flip()

            # Limiting the frame limit to 60 frames per second
            fps.tick(60)

    def menu(self):
        """
        Menu loop
        :return: draws the menu onto the screen
        """
        run = True
        while run:

            # Setting the caption in the window to say "Menu"
            pg.display.set_caption("Menu")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            # Giving the screen a black background
            self.screen.fill(BLACK)

            # Drawing the buttons
            play_button.draw_button("PLAY", BLACK, RED, DARK_RED)
            AI_button.draw_button("AI", BLACK, GREEN, DARK_GREEN)
            quit_button.draw_button("QUIT", BLACK, RED, DARK_RED)

            # Runs the functions if the buttons are clicked
            play_button.function(self.selection)
            AI_button.function(self.AI_selection)
            quit_button.function(self.exit_game)

            # Drawing a decorative 2048 on the menu
            self.draw_2048(self.screen, 65, 65, 150, GRAY, WHITE)

            # Update screen
            pg.display.flip()

            # Limiting the frame limit to 60 frames per second
            fps.tick(60)

    def selection(self):

        run = True
        while run:
            # Setting the caption in the window to say "Menu"
            pg.display.set_caption("Selection")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            # fills black over the previous screen
            self.screen.fill(BLACK)

            single_player_button.draw_button("SINGLE-PLAYER", BLACK, GREEN, DARK_GREEN)
            multiplayer_button.draw_button("MULTIPLAYER", BLACK, RED, DARK_RED)

            single_player_button.function(self.custom_game_selection)
            multiplayer_button.function(self.multiplayer)

            pg.display.update()
            fps.tick(60)

    def custom_game_selection(self):
        """
        Here you will be able to select a board size out of a 5x5 or a 6x6.
        :return:
        """

        run = True
        while run:
            # Setting the caption in the window to say "Menu"
            pg.display.set_caption("Selection")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            # fills black over the previous screen
            self.screen.fill(BLACK)
            
            fiveByFive_button.draw_button("5x5 Grid", BLACK, BLUE, DARK_BLUE)
            sixBySix_button.draw_button("6x6 Grid", BLACK, RED, DARK_RED)

            # If 5x5 is chosen then change the board size to 5 and load the game
            if fiveByFive_button.check_clicked():
                self.boardSize = 5
                self.changeBoardSize()
                self.main_game()

            # If 6x6 is chosen then change the board size to 6 and load the game
            if sixBySix_button.check_clicked():
                self.boardSize = 6
                self.changeBoardSize()
                self.main_game()

            pg.display.update()
            fps.tick(60)
    
    def AI_selection(self):
        """
        Here you will be able to select the board size for the AI game
        :return: none
        """
        run = True
        while run:
            # Setting the caption in the window to say "Menu"
            pg.display.set_caption("Selection")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            # fills black over the previous screen
            self.screen.fill(BLACK)

            # Initialising the buttons
            fourbyfour_button.draw_button("4x4 Grid", BLACK, BLUE, DARK_BLUE)
            fiveByFive_button.draw_button("5x5 Grid", BLACK, BLUE, DARK_BLUE)
            sixBySix_button.draw_button("6x6 Grid", BLACK, BLUE, DARK_BLUE)

            # The events triggered if the four by four button is clicked
            if fourbyfour_button.check_clicked():
                self.boardSize = 4
                self.changeBoardSize()
                self.AI_game()
            
            # The events triggered if the five by five button is clicked
            if fiveByFive_button.check_clicked():
                self.boardSize = 5
                self.changeBoardSize()
                self.AI_game()
            
            # The events triggered if the six by six button is clicked
            if sixBySix_button.check_clicked():
                self.boardSize = 6
                self.changeBoardSize()
                self.AI_game()

            pg.display.update()
            fps.tick(60)

    def AI_game(self):

        run = True
        while run:

            # Setting the caption in the window to say "Menu"
            pg.display.set_caption("AI")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False
                    if event.key == pg.K_c:
                        for _ in range(5):
                            self.reset_board()

            # fills black over the previous screen
            self.screen.fill(BLACK)

            # Draws the reset button onto the screen and gives it functionality
            reset_button.draw_button("RESET", BLACK, GREEN, DARK_GREEN)
            reset_button.function(self.reset_board)

            # Moves the blocks on the screen by the vector returned by the algorithm 4 times
            for _ in range(4):
                self.move_all(Vector(al.get_best_move(g, 2)))

            # Prints the number of instances
            print("Instances : " + str(al.instances))
            al.instances = 0

            # Saves the score everytime a move is made
            self.save_score()

            # spawns a new block every time a move is made
            self.spawn()

            # Draws the board onto the screen
            self.draw(self.screen)

            # Draws the current score
            self.draw_current_score(self.screen)

            # If the game has been won then show the YOU WIN screen
            if self.checkWin():
                self.you_win_screen()

            # Updates the screen
            pg.display.update()
            # Sets the fps to 60
            fps.tick(60)

    def you_win_screen(self):
        """
        This method is called when you have created a block with the value of 2048
        :return takes you to the YOU WIN screen
        """

        run = True
        while run:

            # Setting the caption in the window to say "YOU WIN!!!!"
            pg.display.set_caption("YOU WIN!!!!")

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

            # Draws over the previous screen to give the illusion of a new screen
            self.screen.fill(BLACK)

            # Draws YOU WIN onto the screen along with your score when you WIN
            self.draw_win(self.screen)
            self.draw_score(self.screen, self.currentScore)

    def you_lose_screen(self):
        """
        This method is called when you have no more moves available before you have created a block with the value
        2048

        :return takes you to the YOU LOSE screen
        """

        run = True
        while run:

            for event in pg.event.get():  # Initialising close events so when you click the cross in the top right the
                if event.type == pg.QUIT:  # Game stops running
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        run = False

                        # Setting the caption in the window to say "YOU LOSE!!!!"
                        pg.display.set_caption("YOU LOSE!!!!")

            # Draws over the previous screen to give the illusion of a new screen
            screen.fill(BLACK)

            # Draws YOU LOSE onto the screen along with your score when you lost
            self.draw_lose(self.screen)
            self.draw_score(self.screen, self.currentScore)


game = GameLoops()
game.menu()
