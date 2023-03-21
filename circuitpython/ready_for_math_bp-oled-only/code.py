import random
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import digitalio
from adafruit_debouncer import Debouncer
import adafruit_character_lcd.character_lcd as characterlcd

def waitForClick(swch):
    swch.update()
    while not(swch.value):
        swch.update()
    while (swch.value):
        swch.update()

pin = digitalio.DigitalInOut(board.A0)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

class LedState():
    def __init__(self, _led, _ms):
        self.led = _led
        self.init_tim = time.monotonic()
        self.ms = _ms
    def update(self):
        if (self.init_tim + self.ms) <= time.monotonic():
            self.led.value = not(self.led.value)
            self.init_tim = time.monotonic()

class GameState():
    INTRO = 1
    QUESTION = 2
    ANSWER = 3
    DONE = 4
    def __init__(self, group):
        self.group = group
        self.curr_state = GameState.INTRO
        self.stack_size = 0
        self.x = 0
        self.y = 0
        self.count = 0
    def inc_stack(self):
        self.stack_size = self.stack_size + 1
    def reset_group(self):
        for i in range(self.stack_size):
            self.group.pop()
            self.stack_size = 0
    def new_message(self, message):
        pass
    def show_intro(self):
        self.reset_group()
        self.new_message("Be Brave!")
        # Draw a label
        text = "Ready"
        self.group.append(label.Label(terminalio.FONT,
                                      text=text,
                                      color=0xFFFF00,
                                      x=34,
                                      y=15,
                                      scale=2))

        self.inc_stack()
        text = "for Math?"
        self.group.append(label.Label(terminalio.FONT,
                                      text=text,
                                      color=0xFFFF00,
                                      x=10,
                                      y=41,
                                      scale=2))
        self.inc_stack()
    def reset_question(self):
        self.x = random.randint(2, 12)
        self.y = random.randint(2, 12)
    def show_next_question(self):
        self.new_message("Onward!")
        self.reset_question()
        self.reset_group()
        text = str(self.x) + " x " + str(self.y)
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=25, scale=2)
        splash.append(text_area)
        self.inc_stack()
    def show_next_answer(self):
        self.new_message("You Got It!")
        self.reset_group()
        text = str(self.x * self.y)
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=50, y=30, scale=2)
        splash.append(text_area)
        time.sleep(0.2)
        self.inc_stack()
    def update(self):
        if self.curr_state != GameState.DONE:
            if self.curr_state == GameState.INTRO:
                self.show_next_question()
                self.curr_state = GameState.QUESTION
            elif self.curr_state == GameState.QUESTION:
                self.show_next_answer()
                self.curr_state = GameState.ANSWER
            elif self.curr_state == GameState.ANSWER:
                self.show_next_question()
                self.curr_state = GameState.QUESTION
                self.count = self.count + 1


displayio.release_displays()
i2c = board.I2C()  # uses board.SCL and board.SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

# set-up display border
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

game_state = GameState(splash)
game_state.show_intro()
waitForClick(switch)
game_state.update()

led_state = LedState(led, .5)

while True:
    switch.update()
    led_state.update()
    if switch.rose:
        game_state.update()
