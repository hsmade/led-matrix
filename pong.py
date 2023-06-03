from neopixel import Color
import random
from time import sleep
from scene import Scene


class Ball:
    x = 0
    y = 0
    right = None
    up = None

    def __init__(self, display: Display, color=Color(32, 32, 32)):
        self.__display = display
        self.color = color
        self.reset()

    def reset(self):
        self.x = random.randint(7, 8)
        self.y = random.randint(0, 15)
        self.right = bool(random.getrandbits(1))
        self.up = bool(random.getrandbits(1))

    def move(self):
        self.clear()
        if self.up and self.y < 1 or not self.up and self.y > 14:
            self.x += int(random.randrange(-1, 1))
            self.up = not self.up
        if self.right and self.x > 14 or not self.right and self.x < 1:
            self.y += int(random.randrange(-1, 1))
            self.right = not self.right
        if self.right:
            self.x += 1
        else:
            self.x -= 1
        if self.up:
            self.y -= 1
        else:
            self.y += 1
        self.__display.set_pixel(self.x, self.y, self.color)

    def clear(self):
        self.__display.set_pixel(self.x, self.y, Color(0, 0, 0))

    def bounce(self):
        self.right = not self.right
        self.up = not self.up


class Bar:
    y = 0

    def __init__(self, display, x: int, size=3, color=Color(32, 32, 32)):
        self.__display = display
        self.color = color
        self.x = x
        self.size = size

    def move(self, ball: Ball):
        self._draw(True)
        if ball.right is (self.x == 15):
            if ball.y > self.y:
                self.y += 0.9
            if ball.y < self.y:
                self.y -= 0.9
            if self.y < 0:
                self.y = 0
            if self.y + self.size > 15:
                self.y = 15 - self.size
        self._draw()

    def _draw(self, clear=False):
        for offset in range(self.size):
            if clear:
                self.__display.set_pixel(self.x, int(self.y+offset), Color(0, 0, 0))
            else:
                self.__display.set_pixel(self.x, int(self.y+offset), self.color)

    def touches(self, ball: Ball):
        return self.y-1 <= ball.y <= (self.y + (self.size - 1))

    def blink(self):
        for _ in range(2):
            self._draw(True)
            self.__display.draw()
            sleep(0.3)
            self._draw()
            self.__display.draw()
            sleep(0.3)


class Pong(Scene):
    def __init__(self, display):
        super().__init__(display=display)
        self.bar_left = Bar(display=self._display, x=0, color=Color(32, 0, 0))
        self.bar_right = Bar(display=self._display, x=15, color=Color(0, 32, 0))
        self.ball = Ball(display=self._display, color=Color(32, 0, 32))

    def iter(self):
        self.bar_left.move(self.ball)
        self.bar_right.move(self.ball)
        self.ball.move()

        if self.ball.x == 1 or self.ball.x == 14:
            # print("touch?")
            if self.bar_left.touches(self.ball) or self.bar_right.touches(self.ball):
                # print("touched!")
                self.ball.bounce()

        if self.ball.x == 0:
            self.bar_left.blink()
            self.ball.clear()
            self.ball.reset()
        if self.ball.x == 15:
            self.bar_right.blink()
            self.ball.clear()
            self.ball.reset()

        self._display.draw()
        sleep(0.08)
