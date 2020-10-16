"""Main module."""
from smartagro import utils
import paho.mqtt.client as mqtt


def foo():
    print('[mod1] foo()')


class SmartAgro:
    #after searching for a broker
    # this class instantiates an objecct wc has sensors added to itthen configures one. Next sensors are added with corresponding topics

    def __init__(self, broker_address="test.mosquitto.org", broker_port=1883, qos=0):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.qos = qos
        self.sensors = set()
        self.actuators = set()
        #if none, scan network for brokers and connect to identified broker.
        #config_broker()

    def devices_init(self):
        pass

    def add_sensor(self):
        pass
