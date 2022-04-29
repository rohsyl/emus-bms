# EMUS BMS

This project is a set of python scripts used to retrieved 
data (about Battery Voltage, Power, Current, Temperature, ...)
through serial ports to **EMUS Battery Managment System**.

Works with **EMUS-G1-BMS-Serial_Protocol-v2.0.13**.

## Getting started

How to install this library

### Clone the repository

Go to your home (or anywhere else that suit you.)

```
cd /home/pi
```

Clone the repository

```
git clone git@github.com:rohsyl/emus-bms.git
```

### Dependencies

Make sure that you have intalled **python3.5** or higher and **pip**.

Install the `pyserial`, `python-dotenv`, `mysql-connector` libraries using pip
```
pip3 install pyserial mysql-connector python-dotenv
```

### Configuration

All configurations are done in the `.env` file.

It this file doesm't exists, you can copy and rename the `.env.exemple` file.

#### Serial port

##### EMUS BMS

**For prod usage**
```
EMUS_SERIAL_VID=...
EMUS_SERIAL_PID=...
```
> Find the vid and pid using the following python code snippet
> ```
> python3.7 -m serial.tools.list_ports -v 
> ```
> It use `pyserial` library that you should have installed earlier.

or

**For dev usage**
```
EMUS_SERIAL_PORT=/dev/ttyUSB4
```
> It's not the default behavior to use this to configure the serial port but it's good for dev.
> 
> Only use for **dev purpose** because in a production environment the 
> `/dev/ttyUSB4` can change over time...


## How to use the library

This section show how to open a connection and request some data.

First, Import dependencies
```
import threading
import sys
from config.config import *
from emus_lib.constants import *
from emus_lib.helpers import *
from emus_lib.serial.emus import EmusSerial
```

Then, you have to defined the sentence you want to read.
> Implemented sentence can be seen in emus_lib/constants.py

If you want to request other sentence, feel free to add them here.
```
SEN_ONLY = [
    SEN_BV1,
    SEN_BV2,
]
```

You have to manually set in how many frames the response to a given sentence will be
provided by the EMUS BMS.

You have to set it manually because it depends on how many cells your battery have.

> See the official documentation of EMUS BMS Serial Protocol for me details about it.
```
SEN_RESPONSE_DEFINITION = {
    SEN_BV1: {'length': 1},
    SEN_BV2: {'length': 2},
}
```

I've decided to setup a queue system to store the reponse because sometimes
responses come in a different order than it was requested and also
it handle timeout if no answer from the EMUS BMS is sent.

Instanciate the response queue manager and pass the response definitions
```
q = ResponseQueue(SEN_RESPONSE_DEFINITION)
```


Open serial connection

> For dev, you can pass the `EMUS_SERIAL_PORT` as first parameter to the `EmusSerial` 
> constructor.
> 
> For prod, you can pass `None` as first parameter to the `EmusSerial` 
> and the `EMUS_SERIAL_VID` and `EMUS_SERIAL_PID` will automatically be used to 
> connect to the serial port.
```
serial = EmusSerial(EMUS_SERIAL_PORT, SEN_ONLY, SEN_RESPONSE_DEFINITION)
# serial.set_logger('emus')
serial.open()
serial.set_queue(q)
```

We use another thread to read data in a non-blocking way.

Start to read to the serial port to be ready to get responses from the BMS.
```
thread = threading.Thread(target=serial.read, args=[False])
thread.start()
```

Send a request for each sentences.
```
for request in SEN_RESPONSE_DEFINITION.keys():
    serial.write(request)
```

Wait until we have all responses or it's timed out (if timeout is configured)
```
while not q.is_queue_processed() and not q.has_timed_out():
    pass
```

Close serial connection
```
serial.close()
```

Access do data : 
```
items = q.get_items()
```

And now you can loop though these items and do whatever you want with these data !

You can see emus.py for an exemple.

> This exemple works ONLY when the EMUS BMS is NOT in Broadcast mode !

If you want to work with the broadcast mode enable, you just need to change to following line
```
thread = threading.Thread(target=serial.read, args=[False])
```

Into
```
thread = threading.Thread(target=serial.read_broadcast, args=[False])
```

> Also keep in mind that in broadcast mode, the EMUS BMS is just broadcasting some sentences through the serial port.
>
> That means that you can't send request to the EMUS BMS and also you can access all sentences. See EMUS BMS documentations for more
> details about this.

## Exemple

- `emus.py` : Get data by sending request and waiting for responses.
- `emus_broadcast.py` : Read broadcasted data.

## Extra features

### Locker

The locker will simply create a file that will say that the given resource is in use.

For this exemple resource name is `emus`. So the created file is named emus.LOCK.

Check if a resource is locked and wait until it's unlocked
```
while Locker.is_locked('emus'):
    pass
```
> Default lock timeout is 2 seconds, you can change it by passing it as 2nd parameter to
> the `is_locked` method

Lock a resource
```  
Locker.lock('emus')
``` 

Unlock a resource
```  
Locker.unlock('emus')
```

### Logger

you can init a logger using the following function

```
from emus_lib.helpers import *

logger = init_logging('emus')
```

## Available sentence

This library provide support for the following sentences :
- `BB1`
- `BB2`
- `BC1`
- `BT1`
- `BT2`
- `BT3`
- `BT4`
- `BV1`
- `BV2`
- `CV1`
- `VR1`
- `DT1`
- `ST1`
- `OT1`

## Logs

Log file are located under `/home/pi/homepy/log`. There is a file for each script.


## Contributors
- Sylvain Roh
