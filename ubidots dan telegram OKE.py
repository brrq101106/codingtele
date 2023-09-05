import requests
import math
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

TOKEN = "BBFF-e5j6artnMMHZHud3Mv3vHfukTuJwYW"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "position"  # Put your second variable label here


def build_payload(variable_1, variable_2, variable_3):
    # Creates two random values for sending data
    value_1 = temperature
    value_2 = humidity

    # Creates a random gps coordinates
    #lat = 3.5158333
    #lng = 98.7182236
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: {"value": 1, "context": {"lat": lat, "lng": lng}}}
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

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
       
    elif command =='/cek_suhu':
       bot.sendMessage(chat_id, "Temperature : %s*C" %temperature)
       bot.sendMessage(chat_id, "Humidity : %s persen" %humidity)


    elif command =='/start':
       kirim = "Selamat Datang di NAGATO (Navigasi and Translator).\n"
       kirim+= "Perintah Telegram:\n"
       kirim+= "/start >> Informasi\n"
       kirim+= "/cek_posisi >> Cek Posisi GPS\n"
       kirim+= "/cek_suhu >> Cek Sensor Suhu\n\n"
       kirim+= "By: TIM 70 Der führer"
       bot.sendMessage(chat_id, kirim)

bot = telepot.Bot('6598251290:AAFARsn9RD1iqvAtcty-m08P0OU-upvnzDY')
bot.message_loop(handle)
print ('I am listening...')

if __name__ == '__main__':
    while (True):
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
            lat= 3.5158333
            lng= 98.7182236
            gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
            gps2 = str(lat) + "," + str(lng)
            print(gps)
         
        main()
        time.sleep(1)
