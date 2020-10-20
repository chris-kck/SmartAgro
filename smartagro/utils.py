"""Utilities Module."""
import os
import socket

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

def discover_devices(comm_interface):
    """
    Scans address space and ports to discover connected I2C or SPI devices
    uses os i2cdetect for the 1 I2C port and also scans two SPI ports

    :param comm_interface: communication interface to be scanned.
    :return:

    """
    print("Scan for connected I2C devices' addresses:")
    print(os.popen("i2cdetect -y 1").read())
    # TODO Add SPI scanning support - can only be done by sending a valid
    #  signal to spi mosi and geting a valid response on miso
    print("Checking if SPI Module is loaded:")
    print(os.popen("lsmod | grep spi").read())


def create_sensor_type(read, write, config):  # Add support for new sensor type
    pass


def sensor_attach_i2c(SensorType1, addr, sample_rate, broker):  # Add sensor, assign broker and topic
    pass


def sensor_attach_serial( spi_device=0, baud=976000):  # Add sensor, assign broker and topic
    """
    Adds and configures an SPI device & adds its topic?

    :param spi_device: Either 0 or 1 as there are only 2 spi ports
    :param baud: the bit rate, measured in bit/s clock rate used for device
    :return: No return
    """
    spi = spidev.SpiDev()
    spi.open(0, spi_device)
    spi.max_speed_hz = 976000

    CLK = 23
    MISO = 21
    MOSI = 19
    CS = 24 if spi_device == 0 else 26  # CE0 or CE1

    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)


def read_analogue(channel):
    """
    Reads an analogue signal from the connected SPI ADC device

    :param channel: ADC channel where sensor is connected.
    :return: ADC output Normalized with Vref.
    """
    # link with SPI device initialization. Docs: https://pypi.org/project/mcp3008/
    _, byte1, byte2 = spi.xfer2([1,(8+channel)<<4,0])
    raw_data = ((byte1&3) << 8) + byte2
    return raw_data


def switch_actuator(gpio_pin, state):
    """
    Function to switch fan actuator ON or OFF

    :param gpio_pin: The pin the fan relay (motor in demo) is connected to.
    :param state: Boolean indicating whether fan is on or off.
    :return: NO return
    """
    GPIO.setup(gpio_pin, GPIO.OUT) #repetitive, will need to be done once.

    if state:
        GPIO.output(gpio_pin, GPIO.HIGH)
    else:
        GPIO.output(gpio_pin, GPIO.HIGH)


def sensor_detach(stream, broker):  # remove sensor from publishing topics
    pass


def get_ip():
    """
    Ger the IP address other than the loopback IP that the device has been allocated by DHCP

    :return: IP address
    """
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
    """
    Scan subnet /24 of IP address to check for brokers on the local network.

    :return: list of online devices responding to ICMP echo request using ping.
    """
    my_ip = get_ip()
    net = my_ip.split(".")[:-1]
    online_dev = list()
    print(f"Scanning Hosts {my_ip}'s Network:")
    for host in range(1, 0x64):  # 0xff only scanning /24 subnet
        dev = ".".join(net) + "." + str(host)
        response = os.popen(f"ping -w 1 {dev}")  # -c 1
        try:
            if response.readlines()[5]:
                print(f"{dev} is online")
                online_dev.append(dev)
        except IndexError:
            continue
    return online_dev


def find_broker():
    """
    Scan for a MQTT broker within network by checking online hosts then scanning for
    open MQTT ports
    # TODO Add support to scan online hosts' ports to find broker. - still buggy

    :return: No return
    """

    online_dev = scan_network()
    for ip in online_dev:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = s.connect_ex((ip, 1883)) or s.connect_ex((ip, 8883))  #unencrypted port 1883 or encrypted port 8883 open.
        if (conn == 0):
            print(f'MQTT Port 1883 or 8883 OPEN for {ip}')
        s.close()
    print("Scan Completed")


def add_actuator(pin, device):
    """
    Function to initialize the GPIO pins, numbering system used and communication protocols.

    :return: No return
    """
    GPIO.setup(pin, GPIO.OUT)
    client.publish(f"smartagro/device{device}","New device")

def gpio_init(mode="GPIO.BOARD"):
    """
    Function to initialize the GPIO pins, numbering system used and communication protocols.

    :return: No return
    """
    GPIO.setmode(mode)  # Physical Pin Numbers
    GPIO.setwarnings(False)

def cleanup():
    """
    GPIO.cleanup() and exit(0) for a graceful exit.

    """
    spi.close()
    GPIO.cleanup()
    exit(0)

# All of the above for actuator //Connecting actuator to raspberry pi,
# configuring to subscribe to mqtt topics that send commands to activate / deactivate.
