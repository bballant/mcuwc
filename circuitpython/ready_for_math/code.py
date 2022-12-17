# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT


# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import random
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from rainbowio import colorwheel
import adafruit_dotstar
import digitalio
from adafruit_debouncer import Debouncer

def waitForClick(swch):
    swch.update()
    while not(swch.value):
        swch.update()
    while (swch.value):
        swch.update()

displayio.release_displays()

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 58, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)

# Draw a label
text = "Ready"
splash.append(label.Label(terminalio.FONT,
                          text=text,
                          color=0xFFFF00,
                          x=34,
                          y=15,
                          scale=2))

text = "for Math?"
splash.append(label.Label(terminalio.FONT,
                          text=text,
                          color=0xFFFF00,
                          x=10,
                          y=41,
                          scale=2))

pin = digitalio.DigitalInOut(board.D12)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led.brightness = 0.3
i = 0
while True:

    waitForClick(switch)

    splash.pop()
    splash.pop()

    #print(switch.value)
    i = (i + 10) % 256  # run from 0 to 255
    led.fill(colorwheel(i))
    time.sleep(0.01)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 58, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
    splash.append(inner_sprite)

    x = random.randint(2, 12)
    y = random.randint(2, 12)
    # Draw a label
    text = str(x) + " x " + str(y)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=25, scale=2)
    splash.append(text_area)

    waitForClick(switch)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 58, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
    splash.append(inner_sprite)

    # Draw a label
    text = str(x * y)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=50, y=30, scale=2)
    splash.append(text_area)
