# 
# main.py
# Copyright (c) 2023 Mooshwerks
# All Rights Reserved
#
# Experimenting with the tago.io API and He_003 water level
# sensor at E. Mifflin and Blount St. in Madison, WI.

import math
import json
import base64
import requests
import numpy as np
from tagoio_sdk import Device
from stopwatch import stopwatch
from matplotlib import pyplot as plt

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
        "variable": "water_level",
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


def location_from(location, meters_lat, meters_lon):
    delta_degrees_lat = meters_to_latitude_degrees(lat(location), meters_lat)
    delta_degrees_lon = meters_to_latitude_degrees(lon(location), meters_lon)
    return [lat(location) + delta_degrees_lat, lon(location) + delta_degrees_lon]


def elevations_around_location(location, extent_x1_blocks, extent_x2_blocks, resolution):
    endpoint = f"http://localhost/api/v1/lookup"
    post_json = {"locations": []}
    for block in range(extent_x1_blocks, extent_x2_blocks + 1):
        delta_meters = block * resolution
        loc = location_from(location, 0, delta_meters) # x-direction, ie longitude, only!
        location_json = {"latitude":lat(loc), "longitude":lon(loc)}
        post_json["locations"].append(location_json)

    out_locations = []

    str = json.dumps(post_json)
    response = requests.post(endpoint, json = post_json)
    response_json = response.json()
    for i in range(0, len(response_json['results'])):
        out_locations.append(response_json['results'][i]['elevation'])

    return out_locations


def get_location_elevation(location):
    #endpoint = f"https://api.open-elevation.com/api/v1/lookup?locations={lat(location)},{lon(location)}"
    endpoint = f"http://localhost/api/v1/lookup?locations={lat(location)},{lon(location)}"
    #print(endpoint)
    response = requests.get(endpoint)
    response_json = response.json()
    return response_json['results'][0]['elevation']


def get_osm_url(coords, zoom_level):
    url = f"http://www.openstreetmap.org/?mlat={coords[0]}&mlon={coords[1]}&zoom={zoom_level}"
    return url


def percent_done_string(current_value, min_value, max_value):
    pct_done = int(100 * (current_value - min_value) / (max_value - min_value))
    progress_bar = ''.join(['=' * pct_done])
    return f"[{progress_bar:100}]" # lock it 100 characters wide


def main_doof():
    x = -8
    res = 3

    xabs = abs(x)
    xsgn = np.sign(x)
    m = xsgn * math.floor((xabs + 0.5 * (res-1))/ res)

    xabs = abs(x)
    xfloor = math.floor(xabs)
    xsign = np.sign(x)
    xremainder = math.fmod(xfloor, res)
    xres = xsign * math.floor(xremainder * res)

    xdivres = xfloor/res
    print(xres)

def main():
    token = "ba8d3764-1dc8-46ca-80ca-54aa3aec3297" # He_003 sensor on Bill's tago.io dashboard
    
    print("--- output device info ---")
    out = get_device_data(token)
    print(out)
    print("--------------------------")

    device_location = get_device_location(token)
    orig_url = get_osm_url(device_location, 19)

    moved_location = location_from(device_location, 10, 0)
    moved_url = get_osm_url(moved_location, 19)

    sw = stopwatch()

    sw.start()
    device_elevation = get_location_elevation(device_location)
    sw.stop()
    print(f"time to query one location's elevation: {sw.elapsedMilliseconds():.3f}ms")

    moved_elevation = get_location_elevation(moved_location)

    radius_in_blocks = 100 # radius around device location (in resolution "blocks")
    resolution_meters = 10
    map_size = 2 * radius_in_blocks + 1
    elevation_map = np.zeros((map_size, map_size))
    for y_block in range(-radius_in_blocks, radius_in_blocks + 1):
        sw.stop()
        pct_done = percent_done_string(y_block, -radius_in_blocks, radius_in_blocks)
        print(f"{pct_done} {map_size / sw.elapsedSeconds()} queries/sec")
        sw.start()

        y_loc = location_from(device_location, y_block * resolution_meters, 0)
        row_elevations = elevations_around_location(y_loc, -radius_in_blocks, radius_in_blocks, resolution_meters)
        for i in range(0, len(row_elevations)):
            elevation_map[y_block + radius_in_blocks][i] = row_elevations[i] - device_elevation

    # level_in_meters = 1
    # for y in range(0, map_size):
    #     for x in range(0,map_size):
    #         if elevation_map[y][x] > device_elevation + level_in_meters:
    #             elevation_map[y][x] 


    elevation_map = np.flipud(elevation_map)
    plt.imshow(elevation_map, interpolation='nearest')
    plt.plot(map_size/2, map_size/2, marker='*', color="white")
    plt.show()

    print(orig_url)
    print(moved_url)
    print(device_elevation)
    print(moved_elevation)


main()