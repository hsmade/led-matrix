# LED matrix controller

This software runs on a Raspberry Pico W, with [CircuitPython 8.0.0-beta.6](https://circuitpython.org/board/raspberry_pi_pico_w/).

Expects a `settings.toml` file like this:

```toml
WIFI_PASSWORD="my password"
WIFI_SSID="SSID to connect to"
```
to connect to the WIFI. Then serves a simple web page on port 80.

You can enable the built-in web IDE and such, as long as it runs on a different port.
In `settings.toml`
```toml
# To auto-connect to Wi-Fi
CIRCUITPY_WIFI_SSID="scottswifi"
CIRCUITPY_WIFI_PASSWORD="secretpassword"

# To enable modifying files from the web. Change this too!
# Leave the User field blank in the browser.
CIRCUITPY_WEB_API_PASSWORD="passw0rd"

CIRCUITPY_WEB_API_PORT=81

```
Remember to put strings in quotes, or they won't work.

