class Position:

    before_x = None
    before_y = None

    def __init__(self, coords):

        x = coords[0]
        y = coords[1]

        self.x = x
        self.y = y

    def compare(self, position) -> bool:
        """
        Compares a position to its self
        :param position: Position to compare too
        :return: True if they are in the same location
        """

        return (position.x, position.y) == (self.x, self.y)
