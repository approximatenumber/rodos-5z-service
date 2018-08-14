#!/usr/bin/env python

import sys
import subprocess
import time
import re
from influxdb import InfluxDBClient

INTERVAL = 60

INFLUX_HOST = '2334.bazookatrip.xyz'
INFLUX_PORT = 8086
INFLUX_USER = 'engine'
INFLUX_PASS = 'engine'
INFLUX_DB = 'office_temp'

SENSOR_ID = 'ca031761d4daff28'


def insert_influx(temp, sensor_id="unknown"):
    client = InfluxDBClient(host=INFLUX_HOST,
                            port=INFLUX_PORT,
                            username=INFLUX_USER,
                            password=INFLUX_PASS)
    databases = [db['name'] for db in client.get_list_database()]
    if INFLUX_DB not in databases:
        print('Database {db} not found.'.format(db=INFLUX_DB))
        if not client.create_database(INFLUX_DB):
            print('Cannot create database {db}.'.format(db=INFLUX_DB))
            sys.exit(1)
        print('Database {db} created.'.format(db=INFLUX_DB))
    client.switch_database(INFLUX_DB)
    # Writing weather information
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "sensor-id": SENSOR_ID
            },
            "fields": {"temp": float(temp)}
        }
    ]
    if not client.write_points(json_body):
        print('Cannot write weather data into database!')
        sys.exit(1)


def main():
        while True:
            proc = subprocess.Popen(['./bmcontrol', 'temp', SENSOR_ID],
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
            try:
                out = proc.stdout.readline().rstrip('\n ')
                temp = float(re.search('[0-9]+.[0-9]+', out).group())
                insert_influx(temp, sensor_id=SENSOR_ID)
                print("Written to influx: %f" % temp)
            except (ValueError, TypeError, AttributeError):
                print("incorrect data!")
            proc.communicate()
            time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
