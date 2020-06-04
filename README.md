# Overview

w3mo is a pure python API wrapper for wemo devices

<span>[![Downloads](https://pepy.tech/badge/w3mo)](https://pepy.tech/project/w3mo) 
[![Downloads](https://pepy.tech/badge/w3mo/month)](https://pepy.tech/project/w3mo/month)
[![Downloads](https://pepy.tech/badge/w3mo/week)](https://pepy.tech/project/w3mo/week)</span>

# Installation
```pip3 install w3mo```

# Usage
* Interactive "Shell" 
```python
from w3mo import w3mo
w3mo.interactive() #this mode will launch a "shell" to interact with discovered devices on your network
```

* Device Discovery
```python
from w3mo import w3mo

#returns a dictionary of devices with the device name as the key
#{'name':{'ip':device_ip,'obj':instantiated w3mo control class}}
x = w3mo.discover(return_type=dict)

#returns a list of devices
#[{'name':'device_name_1','ip':'device_ip':,'obj':instantiated w3mo control class}]
x = w3mo.discover(return_type=list)
```

* Device Control
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