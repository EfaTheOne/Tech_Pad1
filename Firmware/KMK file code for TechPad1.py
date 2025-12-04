import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import Scanner
from kmk.extensions.rgb import RGB, AnimationModes

# set up the keyboard
keyboard = KMKKeyboard()

# --- PIN MAPPING FROM MY PCB ---
# SW1 -> D8
# SW3 -> D5
# SW5 -> D7
# SW6 -> D6
# SW2 -> D10
# SW4 -> D9
# LEDs -> D4

# these are the 6 button pins in the order I want them read
keyboard.col_pins = (
    board.D8,   # SW1 (top left)
    board.D5,   # SW3 (top middle)
    board.D7,   # SW5 (top right)
    board.D6,   # SW6 (bottom left)
    board.D10,  # SW2 (bottom middle)
    board.D9    # SW4 (bottom right)
)

# no rows because each button goes straight to ground
keyboard.row_pins = None
keyboard.diode_orientation = "COL2ROW" 

# custom scanner cause i'm  not using matrix setup
class DirectScanner(Scanner):
    def __init__(self, pins, value_when_pressed=False):
        self.pins = pins
        self.value_when_pressed = value_when_pressed
        self.io_pins = []

        for pin in pins:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.UP
            self.io_pins.append(io)

    def scan(self, keyboard):
        for i, pin in enumerate(self.io_pins):
            is_pressed = (pin.value == self.value_when_pressed)
            keyboard.matrix_update(0, i, is_pressed)

# use the custom scanner instead of default kmk one
keyboard.matrix = DirectScanner(keyboard.col_pins)

# --- KEY LAYOUT ---
# physical layout:
# Q     UP     E
# LEFT   DOWN    RIGHT

keyboard.keymap = [
    [
        KC.Q,      # SW1 (top left)
        KC.UP,     # SW3 (top middle)
        KC.E,      # SW5 (top right)
        KC.LEFT,   # SW6 (bottom left)
        KC.DOWN,   # SW2 (bottom middle)
        KC.RIGHT   # SW4 (bottom right)
    ]
]

# --- RGB LED SETUP ---
rgb = RGB(
    pixel_pin=board.D4,   # LED data pin
    num_pixels=2,
    val_limit=150,
    hue_default=0,
    sat_default=255,
    val_default=150,
    animation_speed=2,
    animation_mode=AnimationModes.RAINBOW_SWIRL
)

keyboard.extensions.append(rgb)

if __name__ == "__main__":
    keyboard.go()
