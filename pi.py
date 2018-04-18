import RPi.GPIO as GPIO
import time
import urllib3
import requests
import sys
import spidev
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 1000000
spi.bits_per_word = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(22,GPIO.IN)
GPIO.setwarnings(False)


def API_Get_Button():
    if not GPIO.input(22): # RED Button
        return "R"
    if not GPIO.input(18): # GREEN Button
        return "G"
    if not GPIO.input(16): # YELLOW Button pressed
        return "Y"
    return None

# def API_Get_Button():
#     return input()


while True:
    colour = API_Get_Button()
    if colour:
        client = requests.session()
        #print(colour, "button pressed")
        url = 'http://www.eeslibrary.com:8000/off/'+colour+'/'
        r2 = client.get(url)
        #print(colour, "web requested")
        time.sleep(0.3)
