from game_character import GameCharacter
from eyes import Eyes


# The Pinky class extends GameCharacter, so methods defined in GameCharacter
# are inherited by objects of class Pinky.
class Pinky(GameCharacter):
    def __init__(self, maze, pacman, game_controller):
        self.CHAR_WIDTH = 100
        self.CHAR_HEIGHT = 100
        self.maze = maze
        self.pacman = pacman
        self.gc = game_controller
        self.x = maze.WIDTH/2
        self.y = maze.TOP_HORIZ
        self.velocity = 2
        self.x_add = self.velocity
        self.y_add = 0
        self.eyes = Eyes()
        self.looking = (0, 0)
        self.WIN_PROXIMITY = 80
        self.WALL_TOLERANCE = 2
        self.last_move_direction = 'RIGHT'
        self.last_update_location = (0, 0)

    def draw_self(self, x, y):
        """Draw Pinky to the screen"""
        noStroke()
        fill(1.0, 0.5, 0.6)
        ellipse(x, y, 100, 100)
        bottom_half = createShape()
        bottom_half.beginShape()
        bottom_half.vertex(x, y)
        bottom_half.vertex(x+100, y)
        bottom_half.vertex(x+100, y+50)
        bottom_half.vertex(x+50, y+25)
        bottom_half.vertex(x, y+50)
        bottom_half.endShape()
        shape(bottom_half, -50, 0)

        self.eyes.display(x, y - 15, self.looking)

    def update(self):
        """Carry out necessary updates for each frame before
        drawing to screen"""
        # Check if Pinky is at an intersection
        on_vert = (
            (abs(self.x - self.maze.LEFT_VERT) < self.WALL_TOLERANCE) or
            (abs(self.x - self.maze.RIGHT_VERT) < self.WALL_TOLERANCE)
                   )
        on_horz = (
            (abs(self.y - self.maze.TOP_HORIZ) < self.WALL_TOLERANCE) or
            (abs(self.y - self.maze.BOTTOM_HORIZ) < self.WALL_TOLERANCE)
                   )

        # Check whether Pinky is up or down/left or right of Pacman
        up_down_part = self.pacman.y - self.y
        left_right_part = self.pacman.x - self.x

        # Update Pinky's eyes to look at Pacman
        self.update_eyes(up_down_part, left_right_part)

        # If Pinky gets close to Pacman, tell the GameController
        # that Pinky wins
        if (abs(up_down_part) < self.WIN_PROXIMITY and
                abs(left_right_part) < self.WIN_PROXIMITY):
            self.gc.pinky_wins = True

        # TODO:
        # PROBLEM 2: Make Pinky chase Pacman!
        # Study the code above and below these lines to understand how
        # Pinky's movements are calculated, and how Pinky's position with
        # respect to Pacman is represented.
        # Pinky should decide at each intersection whether to go left, right
        # up or down depending on which direction Pacman is further away in.
        # START CODE CHANGES

        def can_process():
            flag = abs(self.last_update_location[0] - self.x) > self.CHAR_WIDTH / 2 or abs(
                self.last_update_location[1] - self.y) > self.CHAR_WIDTH / 2
            if flag:
                self.last_update_location = (self.x, self.y)
            return flag

        def direction_change_handler(direction):
            self.last_move_direction = operation
            if direction == 'UP':
                self.x_add = 0
                self.y_add = -self.velocity
            elif direction == 'DOWN':
                self.x_add = 0
                self.y_add = self.velocity
            elif direction == 'LEFT':
                self.x_add = -self.velocity
                self.y_add = 0
            elif direction == 'RIGHT':
                self.x_add = self.velocity
                self.y_add = 0

        if (on_horz and on_vert) and can_process():
            potential_operations = []

            if up_down_part > 0:
                potential_operations.append('DOWN')
            elif up_down_part < 0:
                potential_operations.append('UP')

            if left_right_part > 0:
                potential_operations.append('RIGHT')
            elif left_right_part < 0:
                potential_operations.append('LEFT')

            for operation in potential_operations:
                if operation != self.last_move_direction:
                    direction_change_handler(operation)
                    break

            del potential_operations[:]  # cleanup
        # END CODE CHANGES

        # If the player wins, stop Pinky moving
        if self.gc.player_wins:
            self.x_add = 0
            self.y_add = 0

        # Move Pinky
        self.x = self.x + self.x_add
        self.y = self.y + self.y_add

    def update_eyes(self, up_down_part, left_right_part):
        """Set self.looking value based on position of Pinky w/r/t Pacman"""
        if up_down_part and abs(up_down_part) > 5:
            y = up_down_part/abs(up_down_part)
        else:
            y = 0
        if left_right_part and abs(left_right_part) > 5:
            x = left_right_part/abs(left_right_part)
        else:
            x = 0
        self.looking = (x, y)
