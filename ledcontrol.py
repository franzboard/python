#!/usr/bin/env python3
# control LEDs via MQTT
#
from gpiozero import LED
import paho.mqtt.client as mqtt

leds = (LED(18), LED(23), LED(24), LED(25))
led_status = [0, 0, 0, 0]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("bulme/iot-test")

def on_message(client, userdata, msg):
    index = int(str(msg.payload, 'utf-8')[-1]) - 1
    led_status[index] = 1 - led_status[index]
    if led_status[index] == 1:
        leds[index].on()
    else:
        leds[index].off()
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iotlab.bulme.at", 1883, 60)

client.loop_forever()
