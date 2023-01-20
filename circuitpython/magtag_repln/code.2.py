import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import secrets
import time
from adafruit_magtag.magtag import MagTag
from adafruit_magtag.graphics import Graphics

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Get our username, key and desired timezone
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]
location = secrets.get("timezone", None)
TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s&tz=%s" % (aio_username, aio_key, location)
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"
MOTHER_PI_URL = "http://192.168.1.253:8080"

print("ESP32-S2 Adafruit IO Time test")

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
            network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % wifi.radio.ping(ipv4))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("Fetching text from", TIME_URL)
response = requests.get(TIME_URL)
print("-" * 40)
print(response.text)
print("-" * 40)

magtag = MagTag()

magtag.add_text(
    #text_font="/fonts/Arial-Bold-12.bdf",
    text_wrap=48,
    text_maxlen=480,
    text_position=(
        (magtag.graphics.display.width // 2),
        (magtag.graphics.display.height // 2) - 10,
    ),
    line_spacing=0.75,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
)

button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)

while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            print("Button %c pressed" % chr((ord("A") + i)))
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])
            magtag.peripherals.play_tone(button_tones[i], 0.25)
            break
    else:
        magtag.peripherals.neopixel_disable = True

    mother_pi_msg_url = MOTHER_PI_URL + "/message.txt"
    print("Fetching text from", mother_pi_msg_url)
    response = requests.get(mother_pi_msg_url)
    print("-" * 40)
    print(response.text)
    print("-" * 40)
    magtag.set_text(response.text)

    time.sleep(240)
