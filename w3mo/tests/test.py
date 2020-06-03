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