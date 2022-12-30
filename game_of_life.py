from neopixel import Color
import random
from time import sleep
from scene import Scene
from collections import deque

# Options
SIZE_OF_INITIAL_COLONY = 0.4  # where 1 is the whole map

# Constants
WORLD_WIDTH = 16  # number of cells horizontally
WORLD_HEIGHT = 16  # number of cells vertically
CENTER_X = int(WORLD_WIDTH / 2)
CENTER_Y = int(WORLD_HEIGHT / 2)

COLOURS = [
    Color(0, 0, 0),
    Color(0, 150, 0),
    Color(100, 200, 0),
    # Color(150, 255, 0),
    Color(200, 200, 0),
    # Color(255, 255, 0),
    Color(255, 200, 0),
    # Color(255, 150, 0),
    Color(255, 100, 0),
    Color(255, 0, 0),
]


class Cell:
    def __init__(self, x, y, other_cells):
        self.x = x
        self.y = y
        self.live = False
        self.live_neighbours = 0
        self.age = 0
        self.other_cells = other_cells

    def check_neighbours(self):
        self.live_neighbours = 0
        x_to_check = [self.x]
        y_to_check = [self.y]
        if self.y > 0:  # if cell is in the row 0, it doesn't have neighbours above
            y_to_check.append(self.y - 1)
        if self.y < WORLD_HEIGHT - 1:  # if cell is in the lowest row, it doesn't have neighbours below
            y_to_check.append(self.y + 1)
        if self.x > 0:  # if cell is in the left column, it doesn't have neighbours from the left side
            x_to_check.append(self.x - 1)
        if self.x < WORLD_WIDTH - 1:  # if cell is in the right column, it doesn't have neighbours from the right side
            x_to_check.append(self.x + 1)
        for y in y_to_check:
            for x in x_to_check:
                if y != self.y or x != self.x:
                    if self.other_cells[x][y].live:
                        self.live_neighbours += 1

    def change_state(self):  # changes state of the cell to opposite
        self.live = not self.live

    def apply_rules(self):
        if self.live:
            if self.live_neighbours < 2 or self.live_neighbours > 3:
                self.change_state()
        if not self.live and self.live_neighbours == 3:
            self.change_state()

        if self.live:
            self.age += 1
            if self.age > 6:
                self.age = 6
            return self.age
        else:
            self.age -= 1
            if self.age < 0:
                self.age = 0
            return 0


class GameOfLife(Scene):
    def __init__(self, display):
        super().__init__(display=display)
        self.create_world()
        self.seed_world()
        self.sums = deque([0, 0, 0])
        self.cells = []
        self.max_age = len(COLOURS) - 1

    def iter(self):
        self.update_colony()
        self.sums[0] = self.checksum()

        # if we're stuck in a loop
        if self.sums[0] in self.sums[1:2]:
            sleep(1)
            self.reset()
        self.sums.rotate(1)

    def reset(self):
        self._display.clear()
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                self.cells[x][y].live = False
                self.cells[x][y].age = 0
                self.cells[x][y].live_neighbours = 0

    def update_colony(self):
        for row in self.cells:
            for cell in row:
                cell.check_neighbours()
        for row in self.cells:
            for cell in row:
                age = cell.apply_rules()
                self.draw_cell(cell.x, cell.y, age)
        self._display.draw()

    def seed_world(self):
        randomized_seed = ''
        for counter in range(0, 6):
            randomized_seed += str(random.randrange(0, 10))
        print("Seed used: ", randomized_seed)
        random.seed(int(randomized_seed))
        for y in range(int(CENTER_Y - SIZE_OF_INITIAL_COLONY * CENTER_Y),
                       int(CENTER_Y + SIZE_OF_INITIAL_COLONY * CENTER_Y)):
            for x in range(int(CENTER_X - SIZE_OF_INITIAL_COLONY * CENTER_X),
                           int(CENTER_X + SIZE_OF_INITIAL_COLONY * CENTER_X)):
                finger_of_god = random.randrange(0, 2)
                if finger_of_god == 1:
                    self.cells[x][y].change_state()
                if self.cells[x][y].live:
                    self.draw_cell(x, y, self.max_age)

    def create_world(self):
        for x in range(0, WORLD_WIDTH):
            self.cells.append([])
            for y in range(0, WORLD_HEIGHT):
                self.cells[x].append(Cell(x, y, self.cells))

    def checksum(self):
        result = 0
        for index_x, y in enumerate(self.cells):
            for index_y, cell in enumerate(y):
                if cell.live:
                    result += cell.x + cell.y * 16
        return result

    def draw_cell(self, x, y, colour):
        for x_value in range(x, x + 1):
            for y_value in range(y, y + 1):
                # print("writing to x:", x_value, "y:", y_value, "index:", (y_value - 1) * 16 + (x_value - 1), "color:",
                #       colour)
                if colour > self.max_age:
                    self.max_age = colour
                colour = int(colour / self.max_age * self.max_age)
                self._display.set_pixel(x, y, COLOURS[colour])
