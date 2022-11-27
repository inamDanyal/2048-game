from position import Position


class Vector(Position):

    def __init__(self, move):
        super().__init__(move)

    def append(self, position: Position):
        """
        Used to combine squares on collision if the numbers are equal
        :param position: Position of the square
        """

        position.before_x = position.x
        position.before_y = position.y

        position.x += self.x
        position.y += self.y

    def inverse(self, position: Position):
        """
        Used when the numbers in the squares are different to stop them from deleting a square when colliding
        Applies the opposite vector
        :param position: Position to apply to
        """

        position.x -= self.x
        position.y -= self.y
