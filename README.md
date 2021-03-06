<span>[![Downloads](https://pepy.tech/badge/w3mo)](https://pepy.tech/project/w3mo) 
[![Downloads](https://pepy.tech/badge/w3mo/month)](https://pepy.tech/project/w3mo/month)
[![Downloads](https://pepy.tech/badge/w3mo/week)](https://pepy.tech/project/w3mo/week)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mghelton/w3mo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mghelton/w3mo/context:python)
</span>

# Overview

w3mo is a pure python API wrapper for wemo devices

# Installation
```pip3 install w3mo```

# Usage
## Interactive "Shell" 
```python
from w3mo import w3mo
w3mo.interactive() #this mode will launch a "shell" to interact with discovered devices on your network
```

##  Device Discovery
```python
from w3mo import w3mo

#returns a dictionary of devices with the device name as the key
#{'name':{'ip':device_ip,'obj':instantiated w3mo control class}}
x = w3mo.discover(return_type=dict)

#returns a list of devices
#[{'name':'device_name_1','ip':'device_ip':,'obj':instantiated w3mo control class}]
x = w3mo.discover(return_type=list)

#sets the timeout in seconds that the script will wait for a thread to join. This basically improves speed with the understanding that threads will still be running in the background if set too short. Default is 5s.
x = w3mo.discover(join_timeout=5)

#prints verbose debug data to the console. Default is False.
x = w3mo.discover(debug=True)
```

## Device Control
```python
from w3mo import w3mo
import time

devices = w3mo.discover(return_type=list)

#define device as the control class instantiation at index 0 of devices
device = devices[0]['obj']

#device name and state are set at instantiation and updated throughout use
print("Device Name = {}".format(device.name))
print("Device State = {}".format(device.state))

#turn on
device.set_state(1)


#time.sleep(.25)
#turn off
#device.set_state(0)
```

# Supported Devices

* NOTE: supported just means I had these devices / firmwares on hand for testing. Other devices SHOULD work, if you find something that doesn't fix it and submit a pull request!

<strong>Wemo Mini Smart Plug - F7C063</strong>

|Firmware Version                   |Supported          |
|:---                               |:---               |
|WeMo_WW_2.00.11452.PVT-OWRT-SNSV2  |:heavy_check_mark: |
|WeMo_WW_2.00.11420.PVT-OWRT-SNSV2  |:heavy_check_mark: |
|WeMo_WW_2.00.11326.PVT-OWRT-SNSV2  |:heavy_check_mark: |


<strong>Wemo WiFi Smart Light Switch - WLS040</strong>

|Firmware Version                       |Supported          |
|:---                                   |:---               |
|WeMo_WW_2.00.11451.PVT-OWRT-LIGHTV2    |:heavy_check_mark: |
|WeMo_WW_2.00.11395.PVT-OWRT-LIGHTV2    |:heavy_check_mark: |

# Related Projects
* [simple Kivy based UI](https://www.github.com/mghelton/w3mo_kivy)
* [electron and web server based UI](https://www.github.com/mghelton/w3mo_ui)
