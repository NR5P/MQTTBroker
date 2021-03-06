import paho.mqtt.client as MQTTClient
import RPi.GPIO as GPIO     
import vlc, time

class DrivewayController():
    def __init__(self, client_id, mqtt_server, pin_num):
        self.client_id = client_id
        self.client_id = "raspberrypiclient"
        self.mqtt_server = mqtt_server
        self.topic = "outside/driveway_sensor"
        self.light_pin = pin_num
        GPIO.setup(self.light_pin,GPIO.OUT)

    def on_msg(self, client, userdata, msg):
        print(msg.topic+":"+msg.payload.decode("utf-8"))
        if msg.topic == 'outside/driveway_sensor' and msg.payload.decode("utf-8") == 'true':
            print("alarm firing")
            p = self.play_alarm()
            self.turn_light_on()
            p.stop()
        elif msg.topic == 'outside/driveway_sensor' and msg.payload.decode("utf-8") == 'disconnected':
            print("check the driveway sensor batteries")

    def connect_and_subscribe(self):
        client = MQTTClient.Client()
        client.on_message = self.on_msg
        client.connect('127.0.0.1',1883,60)
        client.subscribe(self.topic)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.mqtt_server, self.topic))
        return client

    def restart_and_reconnect(self):
        pass

    def play_alarm(self):
        p = vlc.MediaPlayer("./alarm.mp3")
        p.play()
        return p

    def turn_light_on(self):
        for i in range(5):
            GPIO.output(self.light_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.light_pin, GPIO.LOW)
