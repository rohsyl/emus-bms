# Home Py

This project is a set of python scripts used to retrieved data (about Battery Voltage, Power, Current, Temperature, ...) through serial ports **EMUS Battery Managment System**.

These script are used to retrive data and store them to a database.

## Getting started

How to install and run all these scripts

### Clone the repository

Go to your home

```
cd /home/pi
```

Clone the repository

```
git clone git@github.com:rohsyl/emus-bms.git
```

### Dependencies

Install the `pyserial`, `python-dotenv`, `mysql-connector` and `asyncio` libraries
```
pip3 install pyserial mysql-connector websockets asyncio python-dotenv
```

### Configuration

All configurations are done in the `.env` file.

It this file doesm't exists, you can copy and rename the `.env.exemple` file.

#### Serial port


##### EMUS BMS

```
EMUS_SERIAL_PORT=/dev/ttyUSB1
```

#### Database

```
DB_HOST=localhost
DB_NAME=homepy
DB_USER=user
DB_PASS=pass
```

> See here how to install the database

#### Websocket (optional)

```
WS_LISTEN_PORT=5000
```

##### Normal

```
WS_SECURE=False
WS_CERT_PEM=
```

##### Secure

```
WS_SECURE=True
WS_CERT_PEM=/etc/letsencrypt/live/wss.rohs.ch/fullchain.pem
```

### Executable

There is many different scripts 


#### emus.py - Battery life

This script get data about battery cells though serial connection to EMUS BMS.

- Min cell and his value
- Max cell and his value
- Total
- Average

And then save those value to the database as JSON in the `emus` table


##### Run manually

For testing and dev purpose you can manually run this script by typing the following command:

```
python3.5 emus.py
```


##### Run with CRON

For procduction, we run this script with a cron job

- Every day at 7h
- Every day at 17h

To do that, we create a CRON job.

Edit the crontab by typing the following command:

```
crontab -e
```

And add the following lines at the end of the file:

```
0 7 * * * python3.5 /home/pi/homepy/emus.py
0 17 * * * python3.5 /home/pi/homepy/emus.py
```

## Logs

Log file are located under `/home/pi/homepy/log`. There is a file for each script.


## Contributors
- Sylvain Roh
