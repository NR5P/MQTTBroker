import time
from umqttsimple import MQTTClient
import micropython
import network
import RPi.GPIO as GPIO       
from drivewayController import DrivewayController


with open("settings.json") as file:
    data = ujson.load(file.read())

ssid = data["ssid"]
password = data["password"]
mqtt_server = "127.0.0.1" #localhost in this case
client_id = ubinascii.hexlify(machine.unique_id())

last_message = 0
message_interval = 20
counter = 0
LIGHT_PIN = 17

GPIO.setmode(GPIO.BCM)       

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

drivewayController = DrivewayController(client_id, mqtt_server)

if station.isconnected() == False:
    station.connect(ssid, password)
while station.isconnected() == False:
    pass
print("Connection Successful")
print(station.ifconfig())

try:
    client = drivewayController.connect_and_subscribe()
except OSError as e:
    drivewayController.restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      last_message = time.time()
      counter += 1
  except OSError as e:
    driveway_controller.restart_and_reconnect()