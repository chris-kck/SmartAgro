"""Main module."""
from smartagro import utils
import paho.mqtt.client as mqtt
import adafruit_dht
import time

class SmartAgro:
    """

    after searching for a broker
    this class instantiates an object wc has sensors added to it then configures one. N
    ext sensors are added with corresponding topics
    """


    def __init__(self, broker_address="test.mosquitto.org", broker_port=1883, qos=0):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.qos = qos
        self.sensors = set()
        self.actuators = set()
        self.dhtDevice = adafruit_dht.DHT11(18) #GPIO 18 (Physical 12)
        # if none, scan network for brokers and connect to identified broker.
        # scan with utils.find_broker()
        self.config_broker()
        utils.gpio_init()
        utils.sensor_attach_serial()

    def config_broker(self, broker, qos, port=1883, stream_schema="json"):
        """
        Function to configure a new broker to be published to.

        :param broker: The url or ip address of the broker.
        :param qos: quality of service determining how many times message is sent. 0,1,2
        :param port: broker port in use. default 1883, ssl 8883
        :param stream_schema: the data stream schema used. Default is json
        :return: mqtt client object

        """
        self.client = mqtt.Client("RPi0-ZA-2020")  # create new client
        self.client.connect(broker, port)  # connect to broker
        self.client.publish(topic="smartagro/test", payload="Test Successful", qos=qos)  # TOPIC & test payload
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # The callback for when a PUBLISH message is received from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def read_sensor(self, channel):
        reading = utils.read_analogue(channel)
        self.client.publish(f"smartagro/sensor/{channel}", reading)  # sensor ID
        self.sensors.add(f"smartagro/sensor/{channel}")

    def read_dht_11(self,pin=17):
        sensor=11 #DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        self.client.publish(f"smartagro/sensor/humidity", humidity)
        self.client.publish(f"smartagro/sensor/temperature", temperature)
        self.sensors.add(f"smartagro/sensor/humidity")
        self.sensors.add(f"smartagro/sensor/temperature")

    def read_all(self):
        for channel in range(3):
            self.read_sensor(channel)
        self.read_dht_11()

    def activate_actuator(self, gpio_pin, state):
        utils.switch_actuator(gpio_pin, state)
        self.client.publish(f"smartagro/actuator/{gpio_pin}", state)  # actuator ID
        self.actuators.add(f"smartagro/actuator/{gpio_pin}")

    def remove_device(self, device):
        try:
            self.actuators.remove(device) if device in self.actuators else self.sensors.remove(device)
        except KeyError:
            print("The device you are trying to remove des not exist. Check connected devices again!")


    def active_devices(self):
        return (self.actuators | self.sensors)

# TODO Implement listening of mqtt actuator publish
# TODO add Keyboard interrupt catch for graceful exit.
