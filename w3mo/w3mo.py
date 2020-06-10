import sys
import socket
import requests
import threading
import xml.etree.ElementTree as ET

debug = False
devices = {}

## self.state = 3 means setting state from function call failed


class _DEFAULTS():
    headers={
            'User-Agent': '',
            'Accept': '',
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': '\"urn:Belkin:service:basicevent:1#{action}\"',
    }
    
    actions = {"GET_STATE":"GetBinaryState",
                    "SET_STATE":"SetBinaryState",
                    "GET_NAME":"GetFriendlyName",
                    "SET_NAME":"Name"}

    states = {"STATE":"BinaryState","NAME":"FriendlyName"}
    
    port = 49153
    timeout = 10
    
    base_url = 'http://{device}:{port}/upnp/control/basicevent1'.format(device = "{device}",port=port)

    post_xml = '''
        <?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:{action} xmlns:u="urn:Belkin:service:basicevent:1">
                    <{state}>{value}</{state}>
                </u:{action}>
            </s:Body>
        </s:Envelope>
    '''
    
    get_xml = '''
        <?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:{action} xmlns:u="urn:Belkin:service:basicevent:1">
                </u:{action}>
            </s:Body>
        </s:Envelope>
    '''

def parse_kwargs(required,kwargs):
    for arg,val in kwargs.items():
        if(arg in required):
            if(not isinstance(val,required[arg]['type'])):
                return False
    return True

class w3mo():
    def __init__(self,**kwargs):
        required = {"ip":{"type":str}}
        if(parse_kwargs(required,kwargs)):
            self.ip = kwargs['ip']
            self.url = _DEFAULTS.base_url.format(device=self.ip)
            self.state = 0
            self.name = 'unkown'
            self.get_state()
            self.get_name()
            
    def parse_xml(self,value,search):
        xml = ET.fromstring(value)
        for node in xml.iter(search):
            if(node.text):
                return node.text
            else:
                print("something is off... \n\n {} \n\n".format(node))
                return False

    def set_state(self,state):
        try:
            response = self.control(action=_DEFAULTS.actions['SET_STATE'],
                state=_DEFAULTS.states['STATE'],
                value=state
                )
            try:
                self.state = int(response)
            except:
                self.state = 3
        except Exception as e:
            print(type(e).__name__,e.args)

    def get_state(self):
        try:
            response = self.get(
                action=_DEFAULTS.actions['GET_STATE'],
                value='state'
            )
            try:
                self.state = int(response)
            except:
                self.state = 3
        except Exception as e:
            print(type(e).__name__,e.args)

    def get_name(self):
        try:
            response = self.get(
                action=_DEFAULTS.actions['GET_NAME'],
                value='name'
            )
            self.name = response
        except Exception as e:
            print(type(e).__name__,e.args)

    def control(self,**kwargs):
        required = {"action":{"type":str},"state":{"type":str},"value":{"type":int}}
        if(parse_kwargs(required,kwargs)):
            try:
                headers = _DEFAULTS.headers.copy()
                headers['SOAPACTION'] = headers['SOAPACTION'].format(**kwargs)
    
                data = _DEFAULTS.post_xml.format(**kwargs)
    
                #print("{}\n{}\n{}\n\n\n\n".format(self.url,headers,data))
    
                response = requests.post(self.url,headers=headers,data=data,timeout=_DEFAULTS.timeout)
                if(response.status_code == 200):
                    state = self.parse_xml(response.text,_DEFAULTS.states['STATE'])
                    return state
            except Exception as e:
                if(debug): print("\n{}\n".format(str(e)))
                return False
        return False

    #works!
    def get(self,**kwargs):
        required = {"action":{"type":str}}
        if(parse_kwargs(required,kwargs)):
            try:
                headers = _DEFAULTS.headers.copy()
                headers['SOAPACTION'] = headers['SOAPACTION'].format(**kwargs)
    
                data = _DEFAULTS.get_xml.format(**kwargs)
    
                #print("{}\n{}\n{}\n\n\n\n".format(self.url,headers,data))
    
                response = requests.get(self.url,headers=headers,data=data,timeout=_DEFAULTS.timeout)

                if(response.status_code == 200):
                    if('name' in kwargs['action'].lower()):
                        search = _DEFAULTS.states['NAME']
                    elif('state' in kwargs['action'].lower()):
                        search = _DEFAULTS.states['STATE']
                    else:
                        return False
                    value = self.parse_xml(response.text,search)
                    return value
            except Exception as e:
                if(debug): print("\n{}\n".format(str(e)))
        else:
            return False

def work3r(**kwargs):
    global devices
        
    ip = kwargs['ip']
        
    x = w3mo(ip=ip)
    
    response = x.get(
        action=_DEFAULTS.actions['GET_STATE'],
        value=1
        )
  
    if(not response):
        pass
        #print("No device at address {}".format(ip))
    else:
        response = x.get(
            action=_DEFAULTS.actions['GET_NAME'],
            value=1
            )
        if(response):
            if(isinstance(devices,dict)):
                print("Device {} | {} initialized".format(response,ip))
                devices[response] = {}
                devices[response]['ip'] = ip
                devices[response]['obj'] = x
            elif(isinstance(devices,list)):
                devices.append({"ip":ip,"name":response,"obj":x})

