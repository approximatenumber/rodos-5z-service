### USB-thermometer RODOS-5Z As a Service.

Here is example how to use USB-dongle RODOS-5Z with MP707 sensor to control indoor temperature and visualize it with 
web-based services like Grafana+InfluxDB.

1. Configuration on remote host (aka web-server):

* Copy `service/` to server
* Install `docker`
* Configure `env` section in `docker-compose.yaml` for both services `grafana` and `db`
* Create services and start them: `docker-compose up -d grafana db`
* Okay, now your server is ready to receive data: there is listening `influxdb`-service on port 8086, which recieve data from client and `grafana`-service which visualize that data


2. Configuration on Host with RODOS connected:

* Put udev-rule `99-rodos.rules` to `/etc/udev/rules.d` to set correct rights to access the dongle.

* Compile `bmcontrol` or use compiled version.

* Check that `bmcontrol` works normally: 

```bash
./bmcontrol scan
sensor 1 = ca031761d4daff28
```

```bash
./bmcontrol temp ca031761d4daff28
27.543
```

* Set you sensor id with `SENSOR_ID` var in `service/engine/engine.py`

* Configure `engine`-service in `docker-compose.yaml` to be able to connect to database (`db`) on remote host

* Create and start service `engine`: `docker-compose up -d engine`

* Okay, now your service gets temperature and writes it to InfluxDB on remote host

* Go to `http://office_temp.your.site:3000` (or whatever you have server configuration is...) and configure Grafana to visualize data from database:

![grafana example](/grafana.png)
