from gameboard import GameBoard
from vector import Vector
import copy


g = GameBoard()


class Move:

    def __init__(self):
        pass

    # Directions with vectors
    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)

    @staticmethod
    def getAllPossibleMoves():
        """
        Used to get a list of all the possible moves
        :return: List of possible moves
        """

        return [Move.left, Move.right, Move.up, Move.down]


class Algorithm:
    """
    Represents an algorithm
    """

    def __init__(self):
        pass

    instances: int = 0

    def get_best_move(self, gameboard: GameBoard, depth: int) -> Move:
        """
        Gets the best move
        :param gameboard: Is the instance of the gameboard
        :param depth: How far it sees into the future when analysing a move
        :return: Returns the best move
        """

        # Create map of moves
        # {value: move}
        moves = {}

        # For each move
        for move in Move.getAllPossibleMoves():

            # Create a new instance of the game board
            newInstance = copy.deepcopy(gameboard)
            self.instances += 1

            # Get vector from move
            vector = Vector(move)

            # Apply the vector to the game board
            for _ in range(4):
                newInstance.move_all(vector)

            newInstance.spawn()

            # Calculate_best_move using the new instance
            value = self.calculate_best_move(newInstance, depth - 1, -1000, 1000)

            # Save int value to map/dict
            moves[value] = move

        # Create int to track best score
        best_score = 0

        # Loop though dict
        for (key, value) in moves.items():

            # if value in dict is bigger then best score
            if best_score < key:
                best_score = key

        # Return BEST move
        return moves.get(best_score)

    def calculate_best_move(self, gameboard: GameBoard, depth, alfa, beta):
        """
        Calculates the best move
        :param beta:
        :param alfa:
        :param depth: How far it sees into the future when analysing a move
        :param gameboard: The instance of the current gameboard
        :return: Integer representing how good the move is
        """

        if depth == 0:
            return gameboard.currentScore

        max = -1000

        # For each move possible
        for move in Move.getAllPossibleMoves():

            # Create a new instance of the game board
            newInstance = copy.deepcopy(gameboard)
            self.instances += 1

            # --- Get vector ---
            vector = Vector(move)

            # Make the move on the board
            for _ in range(4):
                newInstance.move_all(vector)

            newInstance.spawn()

            newInstance.getHeuristic()

            # Calculate the best move for the new board
            value = self.calculate_best_move(newInstance, depth - 1, alfa, beta)

            if value > max:
                max = value
            if max > alfa:
                alfa = max
            if alfa >= beta:
                return beta

        return max
