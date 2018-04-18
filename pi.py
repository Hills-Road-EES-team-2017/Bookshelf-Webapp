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


#http = urllib3.PoolManager()
#login_data = dict(login='ledpi', password='ledpassword')
#url = "http://www.eeslibrary.com:8000/"
#session = requests.session()
#r = session.post(url, data=login_data)

url = 'http://www.eeslibrary.com:8000/login/'
client = requests.session()
#client.get(url)
#if 'crsftoken' in client.cookies:
#    crsftoken = client.cookies['crsftoken']
#login_data = dict(username='ledpi', password='ledpassword', crsfmiddlewaretoken=crsftoken, next='/')
login_data = dict(username='ledpi', password='ledpassword', next='/')
r = client.post(url, data=login_data, headers=dict(Referer=url))
print("Logged in")

while True:
    colour = API_Get_Button()
    if colour:
        print(colour, "button pressed")
        url = 'http://www.eeslibrary.com:8000/off/'+colour+'/'

        #r = http.request('GET', url)
        #r2 = session.get(url)
        r2 = client.get(url)
        

        print(colour, "web requested")
        time.sleep(0.3)
