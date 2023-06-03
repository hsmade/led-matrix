from neopixel import NeoPixelBackground

if __name__ == "__main__":
    import board
    import rainbowio
    import supervisor
    import time

    NEOPIXEL = board.GP22
    NUM_PIXELS = 256
    pixels = NeoPixelBackground(NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)
    print("starting")
    #while True:
    #    print("cycle")
    #    # Around 1 cycle per second
    #    pixels.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))

    while True:
        for index in range(NUM_PIXELS):
            time.sleep(0.1)
            pixels[index] = (255,0,0)
            if index > 0:
                pixels[index - 1] = (0,0,0)
            else:
                pixels[NUM_PIXELS - 1] = (0,0,0)

