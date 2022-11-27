from position import Position
from vector import Vector


class Square(Position):

    def __init__(self, number, coords, border):
        super().__init__(coords)

        self.x = coords[0]
        self.y = coords[1]

        # Defines the grid border, the default grid is a 4x4 so the default value is 3
        self.border = border

        self.number = number

    def move(self, vector: Vector):
        """
        Moves the square
        :param vector: Vector to move by
        :return:
        """

        # Adds the vector ontp the coordinates of the square
        vector.append(self)

        # Condititions to make sure the squares do not bug out into the wrong spaces
        # These specify the boards borders
        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        # Sets the boundaries if the grid size is 4x4
        if self.border == 4:
            
            if self.x > 3:
                self.x = 3
            
            if self.y > 3:
                self.y = 3
        
        # Sets the boundares if the grid size is 5x5
        if self.border == 5:

            if self.x > 4:
                self.x = 4
            
            if self.y > 4:
                self.y = 4
        
        # Sets the boundaries if the grid size is 6x6
        if self.border == 6:

            if self.x > 5:
                self.x = 5
        
            if self.y > 5:
                self.y = 5