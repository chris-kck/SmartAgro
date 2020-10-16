"""Main module."""
from smartagro import utils
import paho.mqtt.client as mqtt


def foo():
    print('[mod1] foo()')


class SmartAgro:
    #after searching for a broker
    # this class instantiates an objecct wc has sensors added to itthen configures one. Next sensors are added with corresponding topics

    def __init__(self, broker_ip=None, broker_port=None, qos=0, devices=4):
        self.broker_IP = broker_ip
        self.broker_PORT = broker_port
        self.qos = qos
        self.devices = devices
        #if none, scan network for brokers and connect to identified broker.
        #config_broker()

    def devices_init(self):
        pass

    def add_sensor(self):
        pass
