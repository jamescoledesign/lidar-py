#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:39:46 2023

@author: jamescole
"""

import re
import time
import pandas as pd
from rplidar import RPLidar
import serial
import serial.tools.list_ports
import math
import matplotlib.pyplot as plt
from pathlib import Path
import os
import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter

# Lidar
#PORT_1 = serial.Serial'/dev/cu.usbmodemDC5475C4BCD02', 115200)  
PORT_1 = "Placeholder1"
# Servos
#PORT_2 = serial.Serial('/dev/cu.usbserial-110', 115200)  
PORT_2 = "Placeholder2"

# # Set plot theme styles
# pv.global_theme.background = 'black'
# pv.global_theme.font.color = 'grey'

def show_ports():
    # List serial ports
    ports = list(serial.tools.list_ports.comports())
    for item in ports:
        print( item.name )
        print( item.description )
        print( item.hwid )
        print( item.vid )
        print( item.pid )
        print( item.serial_number )
        print( item.location )
        print( item.manufacturer )
        print( item.product )
        print( item.interface )

    
def check_ports(p1, p2):
    # Check ports
    if p1 and p2:
        print("Ports connected")
        run = True
    else: 
        print("Error: please connect devices")
        
# Listen to serial ports and combine in a DataFrame
run = False
data = []
scanTime = 0

def newLidar():
    print("Scanning...")
    while run:
        new_row = []
        lidar = PORT_1.readline()
        new_row.append(lidar)
        servos = PORT_2.readline()
        new_row.append(servos)

        if servos == b'000\r\n':
            print("——————————————————————————————")
            print("        Scan complete")
            print("——————————————————————————————")
            break
        else:
            data.append(new_row)
            print(new_row)   

xyz = pd.DataFrame(
    {'x': 0,
     'y': 1,
     'z': 2
        }, 
    index=[0])

def import_data(device):

    # Import data
    df = pd.read_csv('./data/raw-sensor-data-livingRoom.csv')
    df.head()
    
    # Make DF with xyz values
    df_copy2 = df.copy()
    df_copy2["1"] = df_copy2["1"].astype(str).str.split('\t')
    df_copy2["2"] = 0
    xvals = []
    yvals = []
    zvals = []
    df_copy2.tail()
    
    for i in df_copy2["1"]:
        x = i[0]
        y = i[1]
        xvals.append(x)
        yvals.append(y)
    
    for i in df_copy2["0"]:
        zvals.append(i)
    
    xyz = pd.DataFrame(
        {'x': xvals,
         'y': yvals,
         'z': zvals
        })

    print(xyz.head())

import_data("garmin")


# Get spherical coordinates
def make_spherical(xpos, ypos, distance):
    # Variables
    # xpos = servo yaw angle between 0 and 180
    # ypos = lidar pitch angle between 0 and 360
    # distance = lidar distance reading
    pi = math.pi

    theta = float((xpos * pi) / 180)  # pan servo
    phi = float((ypos * pi) / 180)  # tilt servo

    z = distance * math.sin(phi)
    x = z * math.cos(phi) * math.cos(theta)
    y = z * math.cos(phi) * math.sin(theta)
    
    return [x, y, z]


# Get angle and distance
new_data = []

for index, row in xyz.iterrows():
    # print(row[0], row[1])
    new_row = []

    z = float(row[2])
    new_row.append(z)

    y = float(row[1])
    new_row.append(y)
    
    x = float(row[0])
    new_row.append(x)
    
    spherical_data = make_spherical(new_row[2], new_row[1], new_row[0])
    new_row = spherical_data

    new_data.append(new_row)
    
point_cloud_data = pd.DataFrame(new_data)
point_cloud_data = point_cloud_data.rename(columns={0: "x", 1: "y", 2: "z"})
point_cloud_data.head()

# Convert data for PyVista
points = point_cloud_data.to_numpy()
points

# Create point cloud
point_cloud = pv.PolyData(points)


# Basic plot
pl = pv.Plotter(notebook=False)
pl.add_mesh(point_cloud, 
            render_points_as_spheres = True,
            scalars = points[:, 2],
            point_size = 2,
            show_scalar_bar = False,
            )
camera = pv.Camera()
pl.camera = camera
pl.camera_position = 'yz'
pl.window_size = [800, 400]
pl.camera.azimuth = 45
pl.add_axes()
pl.show()













