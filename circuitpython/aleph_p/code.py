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

IMAGES = [
    "/images/a001.bmp",
    "/images/a002.bmp",
    "/images/a003.bmp",
    "/images/a004.bmp",
    "/images/a005.bmp",
    "/images/a006.bmp",
    "/images/a007.bmp",
    "/images/a008.bmp",
    "/images/a009.bmp",
    "/images/a010.bmp",
    "/images/a011.bmp",
    "/images/a012.bmp",
    "/images/a013.bmp",
    "/images/a014.bmp",
    "/images/a015.bmp",
    "/images/a016.bmp",
    "/images/a017.bmp",
    "/images/a018.bmp",
    "/images/a019.bmp",
    "/images/a020.bmp",
    "/images/a021.bmp",
    "/images/a022.bmp",
    "/images/a023.bmp",
    "/images/a024.bmp",
    "/images/a025.bmp",
    "/images/a026.bmp",
    "/images/a027.bmp",
    "/images/a028.bmp",
    "/images/a029.bmp",
    "/images/a030.bmp",
    "/images/a031.bmp",
    "/images/a032.bmp",
    "/images/a033.bmp",
    "/images/a034.bmp",
    "/images/a035.bmp",
    "/images/a036.bmp",
    "/images/a037.bmp",
    "/images/a038.bmp",
    "/images/a039.bmp",
    "/images/a040.bmp",
    "/images/a041.bmp",
    "/images/a042.bmp",
    "/images/a043.bmp",
    "/images/a044.bmp",
    "/images/a045.bmp",
    "/images/a046.bmp",
    "/images/a047.bmp",
    "/images/a048.bmp",
    "/images/a049.bmp",
    "/images/a050.bmp",
    "/images/a051.bmp",
    "/images/a052.bmp",
    "/images/a053.bmp",
    "/images/a054.bmp",
    "/images/a055.bmp",
    "/images/a056.bmp",
    "/images/a057.bmp",
    "/images/a058.bmp",
    "/images/a059.bmp",
    "/images/a060.bmp",
    "/images/a061.bmp",
    "/images/a062.bmp",
    "/images/a063.bmp",
    "/images/a064.bmp",
    "/images/a065.bmp",
    "/images/a066.bmp",
    "/images/a067.bmp",
    "/images/a068.bmp",
    "/images/a069.bmp",
    "/images/a070.bmp",
    "/images/a071.bmp",
    "/images/a072.bmp",
    "/images/a073.bmp",
    "/images/a074.bmp",
    "/images/a075.bmp",
    "/images/a076.bmp",
    "/images/a077.bmp",
    "/images/a078.bmp",
    "/images/a079.bmp",
    "/images/a080.bmp",
    "/images/a081.bmp",
    "/images/a082.bmp",
    "/images/a083.bmp",
    "/images/a084.bmp",
    "/images/a085.bmp",
    "/images/a086.bmp",
    "/images/a087.bmp",
    "/images/a088.bmp",
    "/images/a089.bmp",
    "/images/a090.bmp",
    "/images/a091.bmp",
    "/images/a092.bmp",
    "/images/a093.bmp",
    "/images/a094.bmp",
    "/images/a095.bmp",
    "/images/a096.bmp",
    "/images/a097.bmp",
    "/images/a098.bmp",
    "/images/a099.bmp",
    "/images/a100.bmp",
    "/images/a101.bmp",
    "/images/a102.bmp",
    "/images/a103.bmp",
    "/images/a104.bmp",
    "/images/a105.bmp",
    "/images/a106.bmp",
    "/images/a107.bmp",
    "/images/a108.bmp",
    "/images/a109.bmp",
    "/images/a110.bmp",
    "/images/a111.bmp",
    "/images/a112.bmp",
    "/images/a113.bmp",
    "/images/a114.bmp",
    "/images/a115.bmp",
    "/images/a116.bmp",
    "/images/a117.bmp",
    "/images/a118.bmp",
    "/images/a119.bmp",
    "/images/a120.bmp",
    "/images/a121.bmp",
    "/images/a122.bmp",
    "/images/a123.bmp",
    "/images/a124.bmp",
    "/images/a125.bmp",
    "/images/a126.bmp",
    "/images/a127.bmp",
    "/images/a128.bmp",
    "/images/a129.bmp",
    "/images/a130.bmp",
    "/images/a131.bmp",
    "/images/a132.bmp",
    "/images/a133.bmp",
    "/images/a134.bmp",
    "/images/a135.bmp",
    "/images/a136.bmp",
    "/images/a137.bmp",
    "/images/a138.bmp",
    "/images/a139.bmp",
    "/images/a140.bmp",
    "/images/a141.bmp",
    "/images/a142.bmp",
    "/images/a143.bmp",
    "/images/a144.bmp",
    "/images/a145.bmp",
    "/images/a146.bmp",
    "/images/a147.bmp",
    "/images/a148.bmp",
    "/images/a149.bmp",
    "/images/a150.bmp",
    "/images/a151.bmp",
    "/images/a152.bmp",
    "/images/a153.bmp",
    "/images/a154.bmp",
    "/images/a155.bmp",
    "/images/a156.bmp",
    "/images/a157.bmp",
    "/images/a158.bmp",
    "/images/a159.bmp",
    "/images/a160.bmp",
    "/images/a161.bmp",
    "/images/a162.bmp",
    "/images/a163.bmp",
    "/images/a164.bmp",
    "/images/a165.bmp",
    "/images/a166.bmp",
    "/images/a167.bmp",
    "/images/a168.bmp",
    "/images/a169.bmp",
    "/images/a170.bmp",
    "/images/a171.bmp",
    "/images/a172.bmp",
    "/images/a173.bmp",
    "/images/a174.bmp",
    "/images/a175.bmp",
    "/images/a176.bmp",
    "/images/a177.bmp",
    "/images/a178.bmp",
    "/images/a179.bmp",
    "/images/a180.bmp",
    "/images/a181.bmp",
    "/images/a182.bmp",
    "/images/a183.bmp",
    "/images/a184.bmp",
    "/images/a185.bmp",
    "/images/a186.bmp",
    "/images/a187.bmp",
    "/images/a188.bmp",
]

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
        self.on = True
    def turn_off(self):
        self.on = False
        self.led.value = True
    def turn_on(self):
        self.on = True
    def update(self):
        if not(self.on):
            return
        if (self.init_tim + self.ms) <= time.monotonic():
            self.led.value = not(self.led.value)
            self.init_tim = time.monotonic()

class DisplayState():
    GALLERY = 1
    def __init__(self, group, ms):
        self.group = group
        self.curr_state = DisplayState.GALLERY
        self.stack_size = 0
        self.idx = 0
        self.init_tim = time.monotonic()
        self.ms = ms
    def inc_stack(self):
        self.stack_size = self.stack_size + 1
    def reset_group(self):
        for i in range(self.stack_size):
            self.group.pop()
        self.stack_size = 0
    def show_image(self):
        self.reset_group()
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(IMAGES[self.idx])
        self.group.append(displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader))
        self.inc_stack()
    def init_image(self):
        self.show_image()
        self.idx = self.idx + 1
    def update(self):
        if self.curr_state == DisplayState.GALLERY and \
           (self.init_tim + self.ms) <= time.monotonic():
            if self.idx == len(IMAGES):
                self.idx = 0
            self.show_image()
            self.idx = self.idx + 1
            self.init_tim = time.monotonic()

displayio.release_displays()
i2c = board.I2C()  # uses board.SCL and board.SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

game_state = DisplayState(splash, 15)
game_state.init_image()
waitForClick(switch)

led_state = LedState(led, .5)
led_state.turn_off()

while True:
    led_state.update()
    game_state.update()
