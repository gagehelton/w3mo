# w3mo
Control your wemo devices!

# Installation
```pip3 install w3mo```

# Usage
* Device Discovery
```python
import w3mo

#returns a dictionary of devices with the device name as the key
#{'name':{'ip':device_ip,'obj':instantiated w3mo control class}}
x = w3mo.discover(return_type=dict)

#returns a list of devices
#[{'name':'device_name_1','ip':'device_ip':,'obj':instantiated w3mo control class}]
x = w3mo.discover(return_type=list)
```
* Device Control
```python
import w3mo
import time

devices = w3mo.discover(return_type=list)

#define device as the control class instantiation at index 0 of devices
device = devices[0]['obj']
print("Device Name = {}".format(device.name))
print("Device State = {}".format(device.state))

#turn on
device.set_state(1)

time.sleep(.25)

#turn off
device.set_state(0)
```