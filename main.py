# main.py
# Copyright (c) 2023 Mooshwerks
# All Rights Reserved
#
# Experimenting with the tago.io API and He_003 water level
# sensor at E. Mifflin and Blount St. in Madison, WI.

import math
import base64
import requests
import numpy as np
from tagoio_sdk import Device

def lat(location):
    return location[0]


def lon(location):
    return location[1]


def get_device_info(token):
    myDevice = Device({"token": token})
    result = myDevice.info()

    payload = result["payload_decoder"]
    decoded = base64.standard_b64decode(payload)
    decoded = decoded.decode('UTF-8')
    print(decoded)


def get_device_data(token):
    myDevice = Device({ "token": token})
    result = myDevice.getData({
        "query": "last_item",
        "variable": "frequency",
    })
    print(result)


def get_device_location(token):
    myDevice = Device({ "token": token})
    result = myDevice.getData({
        "query": "last_item",
        "variable": "location",
    })

    # coordinates coming from the device are in [lon, lat] order. OSM and Google
    # maps take values in [lat, lon] order, so do the switch here to avoid
    # having to do it everywhere the location is used.
    location = result[0]['location']['coordinates']
    location = [location[1], location[0]]
    return location


def meters_to_latitude_degrees(current_lat, distance_meters):
    if distance_meters == 0:
        return 0
    
    # values taken from https://en.wikipedia.org/wiki/Geographic_coordinate_system#Latitude_and_longitude
    deg = distance_meters / (111132.92 - 559.82 * math.cos(2*current_lat)
           + 1.175 * math.cos(4*current_lat) 
           - 0.0023 * math.cos(6*current_lat))
    return deg


def meters_to_longitude_degrees(current_lon, distance_meters):
    if distance_meters == 0:
        return 0
    
    # values taken from https://en.wikipedia.org/wiki/Geographic_coordinate_system#Latitude_and_longitude
    deg = distance_meters / (111412.84 * math.cos(current_lon)
           - 93.5 * math.cos(3*current_lon) 
           + 0.118 * math.cos(5*current_lon))
    return deg


def location_at_distance(location, meters_lat, meters_lon):
    delta_degrees_lat = meters_to_latitude_degrees(lat(location), meters_lat)
    delta_degrees_lon = meters_to_latitude_degrees(lon(location), meters_lon)
    return [lat(location) + delta_degrees_lat, lon(location) + delta_degrees_lon]


def get__device_elevation(token):
    query = f"https://api.open-elevation.com/api/v1/lookup?locations=41.161758,-8.583933"


def get_osm_url(coords, zoom_level):
    url = f"http://www.openstreetmap.org/?mlat={coords[0]}&mlon={coords[1]}&zoom={zoom_level}"
    return url


def main():
    token = "ba8d3764-1dc8-46ca-80ca-54aa3aec3297" # He_003 sensor on Bill's tago.io dashboard
    #get_device_info(token)
    #get_device_data(token)
    device_location = get_device_location(token)
    orig_url = get_osm_url(device_location, 19)

    moved_location = location_at_distance(device_location, 1, 1)
    moved_url = get_osm_url(moved_location, 19)

    print(orig_url)
    print(moved_url)


main()