#! /usr/bin/python
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
import mariadb
import sys
from datetime import datetime, timezone


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
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

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

    time.sleep(6)

conn.close()
