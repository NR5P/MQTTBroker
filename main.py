import time
import RPi.GPIO as GPIO       
from drivewayController import DrivewayController


mqtt_server = "127.0.0.1" #localhost in this case
client_id = "raspimqttclient"

last_message = 0
message_interval = 20
counter = 0
LIGHT_PIN = 17

GPIO.setmode(GPIO.BCM)       

drivewayController = DrivewayController(client_id, mqtt_server, LIGHT_PIN)


try:
    client = drivewayController.connect_and_subscribe()
    print("Connection Successful")
except OSError as e:
    print("error connecting")

client.loop_forever()

