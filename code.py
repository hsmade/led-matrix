import webserver
import game_of_life
import pong
import mario
from neopixel import Display


if __name__ == '__main__':
    scene = None
    mapping = {
        "game": game_of_life,
        "pong": pong,
        "mario": mario,
    }

    def callback(request):
        global scene
        scene = None  # reset to empty as default
        for word, module in mapping.items():
            if word in request:
                print("starting module:", word)
                scene = module.Scene(display=display)

    display = Display(board.GP22, 16, 16, auto_write=False)
    webserver.connect_network()
    webserver.code_callback = callback

    while True:
        webserver.poll()
        if scene is not None:
            scene.iter()
