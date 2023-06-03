import webserver
import game_of_life
import pong
import mario
import eyes
import pacman
import cat
import FFT
import defrag
from neopixel import Display
import board


if __name__ == '__main__':
    mapping = {
        "game": game_of_life.GameOfLife,
        "pong": pong.Pong,
        "mario": mario.Mario,
        "eyes": eyes.Eyes,
        "pacman": pacman.PacMan,
        "cat": cat.Cat,
        "FFT": FFT.FFT,
        "defrag": defrag.Defrag,
    }
    display = Display(board.GP22, 16, 16, auto_write=False)
    # scene = defrag.Defrag(display=display)
    scene = FFT.FFT(display=display)

    def callback(request):
        global scene
        scene = None  # reset to empty as default
        for word, module in mapping.items():
            if word in request:
                print("starting module:", word)
                scene = module(display=display)

    webserver.connect_network()
    webserver.code_callback = callback

    while True:
        webserver.poll()
        if scene is not None:
            scene.iter()
