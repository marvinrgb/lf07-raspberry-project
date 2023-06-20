#! /usr/bin/python
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
import mariadb
import sys
from datetime import datetime, timezone
import RPi.GPIO as GPIO


# Setup Board and GPIOs
FAN_PIN = 12        # Transistor base connected on that pin
DHT_DATA_PIN = 4    # DHT11 sensor data pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.output(FAN_PIN, GPIO.LOW)

# Setup DHT11 sensor
dht11_sensor = Adafruit_DHT.DHT11

# Connect to MariaDB Database
try:
    conn = mariadb.connect(
        user="python",
        password="vmmFWLgAelf7",
        host="localhost",
        port=3306,
        database="humiture"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    GPIO.cleanup()
    sys.exit(1)

# Get Cursor to database
cur = conn.cursor()

# Setup MQTT Client
client = mqtt.Client()
client.username_pw_set("mqtt_user", "raspberry")
try:
    client.connect("10.7.154.204", 1883)
except OSError as e:
    print("Couldn't connect to BOSS PI!", e)

# Read sensor data and publish
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, DHT_DATA_PIN)

    current_time: str = datetime.now(tz=timezone.utc)

    client.publish("greenhouse-1/floor-1/humiture-1/temperature", temperature)
    client.publish("greenhouse-1/floor-1/humiture-1/humidity", humidity)

    # Save to database
    try:
        cur.execute("INSERT INTO data (time,temperature,humidity) VALUES (?, ?, ?)",
                    (current_time, temperature, humidity))
        conn.commit()
    except mariadb.Error as e:
        print(f"Error saving to database: {e}")

    print(f"Temp: {temperature}°C  Humidity: {humidity}%")

    if (temperature > 25) or (humidity > 80):
        GPIO.output(FAN_PIN, GPIO.HIGH)
    else:
        GPIO.output(FAN_PIN, GPIO.LOW)

    time.sleep(5)

conn.close()
GPIO.cleanup()
