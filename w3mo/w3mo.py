import sys
import requests

class _DEFAULTS():
    headers={
            'User-Agent': '',
            'Accept': '',
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': '\"urn:Belkin:service:basicevent:1#{action}\"',
    }
    
    actions = {"GET_STATE":"GetBinaryState",
                    "SET_STATE":"SetBinaryState",
                    "GET_NAME":"GetFriendlyName"}

    states = {"BINARY_STATE":"BinaryState"}
    
    port = 49153

    

    base_url = 'http://{device}:{port}/upnp/control/basicevent1'.format(device = "{device}",port=port)

    xml_body = '''
        <?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:{action} xmlns:u="urn:Belkin:service:basicevent:1">
                    <{state}>{value}</{state}>
                </u:{action}
            ></s:Body>
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
            
    def control(self,**kwargs):
        required = {"action":{"type":str},"state":{"type":str},"value":{"type":int}}
        if(parse_kwargs(required,kwargs)):
            headers = _DEFAULTS.headers
            headers['SOAPACTION'] = headers['SOAPACTION'].format(**kwargs)

            data = _DEFAULTS.xml_body.format(**kwargs)

            print("{}\n{}\n{}\n\n\n\n".format(self.url,headers,data))

            response = requests.post(self.url,headers=headers,data=data)
            print(response)
            print(response.text)

    #works!
    def get(self,**kwargs):
        required = {"action":{"type":str},"state":{"type":str},"value":{"type":int}}
        if(parse_kwargs(required,kwargs)):
            headers = _DEFAULTS.headers
            headers['SOAPACTION'] = headers['SOAPACTION'].format(**kwargs)

            data = _DEFAULTS.xml_body.format(**kwargs)

            print("{}\n{}\n{}\n\n\n\n".format(self.url,headers,data))

            response = requests.get(self.url,headers=headers,data=data)
            print(response)
            print(response.text)

if __name__ == '__main__':

    error_counter = 0
    
    try:
        ip = str(input("Please Enter The IP Address Of Your Device: ")).strip()
        if(ip == 'exit'):
            sys.exit()
        x = w3mo(ip=ip)
    except Exception as e:
        print(str(e))

    while True:
        try:
            value = input("Please Enter The Desired State (0=OFF,1=ON): ")
            try:
                value = int(value)
            except:
                if(isinstance(value,str) and value == 'exit'):
                    break
                print("Entry Not An Integer!\n")
                error_counter += 1
                value = False   

            '''
            if(not isinstance(value,bool)):         
                x.control(
                    action=_DEFAULTS.actions['SET_STATE'],
                    state=_DEFAULTS.states['BINARY_STATE'],
                    value=value
                )
                error_counter = 0
            '''
            if(not isinstance(value,bool)):         
                x.get(
                    action=_DEFAULTS.actions['GET_STATE'],
                    state=_DEFAULTS.states['BINARY_STATE'],
                    value=value
                )
                error_counter = 0
                
            else:
                print("no value...")
                error_counter += 1

        except Exception as e:
            error_counter += 1
            print(str(e))

        if(error_counter >= 5):
            print("Terminating...")
            break















    