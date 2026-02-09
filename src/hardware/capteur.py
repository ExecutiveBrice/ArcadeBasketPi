import time
from config import DELAI_MIN_PANIER
from core import state
from hardware.leds import blink_panier
from hardware.son import play_panier

last_hit = 0

def on_panier(channel):
    global last_hit
    now = time.time()

    if now - last_hit < DELAI_MIN_PANIER:
        return

    if not state.state["running"]:
        return

    last_hit = now
    state.add_point()
    blink_panier()
    play_panier()