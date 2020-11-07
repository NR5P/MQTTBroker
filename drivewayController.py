from umqttsimple import MQTTClient
import RPi.GPIO as GPIO     
import vlc, time

class DrivewayController():
    def __init__(self, client_id, mqtt_server, pin_num):
        self.client_id = client_id
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.mqtt_server = mqtt_server
        self.topic = b"outside/driveway_sensor"
        self.light_pin = pin_num
        GPIO.setup(self.light_pin,GPIO.OUT)

    def sub_cb(self, topic, msg):
        print((topic, msg))
        if topic == b'outside/driveway_sensor' and msg == b'true':
            self.play_alarm()
            self.turn_light_on()
            self.stop()

    def connect_and_subscribe(self):
        client = MQTTClient(self.client_id, self.mqtt_server)
        client.set_callback(self.sub_cb)
        client.connect()
        client.subscribe(self.topic)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.mqtt_server, self.topic))
        return client

    def restart_and_reconnect(self):
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(10)
        machine.reset()

    def play_alarm(self):
        p = vlc.MediaPlayer("./alarm.mp3")
        p.play()

    def stop_alarm(self):
        p.stop()

    def turn_light_on(self):
        for i in range(5):
            GPIO.output(self.light_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.light_pin, GPIO.LOW)