from neopixel import Display


class Scene:
    def __init__(self, display: Display):
        # set the display allocation to use
        self._display = display

    def iter(self):
        """
        iter runs one iteration of the scene.
        This allows the calling code to handle other things in between them
        :return:
        """
        pass
