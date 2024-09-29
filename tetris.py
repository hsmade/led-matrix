from neopixel import Color
from scene import Scene
from adafruit_pixel_framebuf import PixelFramebuffer

# define colors
YELLOW = Color(0xff, 0xff, 32)
PURPLE = Color(0x8b, 0, 0xff)
RED = Color(0xff, 0, 0)
GREEN = Color(0, 0xff, 0)
BLUE = Color(0, 0, 0xff)
ORANGE = Color(0xff, 0x7f, 0)
LIGHTBLUE = Color(0x4b, 0, 0x82)

# define blocks
RICKY_ORANGE = {"color": ORANGE, "shape": [(0, 1), (1, 1), (2, 1), (2, 0)]}
RICKY_BLUE = {"color": BLUE, "shape": [(0, 0), (0, 1), (1, 1), (2, 1)]}
CLEVELAND_Z = {"color": RED, "shape": [(0, 1), (1, 0), (1, 1), (2, 0)]}
RHODE_ISLAND_Z = {"color": GREEN, "shape": [(0, 1), (1, 0), (1, 1), (2, 0)]}
HERO = {"color": LIGHTBLUE, "shape": [(0, 1), (1, 1), (2, 1), (3, 1)]}
TEEWEE = {"color": PURPLE, "shape": [(0, 1), (1, 0), (1, 1), (2, 1)]}
SMASHBOY = {"color": YELLOW, "shape": [(0, 0), (0, 1), (1, 0), (1, 1)]}

class Tetris(Scene):
    def __init__(self, display):
        super().__init__(display=display)
        self._display.clear()
        self.reset()
        self._framebuf = PixelFramebuffer(self._display, 16, 16)

    def reset(self):
        pass

    def iter(self):
        self._framebuf.pixel(1,1,0xFF0000)
        self._framebuf.display()
