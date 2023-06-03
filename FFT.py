from board import A0
from analogio import AnalogIn
from scene import Scene
from time import sleep
from ulab import numpy as np
from ulab.utils import spectrogram
from math import log
from array import array
from time import monotonic, monotonic_ns
from rainbowio import colorwheel
from gc import mem_free
from neopixel import Color


def wheel_to_color(rgb_int):
    blue = rgb_int & 255
    green = (rgb_int >> 8) & 255
    red = (rgb_int >> 16) & 255
    return Color(red, green, blue)


def sample(sensor, samples):
    sample_rate = 44100
    sampling_interval = 1000000000 / sample_rate
    next_sample_time = monotonic_ns()

    for i in range(len(samples)):
        now = monotonic_ns()
        if now >= next_sample_time:
            next_sample_time += sampling_interval
            samples[i] = sensor.value


# https://learn.adafruit.com/mini-led-matrix-audio-visualizer/code-the-audio-spectrum-light-show

a0 = AnalogIn(A0)
fft_size = 256  # 256  # Sample size for Fourier transform, MUST be power of two
# freq width per bin = 44100 / fft_size (256 -> 172.27)
spectrum_size = fft_size // 2  # Output spectrum is 1/2 of FFT result
# Bottom of spectrum tends to be noisy, while top often exceeds musical
# range and is just harmonics, so clip both ends off:
low_bin = 3  # fft_size(256) -> 172 Hz
high_bin = 75  # fft_size(256) -> 12920 Hz

display_width = 16
display_height = 16

# To keep the display lively, tables are precomputed where each column of
# the matrix (of which there are few) is the sum value and weighting of
# several bins from the FFT spectrum output (of which there are many).
# The tables also help visually linearize the output so octaves are evenly
# spaced, as on a piano keyboard, whereas the source spectrum data is
# spaced by frequency in Hz.
column_table = []
spectrum_bits = log(spectrum_size, 2)  # e.g. 7 for 128-bin spectrum
# Scale low_bin and high_bin to 0.0 to 1.0 equivalent range in spectrum
low_frac = log(low_bin, 2) / spectrum_bits
frac_range = log(high_bin, 2) / spectrum_bits - low_frac
print("low_frac:", low_frac, "frac_range:", frac_range)


for column in range(display_width):
    print("column:", column)
    # Determine the lower and upper frequency range for this column, as
    # fractions within the scaled 0.0 to 1.0 spectrum range. 0.95 below
    # creates slight frequency overlap between columns, looks nicer.
    lower = low_frac + frac_range * (column / display_width * 0.95)
    upper = low_frac + frac_range * ((column + 1) / display_width)
    mid = (lower + upper) * 0.5
    half_width = (upper - lower) * 0.5
    print("Lower:", lower, "upper:", upper)
    # Map fractions back to spectrum bin indices that contribute to column
    first_bin = int(2 ** (spectrum_bits * lower) + 1e-4)
    # print("first_bin:", first_bin)
    last_bin = int(2 ** (spectrum_bits * upper) + 1e-4)
    # print("last_bin", last_bin)
    bin_weights = list()
    print("first_bin:", first_bin, "last_bin:", last_bin)
    for bin_index in range(first_bin, last_bin + 1):
        # bin_weights.append(1/(last_bin + 1 - first_bin))  # weigh all bins evenly
    #     # Find distance from column's overall center to individual bin's
    #     # center, expressed as 0.0 (bin at center) to 1.0 (bin at limit of
    #     # lower-to-upper range).
        bin_center = log(bin_index + 0.5, 2) / spectrum_bits
        dist = abs(bin_center - mid) / half_width
        if dist < 1.0:
            # Bin weights have a cubic falloff curve within range:
            dist = 1.0 - dist
            bin_weights.append(((3.0 - (dist * 2.0)) * dist) * dist)

    # Scale bin weights so total is 1.0 for each column, but then mute
    # lower columns slightly and boost higher columns. It graphs better.
    total = sum(bin_weights)
    bin_weights = [
        (weight / total) * (0.8 + idx / display_width * 1.4)
        for idx, weight in enumerate(bin_weights)
    ]

    # List w/five elements is stored for each column:
    # 0: Index of the first spectrum bin that impacts this column.
    # 1: A list of bin weights, starting from index above, length varies.
    # 2: Color for drawing this column on the LED matrix. The 225 is on
    #    purpose, providing hues from red to purple, leaving out magenta.
    # 3: Current height of the 'falling dot', updated each frame
    # 4: Current velocity of the 'falling dot', updated each frame
    column_table.append([
        first_bin - low_bin,
        bin_weights,
        colorwheel(225 * column / display_width),
        display_width,
        0.0,
    ])
    # print("mem free after column_table update:", mem_free())

