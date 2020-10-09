"""Utilities Module."""
from paho import mqtt
import os
import socket

def bar():
    from smartagro import __author__
    print('[mod2] bar(){}'.format(__author__)) # f'haha{var}' not supported in python 3.5


class Bar:
    pass

def config_broker(ip, QS, PORT, stream_schema): #mqtt broker configuration
    pass

def discover_devices(comm_interface): #scans address space and ports to discover connected I2C or SPI devices
    pass

def create_sensor_type(read,write,config): #Add support for new sensor type
    pass

def sensor_attach_i2c(SensorType1, addr,sample_rate, broker): #Add sensor, assign broker and topic
    pass

def sensor__attach_serial(SensorType2, port, baud, broker): #Add sensor, assign broker and topic
    pass

def sensor_detach(stream, broker):  #remove sensor from publishing topics
    pass

def list_active_sensor_streams(broker): #show topics being published to broker
    pass

def sensor_update(addr, new_sample_rate): #Dynamic adjustment of sensor details
    pass

def find_broker(): #Scan for a MQTT broker within network
    pass

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1' #localhost loopback IP if not connected to wifi
    finally:
        s.close() #close socket
    return IP

def scan_network():
    pass

#functions to communicate with Seeed devices. ADC/Direct/?


#All of the above for actuator //Connecting actuator to raspberry pi, configuring to subscribe to mqtt topics that send commands to activate / deactivate.
