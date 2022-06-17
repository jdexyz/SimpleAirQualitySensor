# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example of publishing the value of an ADC to Adafruit IO
# adafruit_circuitpython_adafruitio with an esp32spi_socket


import ssl
import wifi
import socketpool
import adafruit_requests
from secrets import secrets
from adafruit_magtag.magtag import MagTag
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
import time 



def connect_to_internet():
    if(not wifi.radio.ipv4_gateway):
        print("Available WiFi networks:")
        for network in wifi.radio.start_scanning_networks():
            print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                    network.rssi, network.channel))
        wifi.radio.stop_scanning_networks()

        print("Connecting to %s"%secrets["ssid"])
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("Connected to %s!"%secrets["ssid"])

def send_to_feed(feed, value):
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    # Set your Adafruit IO Username and Key in secrets.py
    # (visit io.adafruit.com if you need to create an account,
    # or if you need your Adafruit IO key.)
    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]

    # Initialize an Adafruit IO HTTP API object
    io = IO_HTTP(aio_username, aio_key, requests)

    try:
        # Get the 'light' feed from Adafruit IO
        feed = io.get_feed(feed)
    except AdafruitIO_RequestError:
        # If no 'light' feed exists, create one
        feed = io.create_new_feed(feed)
    print('Sending to feed', feed, value)
    io.send_data(feed["key"], value)
    print('Sent')

def send_battery_level(level):
    send_to_feed("magtag-battery", level)