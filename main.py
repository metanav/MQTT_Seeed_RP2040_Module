from time import sleep
import network
import mqtt
from machine import Pin, I2C, ADC, UART, SPI, PWM
from bme680 import *

i2c = I2C(1, scl=Pin(27), sda=Pin(6))
bme = BME680_I2C(i2c=i2c, address=0x76)

N1 = network.WLAN_SPI(network.STA_IF)
N1.active(True)
N1.connect("myssid", "mypsk")
sleep(1)

SERVER = 'mqtt_broker_url_or_ip_address' #
USER   = 'myuser'
PWD    = 'mypassword'
TOPIC  = 'sensors/data'

cl = mqtt.MQTTClient(USER, SERVER, mqtt_port = 1883, mqtt_user=USER, mqtt_password=PWD)

sleep(1)

if N1.isconnected():
    print("connecting...")

    print(cl.connect())
    print("connected")
    sleep(1)
    
    while True:
        try:
            temperature = str(round(bme.temperature, 2))
            humidity = str(round(bme.humidity, 2))
            pressure = str(round(bme.pressure, 2))
            gas = str(round(bme.gas/1000, 2))
            data = temperature + " " + humidity + " " + pressure + " " + gas
            cl.publish(TOPIC, data)
        except OSError as e:
            print('Failed to read sensor.')
        
        sleep(1)

