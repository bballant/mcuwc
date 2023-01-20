# common imports
import time
# For display
import board
import displayio
import terminalio
from adafruit_display_text import label
# For network
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import secrets
from adafruit_magtag.magtag import MagTag
from adafruit_magtag.graphics import Graphics

# Set up of wifi #

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
print("Time:" + response.text)

# Set up of

display = board.DISPLAY
time.sleep(display.time_to_refresh)

main_group = displayio.Group()

# white background. Scaled to save RAM
bg_bitmap = displayio.Bitmap(display.width // 8, display.height // 8, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
bg_group = displayio.Group(scale=8)
bg_group.append(bg_sprite)
main_group.append(bg_group)

# show the main group and refresh.
display.show(main_group)

MOTHER_PI_URL = "http://192.168.1.253:8080"
while True:

    # Get weather from server and display it ##################################
    response = requests.get(MOTHER_PI_URL + "/weather.txt")
    weather_text = response.text

    TEXT = "Weather"
    text_area = label.Label(
        terminalio.FONT,
        text=TEXT,
        color=0xFFFFFF,
        background_color=0x666666,
        padding_top=1,
        padding_bottom=3,
        padding_right=4,
        padding_left=4,
    )
    text_area.x = 10
    text_area.y = 14
    main_group.append(text_area)

    another_text = label.Label(
        terminalio.FONT,
        scale=1,
        line_spacing = 1,
        text=weather_text,
        color=0x000000,
        background_color=0xEEEEEE,
        padding_top=1,
        padding_bottom=3,
        padding_right=4,
        padding_left=4,
    )
    # centered
    another_text.anchor_point = (0.5, 0.5)
    another_text.anchored_position = (display.width // 2, display.height // 2 + 5)
    main_group.append(another_text)
    display.refresh()

    time.sleep(240)

    # Get message from server and display it ##################################

    ## pop off previous texts
    main_group.pop()
    main_group.pop()

    response = requests.get(MOTHER_PI_URL + "/message.txt")
    message_text = response.text

    TEXT = "Messages"
    text_area = label.Label(
        terminalio.FONT,
        text=TEXT,
        color=0xFFFFFF,
        background_color=0x666666,
        padding_top=1,
        padding_bottom=3,
        padding_right=4,
        padding_left=4,
    )
    text_area.x = 10
    text_area.y = 14
    main_group.append(text_area)

    another_text = label.Label(
        terminalio.FONT,
        scale=1,
        line_spacing = 1,
        text=message_text,
        color=0x000000,
        background_color=0xEEEEEE,
        padding_top=1,
        padding_bottom=3,
        padding_right=4,
        padding_left=4,
    )
    # centered
    another_text.anchor_point = (0.5, 0.5)
    another_text.anchored_position = (display.width // 2, display.height // 2 + 5)
    main_group.append(another_text)

    display.refresh()

    time.sleep(240)

    ## pop off previous texts before looping around
    main_group.pop()
    main_group.pop()




# import ipaddress
# import ssl
# import wifi
# import socketpool
# import adafruit_requests
# import secrets
# import time
# from adafruit_magtag.magtag import MagTag
# from adafruit_magtag.graphics import Graphics
#
# # Get wifi details and more from a secrets.py file
# try:
#     from secrets import secrets
# except ImportError:
#     print("WiFi secrets are kept in secrets.py, please add them there!")
#     raise
#
# # Get our username, key and desired timezone
# aio_username = secrets["aio_username"]
# aio_key = secrets["aio_key"]
# location = secrets.get("timezone", None)
# TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s&tz=%s" % (aio_username, aio_key, location)
# TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"
# MOTHER_PI_URL = "http://192.168.1.253:8080"
#
# print("ESP32-S2 Adafruit IO Time test")
#
# print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
#
# print("Available WiFi networks:")
# for network in wifi.radio.start_scanning_networks():
#     print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#             network.rssi, network.channel))
# wifi.radio.stop_scanning_networks()
#
# print("Connecting to %s"%secrets["ssid"])
# wifi.radio.connect(secrets["ssid"], secrets["password"])
# print("Connected to %s!"%secrets["ssid"])
# print("My IP address is", wifi.radio.ipv4_address)
#
# ipv4 = ipaddress.ip_address("8.8.4.4")
# print("Ping google.com: %f ms" % wifi.radio.ping(ipv4))
#
# pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl.create_default_context())
#
# print("Fetching text from", TIME_URL)
# response = requests.get(TIME_URL)
# print("-" * 40)
# print(response.text)
# print("-" * 40)
#
# magtag = MagTag()
#
# magtag.add_text(
#     #text_font="/fonts/Arial-Bold-12.bdf",
#     text_wrap=48,
#     text_maxlen=480,
#     text_position=(
#         (magtag.graphics.display.width // 2),
#         (magtag.graphics.display.height // 2) - 10,
#     ),
#     line_spacing=0.75,
#     text_anchor_point=(0.5, 0.5),  # center the text on x & y
# )
#
# button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
# button_tones = (1047, 1318, 1568, 2093)
#
# while True:
#     for i, b in enumerate(magtag.peripherals.buttons):
#         if not b.value:
#             print("Button %c pressed" % chr((ord("A") + i)))
#             magtag.peripherals.neopixel_disable = False
#             magtag.peripherals.neopixels.fill(button_colors[i])
#             magtag.peripherals.play_tone(button_tones[i], 0.25)
#             break
#     else:
#         magtag.peripherals.neopixel_disable = True
#
#     mother_pi_msg_url = MOTHER_PI_URL + "/message.txt"
#     print("Fetching text from", mother_pi_msg_url)
#     response = requests.get(mother_pi_msg_url)
#     print("-" * 40)
#     print(response.text)
#     print("-" * 40)
#     magtag.set_text(response.text)
#
#     time.sleep(240)
