"""Top-level package for SmartAgro."""
#this file is always run each time the package is imported.
#will use this to  effect automatic importing of modules. instead of smartagro.smartagro.func()

import smartagro.smart, smartagro.utils

#implement as: from smartagro.smartagro import * OR import smatagro then use smartagro.smartagro.func()

# from smartagro import *, smart.foo(), utils.bar(), smart.SmartAgro() .

__author__ = """Kudzai Chris Kateera"""
__email__ = 'kckateera@gmail.com'
__version__ = '0.1.0'
__all__ = ['smart','utils'] #imports for from <package_name> import *


print("Invoking __init.py__ for".format(__name__))
