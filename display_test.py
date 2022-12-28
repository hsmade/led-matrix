import board
from neopixel import Display, Color
from time import sleep

if __name__ == '__main__':
    display = Display(board.GP22, 16, 16, auto_write=False)

    # for i in range(16):
    #     display.set_pixel(i, i, Color(0, 32, 0))
    # display.draw()
    #
    # for i in range(16):
    #     display.set_pixel(i, 15 - i, Color(0, 0, 32))
    # display.draw()
    # display.print(color=False)
    # sleep(1)
    # display.clear()

    x = y = old_x = old_y = 0
    yp = 1
    while True:
        display.set_pixel(int(old_x), old_y, Color(0, 0, 0))
        display.set_pixel(int(x), y, Color(32, 32, 32))
        old_x = x
        old_y = y
        x += 0.5
        y += yp
        if y >14:
            yp=-1
        display.draw()
        display.print(color=False)