def discover(**kwargs):
    global devices

    def join():
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        return True

    print("Discovering devices...")
    try:
        if(kwargs['return_type'] == dict):
            devices = {}
        elif(kwargs['return_type'] == list):
            devices = []
    except:
        devices = {}

    try:
        additional_ranges = kwargs['additional_ranges']
    except:
        additional_ranges = []

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        host_ip = s.getsockname()[0]
    except Exception as e:
        s.close()
        print(type(e).__name__,e.args)
        return False

    if(host_ip):
        subnet = '.'.join(host_ip.split(".")[:3])+"."
        for i in range(1,255):
            threading.Thread(target=work3r,kwargs={"ip":subnet+str(i)}).start()

    join()
    
    if(additional_ranges):
        if(isinstance(additional_ranges,list)):
            print("Looking in addtional ranges...")
            for rng in additional_ranges:
                print("{}...".format(rng))
                for i in range(1,255):
                    subnet = '.'.join(rng.split(".")[:3])+"."
                    threading.Thread(target=work3r,kwargs={"ip":subnet+str(i)}).start()
                join()

    print("Dicovery complete!")    
    return devices

def interactive():
    error_counter = 0
    response = False
    found = discover(return_type=list)

    if(not found):
        try:
            ip = str(input("\nPlease enter the IP address of your device: ")).strip()
            if(ip == 'exit'):
                sys.exit()
    
            x = w3mo(ip=ip)
            
            response = x.get(
                action=_DEFAULTS.actions['GET_STATE'],
                value=1
                )
            
            if(not response):
                print("\nNo device at address {}".format(ip))
                sys.exit()
    
            else:
                print("\nDevice {} initialized\n".format(x))
                response = False
            
        except Exception as e:
            print('fail here')
            print(str(e))
    prompt = '''|-------------------------------------------------------------------------------------------------------------------|
| Welcome to W3mo Pwn!                                                                                              |
|-------------------------------------------------------------------------------------------------------------------|
| To control your device just enter a state integer (0=OFF,1=ON)                                                    |
| To get your device power state enter 'state'                                                                      |
| To get your device's friendly name enter 'name'                                                                   |
| To EXIT this prompt enter exit                                                                                    |
| To see this prompt again... enter help or ?                                                                       |
|-------------------------------------------------------------------------------------------------------------------|
| Happy controlling!                                                                                                |
|-------------------------------------------------------------------------------------------------------------------|
'''

    print(prompt)                  


    while True:
        def calc_spaces(index,name):
            TOTAL=112
            out = ""
            for i in range(TOTAL-(len(str(index))+len(name))):
                out+=" "
            return out

        if(found):
            discovery_prompt = '''|-------------------------------------------------------------------------------------------------------------------|
| Device discovery found the following items, please select from the list                                           |
|-------------------------------------------------------------------------------------------------------------------|'''
            print(discovery_prompt)
            for i in range(len(found)):
                print("| {}: {}{}|".format(i,found[i]['name'],calc_spaces(i,found[i]['name'])))
            print("|-------------------------------------------------------------------------------------------------------------------|")


        try:
            term = input('\nw3mo.sh3ll$ ')
            x = found[int(term)]['obj']
        except:
            try:
                if(term.strip().lower() == 'exit'):
                    break
                else:
                    print(prompt)
            except Exception as e:
                print("Failure! {} | {}".format(type(e).__name__,e.args))
        try:
            if(not x):
                print("No device to control!")
                break
                
            value = input('\nw3mo.sh3ll$({}) '.format(x.name))
            response = False
            try:
                value = int(value)
            except:
                if(isinstance(value,str) and value == 'exit'):
                    break

            if(not isinstance(value,bool) and isinstance(value,int)):         
                response = x.control(
                    action=_DEFAULTS.actions['SET_STATE'],
                    state=_DEFAULTS.states['STATE'],
                    value=value
                    )
                if(response):
                    if(response == '1'):
                        current_state = 'ON'
                    else:
                        current_state = 'OFF'
                    print("Success! Your device is: {}\n".format(current_state))
                else:
                    print("Failure!\n")
                error_counter = 0

            elif(value.lower() == 'help' or value == '?'):
                print(prompt)

            elif(not isinstance(value,bool) and isinstance(value,str)):   
                if('name' in value.lower()):
                    action = _DEFAULTS.actions['GET_NAME']
                    ready = True
                elif('state' in value.lower()):
                    action = _DEFAULTS.actions['GET_STATE']
                    ready = True
                else:
                    ready = False
                if(ready):
                    response = x.get(
                        action=action,
                        value=value
                    )
                    if(response):
                        if(response == '1'):
                            current_state = 'ON'
                        elif(isinstance(value,int) or 'state' in value.lower()):
                            current_state = 'OFF'
                        else:
                            current_state = response
                        print("Success! The data you seek is: {}\n".format(current_state))
                    else:
                        print("Failure!\n")
                    error_counter = 0
                else:
                    print("***Command Not Recognized!***")
                    error_counter += 1

            else:
                print("***Command Not Recognized!***")
                error_counter += 1

        except Exception as e:
            error_counter += 1
            print(str(e))

        if(error_counter >= 5):
            print("\nI feel I'm being abused... iniating termination sequence\n")
            break

        value = False
        response = False
        current_state = False


if __name__ == '__main__':
    interactive()