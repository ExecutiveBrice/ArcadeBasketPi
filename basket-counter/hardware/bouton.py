import time
from config import ANTI_REBOND_BOUTON
from core import state
from hardware.leds import match_on

last_press = 0

def on_reset(channel):
    global last_press
    now = time.time()

    if now - last_press < ANTI_REBOND_BOUTON:
        return

    state.start_match()
    match_on()
    last_press = now