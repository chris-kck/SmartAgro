"""Main module."""
from smartagro import utils
import paho.mqtt.client as mqtt
import adafruit_dht
import time

class SmartAgro:
    """
    Implemented After searching for a broker
    Instantiates an object which has sensors added to it then configures a broker.
    Sensors are attached added with corresponding topics
    Sensor Data is published and Actuator can be activated
    """

    def __init__(self):
        """
        Object constructor for the sensors and actuators to be attached to it.

        """
        self.client = None
        self.sensors = set()
        self.actuators = set()
        self.dhtDevice = adafruit_dht.DHT11(18) #GPIO 18 (Physical 12)
        # if none, scan network for brokers and connect to identified broker.
        # scan with utils.find_broker()
        self.config_broker()
        utils.gpio_init()

    def config_broker(self, broker="test.mosquitto.org", qos=0, port=1883, stream_schema="json"):
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
        #self.client.subscribe("smartagro/#")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        The callback for when a connection is established with the server.

        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the server.

        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        pass #print(msg.topic + " " + str(msg.payload))

    def read_sensor(self, channel):
        """
        # Reads sensor, publishes topic to broker
        :param channel:
        :return:
        """
        reading = utils.read_analogue(channel)
        self.client.publish(f"smartagro/sensor/{'Moisture' if channel==0 else 'Light'}", reading)  # sensor ID
        self.sensors.add(f"smartagro/sensor/{'Moisture' if channel==0 else 'Light'}")
        return reading

    def get_dht(self):
        """
        A function to get readings from the single wire DHT11 device.

        :param gpio: GPIO Pin connected to DHT Data Pin Default: GPIO 18 (Physical 12)
        :return: Temperature and Humidity Readings
        """
        try:
            temp=humidity=0
            temp, humidity = self.dhtDevice.temperature, self.dhtDevice.humidity
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0) # Retry after 2 seconds
            temp, humidity = self.dhtDevice.temperature, self.dhtDevice.humidity
        except Exception as error:
            self.dhtDevice.exit()
            raise error
        finally:
            print(f"Temp: {round(temp,2)} C &  Humidity: {round(humidity,2)}% ")  # TODO REMOVE LINE
            yield temp, humidity

    def read_dht(self):
        temperature, humidity = next(self.get_dht())
        self.client.publish(f"smartagro/sensor/humidity", humidity)
        self.client.publish(f"smartagro/sensor/temperature", temperature)
        self.sensors.add(f"smartagro/sensor/humidity")
        self.sensors.add(f"smartagro/sensor/temperature")
        return temperature, humidity

    def read_all(self):
        moist = self.read_sensor(0)/7  # Moisture
        light = self.read_sensor(2)/7  # Light
        temp, humid = self.read_dht()  # DHT
        return moist, light, temp, humid

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
        return self.actuators | self.sensors

# TODO Implement listening of mqtt actuator publish
# TODO add Keyboard interrupt catch for graceful exit.
