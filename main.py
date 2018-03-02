
import network
import time
import machine
from machine import Pin

import gc
from umqtt.simple import MQTTClient

led = Pin(2, Pin.OUT, value=1)

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"ON":
         state = 0
    elif msg == b"OFF":
         state = 1
    led.value(state)
    
adc=machine.ADC(0)

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "wifimac"
yourWifiPassword = "nisupu17"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass

print("Connected to wifi")

  
#
# connect ESP8266 to Adafruit IO using MQTT
#
myMqttClient = "maperales-mqtt-client"  # can be anything unique
adafruitIoUrl = "io.adafruit.com" 
adafruitUsername = "Maperales"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "61eb15f208704af7af96f23dc5956155"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.set_callback(sub_cb)

c.connect()
c.subscribe("Maperales/feeds/b1")

print("Connected to Adafruit.io")
#
# publish temperature and free heap to Adafruit IO using MQTT
#
# note on feed name in the MQTT Publish:  
#    format:
#      "<adafruit-username>/feeds/<adafruitIO-feedname>"
#    example:
#      "MikeTeachman/feeds/feed-TempInDegC"
#
#
while True:
  Luz=adc.read()
  print(Luz)
  c.publish("Maperales/feeds/luz", str(Luz))  # publish temperature to adafruit IO feed
  c.publish("Maperales/feeds/luz-hist", str(Luz))  #publish num free bytes on the Heap
  c.check_msg()
  time.sleep(5)  # number of seconds between each Publish
  
c.disconnect()  
