"""Main module."""
from smartagro import utils
import paho.mqtt.client as mqtt


def foo():
    print('[mod1] foo()')


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
        # if none, scan network for brokers and connect to identified broker.
        self.config_broker(broker_address, qos, broker_port)
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
        self.client.publish(topic="dev/test", payload="OFF ua", qos=qos)  # TOPIC & test payload
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # The callback for when a PUBLISH message is received from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def read_sensor(self, channel):
        # add sensor and add topic
        reading = utils.read_analogue(channel)
        self.sensors.add(channel)
        self.client.publish(f"smartagro/sensor{channel}", reading)  # sensor ID

    def activate_actuator(self, gpio_pin, state):
        utils.switch_actuator(gpio_pin, state)
        self.actuators.add(gpio_pin)
        self.client.publish(f"smartagro/actuator{gpio_pin}", state)  # actuator ID

    # TODO Implement listening of mqtt actuator publish
