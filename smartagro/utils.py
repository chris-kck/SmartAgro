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
    my_ip = get_ip()
    net = my_ip.split(".")[:-1]
    online_dev=list()
    print (f"Scanning Hosts {my_ip}'s Network:")
    for host in range(1,0x64): # 0xff only scanning /24 subnet
        dev = ".".join(net)+"."+str(host)
        response = os.popen(f"ping -w 1 {dev}") #-c 1
        try:
            if(response.readlines()[5]):
                print(f"{dev} is online")
                online_dev.append(dev)
        except:
            continue
    #Add support to scan online hosts' ports to find broker. - still buggy
    for  ip in online_dev:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = s.connect_ex((ip,1883)) #scan port 1883 and 8883 for SSL
        if(conn == 0) :
            print(f'MQTT Port 1883 OPEN for {ip}')
        s.close()
        print("Scan Completed")


#functions to communicate with Seeed devices. ADC/Direct/?


#All of the above for actuator //Connecting actuator to raspberry pi, configuring to subscribe to mqtt topics that send commands to activate / deactivate.