# print(column_table)


class FFT(Scene):
    dynamic_level = 14
    frames, start_time = 0, monotonic()

    def iter(self):
        samples_bit = array('H', [0] * fft_size)
        sample(a0, samples_bit)
        samples = np.array(samples_bit)

        # Compute spectrogram and trim results. Only the left half is
        # normally needed (right half is mirrored), but we trim further as
        # only the low_bin to high_bin elements are interesting to graph.
        spectrum = spectrogram(samples)[low_bin: high_bin + 1]  # cut off lower and higher freqs
        # print("spectrum size:", len(spectrum))
        # Linearize spectrum output. spectrogram() is always nonnegative,
        # but add a tiny value to change any zeros to nonzero numbers
        # (avoids rare 'inf' error)
        spectrum = np.log(spectrum + 1e-7)
        # Determine minimum & maximum across all spectrum bins, with limits
        lower = max(np.min(spectrum), 4)
        upper = min(max(np.max(spectrum), lower + 6), 15)

        # for index, value in enumerate(spectrum):
        #     print(int(value / (upper/10))* "*")
        # return sleep(1)

        # Adjust dynamic level to current spectrum output, keeps the graph
        # 'lively' as ambient volume changes. Sparkle but don't saturate.
        # if upper > self.dynamic_level:
        #     self.dynamic_level = upper * 0.7 + self.dynamic_level * 0.3
        # else:
        #     self.dynamic_level = self.dynamic_level * 0.5 + lower * 0.5
        # print("dyn level:", self.dynamic_level)

        # Apply vertical scale to spectrum data. Results may exceed
        # matrix height...that's OK, adds impact!
        # data = (spectrum - lower) * (7 / (dynamic_level - lower))
        data = (spectrum - lower) * ((display_height + 2) / (self.dynamic_level - lower))
        # data is now a list of levels per freq

        for column, element in enumerate(column_table):
            # Start BELOW matrix and accumulate bin weights UP, saves math
            # print("column:", column)
            # print("data:", data[column])
            first_bin = element[0]
            column_top = display_height + 1
            for bin_offset, weight in enumerate(element[1]):  # bin_weights
            #     print("offset:", bin_offset, "weight:", weight, "results in index:", first_bin + bin_offset)
                column_top -= data[first_bin + bin_offset] * weight  # index out of bounds
            # bin_total = 0
            # for bin_offset in range(high_bin/display_width):
            #     bin_total += data[first_bin+bin_offset]

            # column_top -= bin_total / (high_bin/display_width)  # average of all selected bins
            if column_top < element[3]:
                element[3] = column_top - 0.5
                element[4] = 0
            else:
                element[3] += element[4]
                element[4] += 0.2
            column_top = int(column_top)

            for row in range(column_top):  # Erase area above column
                if row > display_height - 1:  # limit
                    continue
                self._display.set_pixel(column, row, Color(0, 0, 0))
            for row in range(column_top, display_height):  # Draw column
                if row > display_height - 1 or row < 0:  # limit
                    continue
                self._display.set_pixel(column, row, wheel_to_color(element[2]))
            if int(element[3]) > display_height - 1:
                element[3] = display_height - 1
            # Draw peak dot
            # self._display.set_pixel(column, int(element[3]), Color(0xE0, 0x80, 0x80))

            self._display.draw()
            self.frames += 1
            # print(self.frames / (monotonic() - self.start_time), "FPS")

        # sleep(1)
