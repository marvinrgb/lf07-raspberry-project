#! /usr/bin/python
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt


client = mqtt.Client()

client.username_pw_set("mqtt_user", "raspberry")

client.connect("10.7.154.204", 1883)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    client.publish("greenhouse-1/floor-1/humiture-1/temperature", temperature)
    client.publish("greenhouse-1/floor-1/humiture-1/humidity", humidity)

    print(f"Temp: {temperature}°C  Humidity: {humidity}%")

    time.sleep(1)
