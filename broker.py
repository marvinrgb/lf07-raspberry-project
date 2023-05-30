#! /usr/bin/python
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt


# DHT11 data pin (GPIO)
DHT_DATA_PIN = 4

# Setup DHT11 sensor
dht11_sensor = Adafruit_DHT.DHT11

# Setup MQTT Client
client = mqtt.Client()

client.username_pw_set("mqtt_user", "raspberry")

client.connect("10.7.154.204", 1883)

# Read sensor data and publish
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, DHT_DATA_PIN)

    client.publish("greenhouse-1/floor-1/humiture-1/temperature", temperature)
    client.publish("greenhouse-1/floor-1/humiture-1/humidity", humidity)

    print(f"Temp: {temperature}°C  Humidity: {humidity}%")

    time.sleep(6)
