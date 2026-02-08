import subprocess
from config import SON_PANIER


def play_panier():
    subprocess.Popen(
    ["aplay", SON_PANIER],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )