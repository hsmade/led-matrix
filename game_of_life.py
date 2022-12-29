import board
from neopixel import Display, Color
import random
from time import sleep

# Options
ROUND_WORLD = False  # if True object can move around edges, if False edge is treated as an empty cell
USE_USER_SEED = False  # if True USER_SEED will be used to settle cells on world map, if False random seed will be generated
USER_SEED = 27  # seed for the initial colony of cells
SIZE_OF_INITIAL_COLONY = 0.4  # where 1 is the whole map
UPDATE_DELAY = 0  # 0.2  # additional delay between population updates

# Constants
WORLD_WIDTH = 16  # number of cells horizontally
WORLD_HEIGHT = 16  # number of cells vertically
CELL_SIZE = 1  # side of single cell in pixels
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

MAX_AGE = len(COLOURS) - 1

# Variables
cells = []  # array where Cell objects will be stored
display = None
STOP = False
POLL = None


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.live = False
        self.live_neighbours = 0
        self.age = 0

    def check_neighbours(self):
        self.live_neighbours = 0
        x_to_check = [self.x]
        y_to_check = [self.y]
        if ROUND_WORLD:
            y_to_check.append((self.y - 1) % WORLD_HEIGHT)
            y_to_check.append((self.y + 1) % WORLD_HEIGHT)
            x_to_check.append((self.x - 1) % WORLD_WIDTH)
            x_to_check.append((self.x + 1) % WORLD_WIDTH)
        else:
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
                    if cells[x][y].live:
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
            draw_cell(self.x, self.y, self.age)
        else:
            self.age -= 1
            if self.age < 0:
                self.age = 0
            draw_cell(self.x, self.y, 0)


# Helper function used to draw single cell
def draw_cell(x, y, colour):
    global MAX_AGE
    for x_value in range(x * CELL_SIZE, x * CELL_SIZE + CELL_SIZE):
        for y_value in range(y * CELL_SIZE, y * CELL_SIZE + CELL_SIZE):
            # print("writing to x:", x_value, "y:", y_value, "index:", (y_value - 1) * 16 + (x_value - 1), "color:",
            #       colour)
            if colour > MAX_AGE:
                MAX_AGE = colour
            colour = int(colour / MAX_AGE * MAX_AGE)
            # print("    weighted color:", colour, "max:", MAX_AGE)
            display.set_pixel(x, y, COLOURS[colour])
            # pixels[(y_value - 1) * WORLD_WIDTH + (x_value - 1)] = COLOURS[colour]


def checksum():
    global cells
    sum = 0
    for index_x, y in enumerate(cells):
        for index_y, cell in enumerate(y):
            if cell.live:
                sum += cell.x + cell.y * 16
    return sum


# Create world filled with dead cells
def create_world():
    global cells
    for x in range(0, WORLD_WIDTH):
        cells.append([])
        for y in range(0, WORLD_HEIGHT):
            cells[x].append(Cell(x, y))


# Randomize initial state
def seed_world():
    global cells
    randomized_seed = ''
    if USE_USER_SEED:
        print("User seed used: ", USER_SEED)
        random.seed(USER_SEED)
    else:
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
                cells[x][y].change_state()
            if cells[x][y].live:
                draw_cell(x, y, MAX_AGE)


# Helper function used to update state of the colony
def update_colony():
    for row in cells:
        for cell in row:
            cell.check_neighbours()
    for row in cells:
        for cell in row:
            cell.apply_rules()
    display.draw()
    # display.print(color=False)


def reset():
    display.clear()
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            cells[x][y].live = False
            cells[x][y].age = 0
            cells[x][y].live_neighbours = 0


def main():
    global display
    display = Display(board.GP22, 16, 16, auto_write=False)

    create_world()
    seed_world()
    old_sum = 0
    older_sum = 0

    while True:
        if STOP:
            display.stop()
            return
        if POLL:
            POLL()

        update_colony()
        sleep(UPDATE_DELAY)
        current_sum = checksum()
        if old_sum == current_sum or older_sum == current_sum:
            print("reseed")
            sleep(1)
            reset()
            seed_world()
        older_sum = old_sum
        old_sum = checksum()


def set_poll(poll):
    global POLL
    POLL = poll


if __name__ == '__main__':
    main()