# w3mo
Control your wemo devices!

# Installation
```pip3 install w3mo```

# Usage
```python
import w3mo

#returns a dictionary of w3mo devices with the IP address as the key
x = w3mo.discover(return_type=dict)

# OR

x = w3mo.discover(return_type=list)



```