##### DHT11 Telemetry Collector #####
#@Description This program collects Temperature and Humidity readings and writes them to a CSV folder,
#used to collect legitimate data for later processing with a Machine Learning Algorthim.
#@Author: 'Bits, Please'
#@Date: 25/03/2022

##### IMPORTS #####
import time
import board
import adafruit_dht
import psutil
from datetime import datetime
import csv

##### METHODS #####
# Method to write sensor data to CSV file
def AppendToCSV(DataToWrite):
    with open('./THreadings2.csv', 'a') as csvfile:
        CSVWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        CSVWriter.writerow(DataToWrite)
        print("Appended new row to CSV File: {}".format(DataToWrite))
        

##### MAIN METHOD #####
if __name__ == "__main__":
    # First check if libgpiod process is running. If so terminate running instance.
    for process in psutil.process_iter():
        if (process.name() == 'libgpiod_pulsein' or process.name() == 'libgpiod_pulsei'):
            process.kill()

    # Initialise sensor object
    DHT11Sensor = adafruit_dht.DHT11(4)
    while True:
        try:
            Timestamp = datetime.now().replace(microsecond=0)
            Temperature = DHT11Sensor.temperature
            Humidity = DHT11Sensor.humidity
            TempHumidArray = [Temperature, Humidity]
            print("{} > Temperature: {}*C,  Humidity: {}% ".format(Timestamp, Temperature, Humidity))
            AppendToCSV(TempHumidArray)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            DHT11Sensor.exit()
            raise error
        
        # Sleep for two seconds before taking next measurement
        time.sleep(2.0)
