"""Utilities Module."""
import paho.mqtt.client as mqtt
import os
import socket
import mcp3008

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Use sudo / run sudo usermod -aG gpio <myusername> to get permission")

def bar():
    """
    Useless test function
    :return:
    """
    from smartagro import __author__
    print('[mod2] bar(){}'.format(__author__))  # f'haha{var}' not supported in python 3.5

topic = "SmartAgro/Sensors/"

class Bar:
    pass


def config_broker(broker="mqtt.eclipse.org", QS=0, PORT="1883", stream_schema="json"):
    """
    Function to configure a new broker to be published to.
    :param broker: The url or ip address of the broker
    :param QS: quality of service determining how many times message is sent. 0,1,2
    :param PORT: broker port in use. default 1883, ssl 8883
    :param stream_schema: the data stream schema used. Default is json
    :return: No return
    """
    client = mqtt.Client("RPi0-ZA") #create new client
    client.connect(broker,PORT) #connect to broker
    client.publish("dev/test","OFF ua") #TOPIC & test payload
    #TODO test functionality


def discover_devices(comm_interface):  # scans address space and ports to discover connected I2C or SPI devices
    #os i2cdetect?
    #1 I2C port and two SPI ports
    print("Scan for connected I2C devices' addresses:")
    print(os.popen("i2cdetect -y 1").read())
    #TODO Add SPI scanning support

def create_sensor_type(read, write, config):  # Add support for new sensor type
    pass

def sensor_attach_i2c(SensorType1, addr, sample_rate, broker):  # Add sensor, assign broker and topic
    pass


def sensor_attach_serial(SensorType2, port, baud, broker):  # Add sensor, assign broker and topic
    pass

def sensor_read_analogue():
    adc = mcp3008.MCP3008()
    ADC_values = adc.read_all()
    adc.close()

def sensor_detach(stream, broker):  # remove sensor from publishing topics
    pass


def list_active_sensor_streams(broker):  # show topics being published to broker
    pass


def sensor_update(addr, new_sample_rate):  # Dynamic adjustment of sensor details
    pass

def find_broker():  # Scan for a MQTT broker within network
    # Add support to scan online hosts' ports to find broker. - still buggy
    online_dev = scan_network()
    for ip in online_dev:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = s.connect_ex((ip, 1883))  # scan port 1883 and 8883 for SSL
        if (conn == 0):
            print(f'MQTT Port 1883 OPEN for {ip}')
        s.close()
        print("Scan Completed")


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'  # localhost loopback IP if not connected to wifi
    finally:
        s.close()  # close socket
    return IP

def scan_network():
    my_ip = get_ip()
    net = my_ip.split(".")[:-1]
    online_dev = list()
    print(f"Scanning Hosts {my_ip}'s Network:")
    for host in range(1, 0x64):  # 0xff only scanning /24 subnet
        dev = ".".join(net) + "." + str(host)
        response = os.popen(f"ping -w 1 {dev}")  # -c 1
        try:
            if (response.readlines()[5]):
                print(f"{dev} is online")
                online_dev.append(dev)
        except:
            continue
    return online_dev

# functions to communicate with Seeed devices. ADC/Direct/?


# All of the above for actuator //Connecting actuator to raspberry pi, configuring to subscribe to mqtt topics that send commands to activate / deactivate.
