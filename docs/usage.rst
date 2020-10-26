=====
Usage
=====

To use SmartAgro in a project::

    #Can be imported and implemented in different ways:
    #import smatagro then use smartagro.smartagro.func1() or smartagro.utils.func2()
    #from smartagro.smartagro import *
    # from smartagro import *, smart.SmartAgro(), smart.func1(), utils.func2()

Prefered and easy way to use SmartAgro in a project::

    from smartagro import *
    import time

    utils.find_broker() #search for a broker within your network
    utils.discover_i2c() #discover devices connected to your Pi

    # instatiate SmartAgro Object and conect to a broker. Optionally specify details
    obj = smart.SmartAgro()

    # Print different sensor' data values
    print(f"Moisture 0 output: {obj.read_sensor(0)} %")
    print(f"Light 2 output: {obj.read_sensor(2)} %")
    print(f"dht temperature and humidity: {obj.read_dht()}")

    # Activate an actuator directly with a pause then deactivate
    obj.activate_actuator(15,1)
    time.sleep(3)
    obj.activate_actuator(15,0)

    # Print out all 4 sensors' current values and publish to broker
    print(obj.read_all())

    #cleanup and exit the program
    utils.cleanup()
    exit(0)
