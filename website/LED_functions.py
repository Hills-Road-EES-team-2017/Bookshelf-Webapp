import RPi.GPIO as GPIO
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

speed = 0.0000025
number_of_LEDs = 60
number_of_strips = 10
LEDs = []
for x in range(number_of_strips):
    LEDs.append([])
    for y in range(number_of_LEDs):
        LEDs[x].append(3758096384)



def initialise():
    for strip_number in range(number_of_strips):
         for LED_number in range(number_of_LEDs):
             LEDs[strip_number][LED_number] = 0xE0000000
         #start frame - all 0s
         send_32bits(strip_number,0x00000000)
         for LED_number in range(number_of_LEDs):
             send_32bits(strip_number, LEDs[strip_number][LED_number])
         #End frame - all 1s
         send_32bits(strip_number, 0x11111111)
def initialise():
  pass

def send_32bits(shelf, data):
    
    # send_data = [0]
    # if (shelf == 0):
    #     GPIO.output(11, GPIO.LOW)
    # else:
    #     GPIO.output(11, GPIO.HIGH)
    #
    # send_data[0] = (data >> 24) & 0x000000FF
    # spi.xfer(send_data)
    # send_data[0] = (data >> 16) & 0x000000FF
    # spi.xfer(send_data)
    # send_data[0] = (data >> 8) & 0x000000FF
    # spi.xfer(send_data)
    # send_data[0] = (data >> 0) & 0x000000FF
    # spi.xfer(send_data)
    pass
                
def LED_function(shelf, distance, colour):
    print(shelf, distance, colour)
    print()
    #API LEDs
    #update array
    colourDict = {"R":0xF00000FF,"B":0xF0FF0000,"W":0xFFF0F0F0,"O":0xE0000000,"C":0xF0F0F000,"Y":0xF0004488,"M":0xF0FF00FF,"G":0xF000FF00}
    LEDposition = int (distance/16.5)
    
    for i in range(int(len(LEDs[shelf])/2)): #Finds nearest LED not on already
        if LEDs[shelf][LEDposition+i] == 3758096384: #If equal to "O"
            LEDposition += i
            break
        elif LEDs[shelf][LEDposition-i] == 3758096384:
            LEDposition -= i
            break
        
    # Assigns colour to required LED
    LEDs[shelf][LEDposition] = colourDict[colour]
    #light LED Strip
    #start frame - all 0s
    send_32bits(shelf,0x00000000)
    for LED_number in range(number_of_LEDs):
        # Sends data to each LED
        send_32bits(shelf, LEDs[shelf][LED_number])
    #End frame - all 1s
    send_32bits(shelf, 0x11111111)

def LED_colour_off(shelf, colour):
    colourDict = {"R":0xF00000FF,"B":0xF0FF0000,"W":0xFFF0F0F0,"O":0xE0000000,"C":0xF0F0F000,"Y":0xF0004488,"M":0xF0FF00FF,"G":0xF000FF00}
    LEDposition = 0
    for LED_number in range(len(LEDs[shelf])):
        if LEDs[shelf][LED_number] == colourDict[colour]:
            LEDposition = LED_number
            break

    LEDs[shelf][LEDposition] = colourDict["O"]

            
    #start frame - all 0s
    send_32bits(shelf,0x00000000)
    for LED_number in range(number_of_LEDs):
        # Sends data to each LED
        send_32bits(shelf, LEDs[shelf][LED_number])
    #End frame - all 1s
    send_32bits(shelf, 0x11111111)
                                                                         
