import sys
import time
from datetime import datetime
import Adafruit_DHT

import csv

# set type of the sensor
sensor = 11
# set pin number
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).


def AppendToCSV(DataToWrite):
    with open('./readings.csv', 'a') as csvfile:
        CSVWriter = csv.writer(csvfile, delimiter=',')
        CSVWriter.writerow([DataToWrite])
        print("Appended new row to CSV File: {}".format(DataToWrite))


if __name__ == "__main__":
    while True:
        timestamp = datetime.now().replace(microsecond=0)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            print('{}: Temp={}C, Humidity={}%'.format(timestamp, temperature, humidity))
            AppendToCSV(int(temperature))
        else:
            print('Failed to get reading. Try again!')
        time.sleep(2)