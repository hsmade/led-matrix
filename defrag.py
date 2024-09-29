from neopixel import Color
from time import sleep
from scene import Scene
import random

MAX_OCCUPATION = 0.5
MAX_FILE_SIZE = 8
BRIGHTNESS = 0.5
EMPTY = Color(0, 0, 0)
UNPROCESSED = Color(0, 255 * BRIGHTNESS, 255 * BRIGHTNESS)  # CYAN
READ = Color(0, 255 * BRIGHTNESS, 0)  # READ
WRITE = Color(255 * BRIGHTNESS, 0, 0)  # WRITE
PROCESSED = Color(0, 0, 250 * BRIGHTNESS)  # BLUE
ACTION_SLEEP = 0.2


class Defrag(Scene):
    data = []
    position = 0
    file_sizes = {}

    def __init__(self, display):
        super().__init__(display=display)
        self.prefill()

    def prefill(self):
        self._display.clear()
        # matrix size is 16 * 16 = 256
        display_size = self._display.height * self._display.width
        files = []

        # create files
        while sum(files) < MAX_OCCUPATION * display_size:
            files.append(random.randint(1, MAX_FILE_SIZE))
            self.file_sizes[len(files)] = files[-1]
        # print("files: {}".format(files))

        for y in range(self._display.height):
            for x in range(self._display.width):
                if random.randint(1, display_size) < MAX_OCCUPATION * display_size:  # do we write a pixel?
                    # print("write pixel: {}, {}".format(x, y))
                    # select a non-empty file to write
                    while sum(files) > 0:
                        test_index = random.randint(0, len(files) - 1)
                        if files[test_index] > 0:
                            index = test_index
                            # print("write file {}".format(index))
                            break
                    self._display.set_pixel(x, y, UNPROCESSED)
                    files[index] -= 1
                    self.data.append(index + 1)
                else:
                    self.data.append(0)
        # print("draw")
        self._display.draw()

    def get_location_from_pos(self, pos):
        y = pos // self._display.width
        x = pos - (y * self._display.width)
        return x, y

    def number_of_empty_before(self):
        if self.position == 0:  # we're at the start
            return 0

        offset = 1
        while True:
            if self.position - offset == 0:  # we're at the start
                # print("found {} empty spaces before".format(offset))
                return offset
            if self.data[self.position - offset] != 0:  # end of empty blocks
                # print("found {} empty spaces before".format(offset))
                return offset - 1  # current offset isn't empty
            offset += 1

    def find_empty_space_after(self, pos):
        offset = 1
        # fixme: index out of bounds on self.data
        while self.data[pos + offset] != 0:
            offset += 1
        # print("found empty space at {}".format(pos + offset))
        return pos + offset

    def read(self, pos):
        # print("read pos {}".format(pos))
        self.data[pos] = 0
        x, y = self.get_location_from_pos(pos)
        self._display.set_pixel(x, y, READ)
        self._display.draw()
        sleep(ACTION_SLEEP)
        self._display.set_pixel(x, y, EMPTY)
        self._display.draw()

    def write(self, pos, file_number):
        # print("write pos {}".format(pos))
        self.data[pos] = file_number
        x, y = self.get_location_from_pos(pos)
        self._display.set_pixel(x, y, WRITE)
        self._display.draw()
        sleep(ACTION_SLEEP)
        self._display.set_pixel(x, y, UNPROCESSED)
        self._display.draw()

    def mark_as_done(self, pos):
        # print("mark pos {}".format(pos))
        x, y = self.get_location_from_pos(pos)
        self._display.set_pixel(x, y, PROCESSED)
        self._display.draw()
        sleep(ACTION_SLEEP/2)

    def iter(self):
        display_size = self._display.height * self._display.width

        # if defrag is done
        if self.position == display_size:
            # print("prefill")
            self.prefill()
            self.position = 0

        if self.data[self.position] == 0:
            # print("skip empty pos {}".format(self.position))
            self.position += 1
            return

        current_file = self.data[self.position]
        # print("working on file {} at pos {} with size {}".format(current_file, self.position, self.file_sizes[current_file]))
        # create empty space
        empty_before = self.number_of_empty_before()
        size_needed = self.file_sizes[current_file] - empty_before
        # print("need {} empty space".format(size_needed))
        # free up space in front of us
        for offset in range(0, size_needed):
            test_pos = self.position + offset
            if self.data[test_pos] != 0:
                # print("moving block at pos {}".format(test_pos))
                empty_space = self.find_empty_space_after(self.position + size_needed)
                file_number = self.data[test_pos]
                self.read(test_pos)
                self.write(empty_space, file_number)
            # else:
            #     print("space is already empty at pos {}".format(self.position + offset))

        # find all blocks for file and write them to the now empty space
        # print("write file number {}".format(current_file))
        offset = 0
        empty_offset = 0 - empty_before  # set to start of empty space
        written = 0
        while written < self.file_sizes[current_file] and self.position + offset < display_size:
            if self.data[self.position + offset] == current_file:  # found a block
                self.read(self.position + offset)
                self.write(self.position + empty_offset, current_file)
                self.data[self.position + empty_offset] = current_file
                empty_offset += 1
                written += 1
            offset += 1

        # advance forward to end of file
        # print("move forward {}".format(size_needed))
        # print("loop from offset {} to {}".format(0 - empty_before, self.file_sizes[current_file] - empty_before))
        orig_pos = self.position
        for offset in range(0 - empty_before, self.file_sizes[current_file] - empty_before):
            # print("at offset {}".format(offset))
            self.position = orig_pos + offset
            if self.data[self.position] != 0:
                self.mark_as_done(self.position)

        # next block
        self.position += 1
        sleep(ACTION_SLEEP)
