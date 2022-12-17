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
import digitalio
from adafruit_debouncer import Debouncer
import adafruit_character_lcd.character_lcd as characterlcd

def waitForClick(swch):
    swch.update()
    while not(swch.value):
        swch.update()
    while (swch.value):
        swch.update()

lcd_rs = digitalio.DigitalInOut(board.A0)
lcd_en = digitalio.DigitalInOut(board.A1)
lcd_d7 = digitalio.DigitalInOut(board.B9)
lcd_d6 = digitalio.DigitalInOut(board.B8)
lcd_d5 = digitalio.DigitalInOut(board.A15)
lcd_d4 = digitalio.DigitalInOut(board.A9)

lcd_columns = 16
lcd_rows = 2
main_lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

pin = digitalio.DigitalInOut(board.B3)
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

class LcdState():
    def __init__(self, lcd, game_state):
        self.lcd = lcd
        self.game_state = game_state
        self.init_tim = time.monotonic()
        self.phase = 0
    def new_message(self, new_phase, message):
        self.lcd.message = "                \n                 "
        self.lcd.message = message
        self.phase = new_phase
    def phase_check(self, phase):
        return time.monotonic() >= self.init_tim + phase and self.phase < phase
    def update(self):
        if self.phase_check(20): # 20 secs
            self.new_message(20, "20 Seconds!\nKilling It!")
        elif self.phase_check(30):
            self.new_message(30, "30 Seconds!")
        elif self.phase_check(31):
            self.new_message(31," ")
        elif self.phase_check(32):
            self.new_message(32, "30 Seconds!")
        elif self.phase_check(33):
            self.new_message(33, " ")
        elif self.phase_check(34):
            self.new_message(34, "30 Seconds!")
        elif self.phase_check(35):
            self.new_message(35, "")
        elif self.phase_check(36):
            self.new_message(36, "Don't Stop Now!")
        elif self.phase_check(45):
            self.new_message(45, "15 More Seconds!")
        elif self.phase_check(55):
            self.new_message(55, "Five!")
        elif self.phase_check(56):
            self.new_message(56, "Four!")
        elif self.phase_check(57):
            self.new_message(57, "Three!")
        elif self.phase_check(58):
            self.new_message(58, "Two!")
        elif self.phase_check(59):
            self.new_message(59, "One!")
        elif self.phase_check(60):
            self.new_message(60, "Wow!! You Did\n" + str(game_state.count) + " Questions!")
            self.game_state.curr_state = GameState.DONE

class GameState():
    INTRO = 1
    QUESTION = 2
    ANSWER = 3
    DONE = 4
    def __init__(self, group, lcd):
        self.group = group
        self.lcd = lcd
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
        self.lcd.message = "                \n                "
        self.lcd.message = message
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
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
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

game_state = GameState(splash, main_lcd)
game_state.show_intro()
waitForClick(switch)
game_state.update()

lcd_state = LcdState(main_lcd, game_state)
led_state = LedState(led, .5)

while True:
    switch.update()
    led_state.update()
    lcd_state.update()
    if switch.rose:
        game_state.update()
