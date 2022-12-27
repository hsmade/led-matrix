import board
from neopixel import Display, Color
from time import sleep


if __name__ == '__main__':
    display = Display(board.GP22, 16, 16, auto_write=False)

    for i in range(16):
        display.set_pixel(i, i, Color(0,32,0))
    display.draw()

    for i in range(16):
        display.set_pixel(i, 15-i, Color(0,0,32))
    display.draw()
    sleep(1)
    display.clear()


