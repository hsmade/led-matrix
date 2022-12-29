import webserver
import game_of_life
import pong
import mario

CODE = None
MAPPING = {
    "game": game_of_life,
    "pong": pong,
    "mario": mario,
}


def set_code(request):
    print("looping over mapping")
    global CODE
    for word, module in MAPPING.items():
        module.STOP = True
        if word in request:
            print("starting module:", word)
            module.STOP = False
            CODE = module


if __name__ == '__main__':
    webserver.connect_network()
    webserver.code_callback = set_code
    while True:
        webserver.poll()
        if CODE:
            print("got CODE, starting it")
            CODE.set_poll(webserver.poll)
            CODE.main()
