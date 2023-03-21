import storage
import board, digitalio

main_button = digitalio.DigitalInOut(board.A0)
main_button.direction = digitalio.Direction.INPUT
main_button.pull = digitalio.Pull.UP

if main_button.value:
    storage.disable_usb_drive()

