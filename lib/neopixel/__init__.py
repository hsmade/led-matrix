# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Demonstrate background writing with NeoPixels

The NeoPixelBackground class defined here is largely compatible with the
standard NeoPixel class, except that the ``show()`` method returns immediately,
writing data to the LEDs in the background, and setting `auto_write` to true
causes the data to be continuously sent to the LEDs all the time.

Writing the LED data in the background will allow more time for your
Python code to run, so it may be possible to slightly increase the refresh
rate of your LEDs or do more complicated processing.

Because the pixelbuf storage is also being written out 'live', it is possible
(even with auto-show 'false') to experience tearing, where the LEDs are a
combination of old and new values at the same time.

The demonstration code, under ``if __name__ == '__main__':`` is intended
for the Adafruit MacroPad, with 12 NeoPixel LEDs. It shows a cycling rainbow
pattern across all the LEDs.
"""

import struct
import adafruit_pixelbuf
from rp2pio import StateMachine
from adafruit_pioasm import Program
import time

# Pixel color order constants
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

# NeoPixels are 800khz bit streams. We are choosing zeros as <312ns hi, 936 lo>
# and ones as <700 ns hi, 556 ns lo>.
_program = Program(
    """
.side_set 1 opt
.wrap_target
    pull block          side 0
    out y, 32           side 0      ; get count of NeoPixel bits

bitloop:
    pull ifempty        side 0      ; drive low
    out x 1             side 0 [5]
    jmp !x do_zero      side 1 [3]  ; drive high and branch depending on bit val
    jmp y--, bitloop    side 1 [4]  ; drive high for a one (long pulse)
    jmp end_sequence    side 0      ; sequence is over

do_zero:
    jmp y--, bitloop    side 0 [4]  ; drive low for a zero (short pulse)

end_sequence:
    pull block          side 0      ; get fresh delay value
    out y, 32           side 0      ; get delay count
wait_reset:
    jmp y--, wait_reset side 0      ; wait until delay elapses
.wrap
        """
)


class NeoPixelBackground(  # pylint: disable=too-few-public-methods
    adafruit_pixelbuf.PixelBuf
):
    def __init__(
            self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None
    ):
        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        elif isinstance(pixel_order, tuple):
            order_list = [RGBW[order] for order in pixel_order]
            pixel_order = "".join(order_list)

        byte_count = bpp * n
        bit_count = byte_count * 8
        padding_count = -byte_count % 4

        # backwards, so that dma byteswap corrects it!
        header = struct.pack(">L", bit_count - 1)
        trailer = b"\0" * padding_count + struct.pack(">L", 3840)

        self._sm = StateMachine(
            _program.assembled,
            auto_pull=False,
            first_sideset_pin=pin,
            out_shift_right=False,
            pull_threshold=32,
            frequency=12_800_000,
            **_program.pio_kwargs,
        )

        self._first = True
        super().__init__(
            n,
            brightness=brightness,
            byteorder=pixel_order,
            auto_write=False,
            header=header,
            trailer=trailer,
        )

        self._auto_write = False
        self._auto_writing = False
        self.auto_write = auto_write

    @property
    def auto_write(self):
        return self._auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._auto_write = bool(value)
        if not value and self._auto_writing:
            self._sm.background_write()
            self._auto_writing = False
        elif value:
            self.show()

    def _transmit(self, buf):
        if self._auto_write:
            if not self._auto_writing:
                self._sm.background_write(loop=memoryview(buf).cast("L"), swap=True)
                self._auto_writing = True
        else:
            self._sm.background_write(memoryview(buf).cast("L"), swap=True)


class Color:
    red = 0
    green = 0
    blue = 0

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def get(self):
        return self.red, self.green, self.blue


class Display:
    def __init__(self, pin, width: int, height: int, auto_write=False):
        self.width = width
        self.height = height
        self.__auto_write = auto_write
        self.__pixels = NeoPixelBackground(pin, width * height, brightness=0.1, auto_write=auto_write)
        self.__buffer = [[Color(0, 0, 0)] * width for _ in range(height)]

    @property
    def auto_write(self):
        return self.__auto_write

    def stop(self):
        self.__pixels._sm.deinit()

    def __setitem__(self, index, val):
        color = Color(val[0], val[1], val[2])
        self.set_pixel(index % self.width, index // self.width, color)

    def set_pixel(self, x: int, y: int, color: Color):
        if x > self.width - 1 or y > self.height - 1 or x < 0 or y < 0:
            print("Attempting to set out of bounds pixel at {},{}".format(x, y))
            return
        self.__buffer[x][y] = color
        if x % 2:
            # print("!set x:", x, "y:", y, "index:", (self.height - y) + x * self.height, "to:", color.get())
            self.__pixels[(self.height - (y + 1)) + x * self.height] = color.get()
        else:
            # print("set x:", x, "y:", y, "index:", x + y * self.width, "to:", color.get())
            self.__pixels[y + x * self.height] = color.get()

    def show(self):
        self.__pixels.show()

    def draw(self):
        self.__pixels.show()
        time.sleep(self.height * self.width / 32000)

    def clear(self):
        self.__pixels.fill((0, 0, 0))
        if not self.__auto_write:
            self.draw()

    def print(self, color=True):
        for y in range(self.height):
            for x in range(self.width):
                if color:
                    print(self.__buffer[x][y].get(), end=' ')
                else:
                    if self.__buffer[x][y].get() != (0, 0, 0):
                        print("*", end='  ')
                    else:
                        print(" ", end='  ')
            print()


if __name__ == '__main__':
    import board

    display = Display(board.GP22, 16, 16, auto_write=False)

    for i in range(16):
        display.set_pixel(i, i, Color(32, 0, 0))
    display.draw()

    for i in range(16):
        display.set_pixel(i, 15 - i, Color(0, 0, 32))
    display.draw()
