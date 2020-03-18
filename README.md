# Home Py

This project is a set of python scripts used to retrieved data (about Battery Voltage, Power, Current, Temperature, ...) through serial ports to **Studer Innotec Xtender System** and **EMUS Battery Managment System**.

These script are used to retrive data and store them to a database or serve them through a websocket.

## Getting started

How to install and run all these scripts

### Clone the repository

Go to your home

```
cd /home/pi
```

Clone the repository

```
git clone git@github.com:rohsyl/homepy.git
```

### Dependencies

Install the `pyserial`, `python-dotenv`, `mysql-connector`, `websockets` and `asyncio` libraries
```
pip install pyserial mysql-connector websockets asyncio python-dotenv
```

### Configuration

All configurations are done in the `.env` file.

It this file doesm't exists, you can copy and rename the `.env.exemple` file.

#### Serial port

##### StuderInnotec Xtender

```
STUDER_SERIAL_PORT=/dev/ttyUSB3
```

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

#### Websocket

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

#### main.py - StuderInnotec Xtender

This script connect through the serial port to the StuderInnotec Xtender to get data about battery.

- Current Battery Voltage
- Battery Power
- Battery SOC
- ...

Then those data are stored to the database in the `datas` table. (See here how to install the database).

##### Run manually

For testing and dev purpose you can manually run this script by typing the following command:

```
python3.5 main.py
```

> While testing or dev, be sure the CRON job is down !

##### Run with CRON

For production, we need to run periodically this script to get data (ie. each minutes).

To do that, we create a CRON job.

Edit the crontab by typing the following command:

```
crontab -e
```

And add the following line at the end of the file to run the script each minutes:

```
* * * * * python3.5 /home/pi/homepy/main.py
```

#### service_socket.py - Livedata websocket

This script serve a websocket and give data about EMUS BMS.

Port is **5000**.

##### Run manually

For testing and dev purpose you can manually run this script by typing the following command:

```
python3.5 service_socket.py
```

##### Systemd service

For production, this will run as a linux systemd service. 

###### Create a service

- Create a new .service file
```
sudo nano /etc/systemd/system/homepyemus.service
```

- Set the content of the file
```
[Unit]
Description=HomePy - Emus BMS

[Service]
Type=simple
Restart=always
RestartSec=5
User=pi
ExecStart=/usr/bin/python3.5 /home/pi/homepy/service_socket.py

[Install]
WantedBy=multi-user.target
```

###### Enable the autostart

```
sudo systemctl enable homepyemus
```

###### Start the service

```
sudo systemctl start homepyemus
```

###### Stop the service

```
sudo systemctl stop homepyemus
```

###### Restart the service

```
sudo systemctl restart homepyemus
```


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
