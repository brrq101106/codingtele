import Adafruit_DHT
import serial
import string
import pynmea2
import sys
import time
import random
import datetime
import telepot
import RPi.GPIO as GPIO
from telepot.loop import MessageLoop

#LED
def on(pin):
        GPIO.output(pin,GPIO.HIGH)
        return
def off(pin):
        GPIO.output(pin,GPIO.LOW)
        return
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up GPIO output channel
GPIO.setup(5, GPIO.OUT)
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
# Set GPIO sensor is connected to
gpio=4

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Got command: %s' % command)

    if command == '/cek_posisi':
       bot.sendMessage(chat_id, 'Posisi GPS: https://maps.google.com/maps?q=%s' %gps2)
       #"https://maps.google.com/maps?q=") + latitude + String(",") + longitude;
       on(5)
    elif command =='/cek_suhu':
       bot.sendMessage(chat_id, "Sensor Suhu : %s*C" %temperature)
       off(5)
    elif command =='/start':
       kirim = "Selamat Datang di NAGATO (Navigasi and Translator).\n"
       kirim+= "Perintah Telegram:\n"
       kirim+= "/start >> Informasi\n"
       kirim+= "/cek_posisi >> Cek Posisi GPS\n"
       kirim+= "/cek_suhu >> Cek Sensor Suhu\n\n"
       kirim+= "By: MAN 3 MEDAN"
       bot.sendMessage(chat_id, kirim)

bot = telepot.Bot('6598251290:AAFARsn9RD1iqvAtcty-m08P0OU-upvnzDY')
bot.message_loop(handle)
print ('I am listening...')

while 1:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    if humidity is not None and temperature is not None:
      print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
      print('Failed to get reading. Try again!')
    
    #Program Baca data GPS
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    #print(newdata)

    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
        gps2 = str(lat) + "," + str(lng)
        print(gps)
    else:
        lat= "3.5158333"
        lng= "98.7182236"
        gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
        gps2 = str(lat) + "," + str(lng)
        print(gps)
        
    time.sleep(1)




