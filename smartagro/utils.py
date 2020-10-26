"""Utilities Module. With several functions that are repeatedly used"""
import os
import socket
import spidev

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Use sudo / run sudo usermod -aG gpio <myusername> to get permission")


def discover_i2c():
    """
    Scans address space and ports to discover connected I2C or SPI devices
    uses os i2cdetect for the 1 I2C port and also scans two SPI ports

    """
    print("Scan for connected I2C devices' addresses:")
    print(os.popen("i2cdetect -y 1").read())
    print("Checking if SPI Module is loaded:")
    print(os.popen("lsmod | grep spi").read())


def read_analogue(channel, spi_device=0, baud=1350000):
    """
    Reads an analogue signal from the connected SPI ADC device and returns channel reading.

    :param channel: ADC channel where sensor is connected.
    :type channel: int
    :param spi_device: Either 0 or 1 as there are only 2 spi ports
    :type spi_device: int
    :param baud: the bit rate, measured in bit/s clock rate used for device
    :type baud: int
    :return: Raw 1024 bit ADC output data.
    """
    spi = spidev.SpiDev()
    spi.open(0, spi_device)
    spi.max_speed_hz = baud  # spi clock speed
    _, byte1, byte2 = spi.xfer2([1, (8+channel) << 4, 0])
    raw_data = ((byte1 & 3) << 8) + byte2
    return raw_data


def switch_actuator(gpio_pin, state):
    """
    Function to switch actuator ON or OFF

    :param gpio_pin: The pin the fan relay (motor in demo) is connected to.
    :type gpio_pin: int
    :param state: Boolean indicating whether fan is on or off.
    :type state: boolean
    """
    GPIO.setup(gpio_pin, GPIO.OUT)  # repetitive, will need to be done once.
    GPIO.output(gpio_pin, state)


def scan_network():
    """
    Ger the IP address other than the loopback IP that the device has been allocated by DHCP
    Scan subnet /24 of IP address to check for LAN brokers' availability.

    :return: list of online devices responding to ICMP echo request using ping.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'  # localhost loopback IP if not connected to wifi
    finally:
        s.close()  # close socket

    net = ip.split(".")[:-1]
    online_dev = list()
    print(f"Scanning Hosts {ip}'s Network:")
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
    Scan for online MQTT brokers then scan within network by checking online hosts then scanning for
    open MQTT ports

    :return: No return
    """

    online_dev = scan_network()
    online_dev = ["mqtt.eclipse.org", "test.mosquitto.org"]+online_dev  # prepend online test brokers
    for ip in online_dev:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # unencrypted port 1883 or encrypted port 8883 open.
        conn = min(s.connect_ex((ip, 1883)), s.connect_ex((ip, 8883)))
        if conn == 0:
            print(f'MQTT Port 1883 or 8883 OPEN for {ip}')
        else:
            print(f'MQTT Port 1883 or 8883 CLOSED for {ip}')
        s.close()
    print("Scan Completed")


def gpio_init():
    """
    Function to initialize the GPIO pins, numbering system used and communication protocols.
    GPIO.BCM IS THE DEFAULT

    """
    GPIO.setmode(GPIO.BCM)  # Physical Board Pin Numbers
    GPIO.setwarnings(False)


def cleanup():
    """
    GPIO.cleanup() and exit(0) for a graceful exit.

    """
    spidev.SpiDev().close()  # close SPI connection
    GPIO.cleanup()
    exit(0)

def create_sensor_type(read, write, config):  # Add support for new sensor type
    pass

def sensor_attach_i2c(SensorType1, addr, sample_rate, broker):  # Add sensor, assign broker and topic
    pass
