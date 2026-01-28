import RPi.GPIO as GPIO
import threading
import time
from config import GPIO_LED_PANIER, GPIO_LED_MATCH


def blink_panier():
def _blink():
GPIO.output(GPIO_LED_PANIER, GPIO.HIGH)
time.sleep(0.15)
GPIO.output(GPIO_LED_PANIER, GPIO.LOW)
threading.Thread(target=_blink, daemon=True).start()


def match_on():
GPIO.output(GPIO_LED_MATCH, GPIO.HIGH)


def match_off():
GPIO.output(GPIO_LED_MATCH, GPIO.LOW)