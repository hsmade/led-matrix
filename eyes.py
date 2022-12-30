from neopixel import Color
from time import sleep
from scene import Scene

WHITE = Color(32, 32, 32)
DBLUE = Color(0, 0, 32)
LBLUE = Color(16, 16, 32)
BROWN = Color(28, 16, 0)
SKIN = Color(48, 32, 0)
NONE = Color(0, 0, 0)

FRAME1 = [
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE, NONE, NONE],
    [BROWN, BROWN, BROWN, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, BROWN, NONE, NONE, NONE],

    [BROWN, NONE, WHITE, DBLUE, DBLUE, BROWN, NONE, NONE, NONE, NONE, DBLUE, WHITE, BROWN, NONE, NONE, NONE],
    [BROWN, NONE, WHITE, LBLUE, DBLUE, NONE, NONE, NONE, NONE, NONE, DBLUE, WHITE, BROWN, NONE, NONE, NONE],
    [BROWN, BROWN, WHITE, LBLUE, LBLUE, NONE, NONE, NONE, NONE, NONE, LBLUE, WHITE, BROWN, NONE, NONE, NONE],

    [BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE, NONE, NONE],
    [BROWN, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
]

FRAME2 = [
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE],
    [BROWN, BROWN, BROWN, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, BROWN, BROWN, BROWN, NONE],

    [BROWN, NONE, WHITE, DBLUE, DBLUE, BROWN, NONE, NONE, NONE, BROWN, DBLUE, DBLUE, WHITE, NONE, BROWN, NONE],
    [BROWN, NONE, WHITE, LBLUE, DBLUE, NONE, NONE, NONE, NONE, NONE, DBLUE, LBLUE, WHITE, NONE, BROWN, NONE],
    [BROWN, BROWN, WHITE, LBLUE, LBLUE, NONE, NONE, NONE, NONE, NONE, LBLUE, LBLUE, WHITE, BROWN, BROWN, NONE],

    [BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE],
    [BROWN, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, BROWN, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
]

FRAME3 = [
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE],
    [NONE, BROWN, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, BROWN, BROWN, BROWN, NONE],

    [NONE, BROWN, WHITE, DBLUE, NONE, NONE, NONE, NONE, NONE, BROWN, DBLUE, DBLUE, WHITE, NONE, BROWN, NONE],
    [NONE, BROWN, WHITE, DBLUE, NONE, NONE, NONE, NONE, NONE, NONE, DBLUE, LBLUE, WHITE, NONE, BROWN, NONE],
    [NONE, BROWN, WHITE, LBLUE, NONE, NONE, NONE, NONE, NONE, NONE, LBLUE, LBLUE, WHITE, BROWN, BROWN, NONE],

    [NONE, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, NONE],
    [NONE, BROWN, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, BROWN, BROWN, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    [NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
]


class Eyes(Scene):
    def show(self, frame):
        for x in range(16):
            for y in range(16):
                self._display.set_pixel(x, y, frame[y][x])
        self._display.draw()

    def iter(self):
        self.show(FRAME1)
        sleep(2)
        # self.show(FRAME2)
        # sleep(1)
        self.show(FRAME3)
        sleep(2)
