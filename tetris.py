from scene import Scene
from adafruit_pixel_framebuf import PixelFramebuffer
from  adafruit_led_animation import color
from time import sleep
import random

# define blocks
BRICKS = [
    {"color": color.RED, "shape":    [(0, 0), (1, 1), (1, 0), (2, 1)]}, # -\_
    {"color": color.GREEN, "shape":  [(0, 1), (1, 1), (1, 0), (2, 0)]}, # _/-
    {"color": color.BLUE, "shape":   [(0, 0), (0, 1), (1, 1), (2, 1)]}, # |__
    {"color": color.YELLOW, "shape": [(0, 1), (0, 0), (1, 1), (1, 0)]}, # []
    {"color": color.PURPLE, "shape": [(0, 1), (1, 1), (2, 1), (1, 0)]}, # _|_
    {"color": color.AQUA, "shape":   [(0, 1), (1, 1), (2, 1), (3, 1)]}, # ____
    {"color": color.ORANGE, "shape": [(0, 1), (1, 1), (2, 1), (2, 0)]}, # __|
]


class Brick():
    def __init__(self, framebuf, shape, color):
        self.shape = shape
        self.base_shape = shape
        self.color = color
        self._framebuf = framebuf

    def rotate(self): # FIXME, splits the thing apart
        x_offset = self.get_left() + self.get_width() // 2
        y_offset = self.get_top() + self.get_height() // 2
        self.remove()

        translated_shape = [(x - x_offset, y - y_offset) for x, y in self.shape]
        rotated_shape = [(-y, x) for x, y in translated_shape]
        self.shape = [(x + x_offset, y + y_offset) for x, y in rotated_shape]

    def move(self, dx, dy):
        self.remove()
        self.shape = [(x + dx, y + dy) for x, y in self.shape]

    def remove(self):
        for x, y in self.shape:
            self._framebuf.pixel(x, y, color.BLACK)

    def draw(self):
        for x, y in self.shape:
            self._framebuf.pixel(x, y, self.color)

    def can_move(self, dx, dy, occupied):
        for x, y in self.shape:
            if x + dx < 0 or x + dx >= 16 or y + dy < 0 or y + dy >= 16:
                # print("can_move: out of bounds", x, dx, y, dy)
                return False
            if occupied[x + dx][y + dy]:
                # print("can_move: occupied", x, dx, y, dy)
                return False
        return True

    def can_rotate(self, occupied):
        backup_shape = self.shape
        self.rotate()
        can = True
        for x, y in self.shape:
            if x < 0 or x >= 16 or y < 0 or y >= 16:
                can = False
                break
            if occupied[x][y]:
                can = False
                break
        self.shape = backup_shape
        return can

    def get_bounding_box(self):
        min_x = min(x for x, y in self.shape)
        max_x = max(x for x, y in self.shape)
        min_y = min(y for x, y in self.shape)
        max_y = max(y for x, y in self.shape)
        return min_x, max_x, min_y, max_y

    def get_bottom(self):
        return max(y for x, y in self.shape)

    def get_left(self):
        return min(x for x, y in self.shape)

    def get_right(self):
        return max(x for x, y in self.shape)

    def get_top(self):
        return min(y for x, y in self.shape)

    def get_width(self):
        return self.get_right() - self.get_left() + 1

    def get_height(self):
        return self.get_bottom() - self.get_top() + 1

    def find_best_position(self, occupied):
        best_position = None
        best_rotation = 0
        best_score = None
        shape_backup = self.shape

        for y in range(15, self.get_bottom(), -1):
            for x in range(17):
                if self.can_move(x - self.get_left(), y - self.get_bottom(), occupied):
                    self.move(x - self.get_left(), y - self.get_bottom())
                    if self.can_move(x - self.get_left(), y - self.get_bottom() + 1, occupied):
                        # print("space below us", x, y)
                        continue # space below us, can't score
                    for r in range(0, 4):
                        if self.can_rotate(occupied):
                            score = self.get_score(occupied)
                            if best_score is None or score > best_score:
                                print("better score at", x, y, r, score)
                                best_score = score
                                best_position = (x, y)
                                best_rotation = r
                            self.rotate()
                # else:
                #     print("can't move to", x, y)
        self.shape = shape_backup
        return best_position, best_rotation

    def get_score(self, occupied):
        score = 0
        for (x, y) in self.shape:
            if not occupied[x][y]:
                # FIXME: make Z and ____ always stand upright
                score += y - (self.get_top() - 1) # lower parts get more points
        return score

class Tetris(Scene):
    def __init__(self, display):
        super().__init__(display=display)
        self._framebuf = PixelFramebuffer(self._display, 16, 16, rotation=0, alternating=False)
        self.reset()

    def pick_brick(self):
        index = random.randint(0, len(BRICKS) - 1)
        self.brick = Brick(self._framebuf, BRICKS[index]["shape"], BRICKS[index]["color"])


    def reset(self):
        self._display.clear()
        self.occupied = [[False] * 16 for _ in range(16)]
        self.pick_brick()
        self.brick.move(8, 8) # FIXME was dy:1
        self.game_over = False

    def occupied_brick(self, brick):
        for x, y in brick.shape:
            print("occupied", x, y)
            self.occupied[x][y] = True

    def remove_full_lines(self):
        # FIXME: this is not working
        for y in range(16):
            if all(self.occupied[x][y] for x in range(16)):
                for x in range(16):
                    self.occupied[x][y] = False
                for y1 in range(y, 0, -1):
                    for x in range(16):
                        self.occupied[x][y1] = self.occupied[x][y1 - 1]
        self._framebuf.fill(0)
        for x in range(16):
            for y in range(16):
                if self.occupied[x][y]:
                    self._framebuf.pixel(x, y, color.WHITE)

    def iter(self):
        if self.game_over:
            print("game over, resetting")
            self.reset()
            return

        # print("best rot", self.brick.find_best_rotation(self.occupied))
        print("best pos", self.brick.find_best_position(self.occupied))

        pos, rot = self.brick.find_best_position(self.occupied)
        if pos is not None:
            for _ in range(0, rot):
                if self.brick.can_rotate(self.occupied):
                    self.brick.rotate()
            if self.brick.can_move(pos[0] - self.brick.get_left(), 0, self.occupied):
                self.brick.move(pos[0] - self.brick.get_left(), 0)

            # see if we need to shift right to have a path downwards
            for x in range(self.brick.get_right(), 16):
                if self.brick.can_move(0, 1,self.occupied):
                    break
                else:
                    self.brick.move(x - self.brick.get_right(), 0)


        if self.brick.can_move(0, 1, self.occupied):
            print("can move")
            self.brick.move(0, 1)
        else:
            print("can't move")
            self.brick.draw()
            self.occupied_brick(self.brick)
            self.pick_brick()
            self.brick.move(8, 1)
            if not self.brick.can_move(0, 0, self.occupied):
                self.game_over = True

        # self.remove_full_lines()
        self.brick.draw()
        self._framebuf.display()
        # sleep(2)
