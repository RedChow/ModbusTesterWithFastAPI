# ModbusTesterWithFastAPI
Using FastAPI along with pymodbus allows us to write a user interface in any language that supports sending/receiving HTTP requests.

## General Notes
* Any machine that speaks modbus should be able to connect to the modbus server.
* HTTP requests need to have Content-Type specified as 'application/json.' Additionally, JSON data needs to have the entries listed in json_models.py and must be of the type specified. The examples below illustrate write and read requests. Although urllib2 has been split across different modules in Python 3, it's used here for brevity and for users of Jython and older versions of Python.
* FUNCTION_MAP in modbus_server.py contains the expected register names.
* This has been tested against more than 6 Siemens PLCs simultaneously connected to the modbus server with each PLC reading/writing more than 200 points/second. Interface using Jython's urllib2 posed no problems sending/receiving modbus information.
* I've written interfaces in Ignition, PySide2, and Qt. I hope to upload those UI designs and files in the future.

## Write Example using urllib2
```Python
import urllib2
import json

register_type = 'holding_registers'
data = json.dumps({'register_type': register_type, 'address': 3, 'unit_id': 1, 'values': [2, 4, 66, 1]})
data_length = len(data)
req = urllib2.Request('http://127.0.0.1:8000/write', data, {'Content-Type': 'application/json', 'Content-Length': data_length})
urllib2.urlopen(req)

```

## Read Example using urllib2
```Python
import urllib2
import json

data = json.dumps({'register_type':'discrete_inputs', 'starting_address':sa, 'unit_id':unit_id, 'quantity':q})
data_length = len(data)
req = urllib2.Request('http://127.0.0.1:8000/get', data, {'Content-Type': 'application/json', 'Content-Length': data_length})
f = urllib2.urlopen(req)
json_data = json.loads(f.readlines()[0])
for i, v in enumerate(json_data['values']):
  #do something with the value v; sa + i will be the register to which v corresponds
  pass
```
