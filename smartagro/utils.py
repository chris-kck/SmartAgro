"""Utilities Module."""

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


#All of the above for actuator //Connecting actuator to raspberry pi, configuring to subscribe to mqtt topics that send commands to activate / deactivate.
