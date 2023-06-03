import os
import time
import wifi
import socketpool
import microcontroller
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.response import HTTPResponse

server = HTTPServer(socketpool.SocketPool(wifi.radio))
code_callback = None


def poll():
    server.poll()


@server.route("/")
def base(request):  # pylint: disable=unused-argument
    print("serving /")
    return HTTPResponse(content_type="text/html", body=webpage())


@server.route("/", "POST")
def start_code(request):
    print("got POST on /")
    raw_text = request.body.decode("utf8")
    if code_callback:
        code_callback(raw_text)
    return HTTPResponse(content_type="text/html", body=webpage())


def connect_network():
    wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
    print("connected to wifi")
    print("My IP address is", wifi.radio.ipv4_address)
    try:
        server.start(str(wifi.radio.ipv4_address))
    except OSError:
        time.sleep(5)
        print("restarting..")
        microcontroller.reset()
    print("started webserver")


def webpage():
    return f"""
        <!DOCTYPE html>
    <html>
    <body>
    <ul>
        <li><form method="POST"><input name="FFT" type="hidden"/><button type="submit">FFT</button></form></li>
        <li><form method="POST"><input name="game" type="hidden"/><button type="submit">game</button></form></li>
        <li><form method="POST"><input name="pong" type="hidden"/><button type="submit">pong</button></form></li>
        <li><form method="POST"><input name="mario" type="hidden"/><button type="submit">mario</button></form></li>
        <li><form method="POST"><input name="eyes" type="hidden"/><button type="submit">eyes</button></form></li>
        <li><form method="POST"><input name="pacman" type="hidden"/><button type="submit">pacman</button></form></li>
        <li><form method="POST"><input name="cat" type="hidden"/><button type="submit">cat</button></form></li>
    </ul>
    </body>
    </html>
    """
