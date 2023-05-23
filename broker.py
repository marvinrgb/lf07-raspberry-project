#! /usr/bin/python
import time
import Adafruit_DHT

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print(f"Temp: {temperature}°C  Humidity: {humidity}%")

    time.sleep(1)
