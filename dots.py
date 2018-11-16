from dot import Dot


class Dots:
    """A collection of dots."""
    def __init__(self, WIDTH, HEIGHT,
                 LEFT_VERT, RIGHT_VERT,
                 TOP_HORIZ, BOTTOM_HORIZ):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TH = TOP_HORIZ
        self.BH = BOTTOM_HORIZ
        self.LV = LEFT_VERT
        self.RV = RIGHT_VERT
        self.SPACING = 75
        self.EAT_DIST = 50
        # Initialize four rows of dots, based on spacing and width of the maze
        self.top_row = [Dot(self.SPACING * i, self.TH)
                        for i in range(self.WIDTH//self.SPACING + 1)]
        self.bottom_row = [Dot(self.SPACING * i, self.BH)
                           for i in range(self.WIDTH//self.SPACING + 1)]
        self.left_col = [Dot(self.LV, self.SPACING * i)
                         for i in range(self.HEIGHT//self.SPACING + 1)]
        self.right_col = [Dot(self.RV, self.SPACING * i)
                          for i in range(self.HEIGHT//self.SPACING + 1)]

    def display(self):
        """Calls each dot's display method"""
        for i in range(0, len(self.top_row)):
            self.top_row[i].display()
        for i in range(0, len(self.bottom_row)):
            self.bottom_row[i].display()
        for i in range(0, len(self.left_col)):
            self.left_col[i].display()
        for i in range(0, len(self.right_col)):
            self.right_col[i].display()

    # TODO:
    # PROBLEM 3: implement dot eating
    # BEGIN CODE CHANGES
    def eat(self, pacman_x, pacman_y):  # You might want/need to pass arguments here.
        self.dots_handler(self.top_row, pacman_x, pacman_y)
        self.dots_handler(self.bottom_row, pacman_x, pacman_y)
        self.dots_handler(self.left_col, pacman_x, pacman_y)
        self.dots_handler(self.right_col, pacman_x, pacman_y)
    
    def dots_handler(self, dots, pacman_x, pacman_y):
        index = None

        if len(dots) == 0:
            return
        for i in range(len(dots)):
            if dots[i] == None:
                continue

            vertial_part = pacman_y - dots[i].y
            horizontal_part = pacman_x - dots[i].x

            if abs(vertial_part) < self.EAT_DIST and abs(horizontal_part) < self.EAT_DIST:
                index = i
                break
        if index is not None:
            del dots[index]

    # END CODE CHANGES

    def dots_left(self):
        """Returns the number of remaing dots in the collection"""
        return (len(self.top_row) +
                len(self.bottom_row) +
                len(self.left_col) +
                len(self.right_col))
