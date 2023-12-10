import serial
import serial.tools.list_ports
import time
from rplidar import RPLidar
import pandas as pd
import pyvista as pv
from pyvistaqt import BackgroundPlotter
import math
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from pathlib import Path


def menu(version):
    if version == 1:
        print("——————————————————————————————")
        print("            Home")
        print("——————————————————————————————")
        print(" ")
        print("[1] Get serial port info")
        print("[2] Run scan")
        print("[3] Import Data")
        print("[4] Exit")
        print(" ")
    elif version == 2:
        print("——————————————————————————————")
        print("           Import")
        print("——————————————————————————————")
        print(" ")
        print("[1] raw-sensor-data-livingRoom.csv")
        print("[2] raw-sensor-data-office.csv")
        print("[3] Go back")
        print("[4] Exit")
        print(" ")
    elif version == 3:
        print("——————————————————————————————")
        print("            Plot")
        print("——————————————————————————————")
        print(" ")
        print("[1] Create basic plot")
        print("[2] Create interactive plot")
        print("[3] Go back")
        print("[4] Exit")
        print(" ")


# Show serial port information
def show_ports():
    ports = list(serial.tools.list_ports.comports())
    for item in ports:
        print(item.name)
        print(item.description)
        print(item.hwid)
        print(item.vid)
        print(item.pid)
        print(item.serial_number)
        print(item.location)
        print(item.manufacturer)
        print(item.product)
        print(item.interface)
    print("—— End serial port info ——")


# Import data
def import_data():
    menu(2)
    data_path = int(input("Select a file: "))
        
    if data_path == 1:
        print("Importing...")
        df = pd.read_csv("./data-exports/raw-sensor-data-livingRoom.csv")
        
        # Make DF with xyz values
        df_copy2 = df.copy()
        df_copy2["1"] = df_copy2["1"].astype(str).str.split('\t')
        df_copy2["2"] = 0
    
        xvals = []
        yvals = []
        zvals = []
        df_copy2.tail()
    
        # Place into correct cols
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
        print(u"\u2713 Data import complete")
        print("Length: " + str(len(xyz)) + " rows")

        return xyz
        
    elif data_path == 2:
        print("Importing...")
        df = pd.read_csv("./data-exports/raw-sensor-data-office.csv")
        for index, row in df.iterrows():
            if re.search("^b", row[0]):
                move = row[0]
                row[0] = row[1]
                row[1] = move
        
        # last_row = len(df)
        # df = df.drop([last_row])
        
        print("Cleaning...")
        # Get angle and distance
        new_data = []
        tilt = df["1"]  # change index to "1" (str) if importing data 
                
        df_copy2 = df.copy()
        for index, row in df.iterrows():
            new_row = []
        
            measurement = re.split("\t", row[0])
        
            distance = float(measurement[3])
            new_row.append(distance)
        
            angle = float(measurement[2])
            new_row.append(angle)
            
            tilt = re.search("\d{1,3}", row[1])
            if tilt:
                number = float(tilt.group(0))
                new_row.append(number)
                
            new_data.append(new_row)
            
        xyz = pd.DataFrame(new_data)
        xyz = xyz.rename(columns={0: "x", 1: "y", 2: "z"})  
        
        print(xyz.head())
        print(u"\u2713 Data import complete")
        print("Length: " + str(len(xyz)) + " rows")

        return xyz

            
    elif data_path == 3:
        print("Going back")
        

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


def basic_plot():
    # Basic plot
    pl = pv.Plotter(notebook=True)
    pl.add_mesh(point_cloud,
                render_points_as_spheres=True,
                scalars=points[:, 2],
                point_size=2,
                show_scalar_bar=False,
                )
    camera = pv.Camera()
    pl.camera = camera
    pl.camera_position = 'xz'
    pl.window_size = [400, 300]
    pl.show()


def interactive_plot():
    rgba = points - points.min(axis=0)
    rgba /= rgba.max(axis=0)

    plotter = BackgroundPlotter()
    plotter.add_mesh(point_cloud, scalars=rgba, rgba=True, point_size=3)

    plotter.add_axes()


run = True
while run:
    try:
        menu(1)
        selection = int(input("Make a selection: "))
        if selection == 1:
            show_ports()
        elif selection == 3:

            # Get angle and distance
            xyz = import_data()
            new_data = []

            for index, row in xyz.iterrows():
                new_row = []

                z = float(row[2])
                new_row.append(z)

                y = float(row[1])
                new_row.append(y)

                x = float(row[0])
                new_row.append(x)

                spherical_data = make_spherical(
                    new_row[2], new_row[1], new_row[0])
                new_row = spherical_data

                new_data.append(new_row)

            point_cloud_data = pd.DataFrame(new_data)
            point_cloud_data = point_cloud_data.rename(
                columns={0: "x", 1: "y", 2: "z"})
            point_cloud_data.head()

            # Convert data for PyVista
            points = point_cloud_data.to_numpy()

            # Create point cloud
            point_cloud = pv.PolyData(points)

            # Set plot theme styles
            pv.global_theme.background = 'black'
            pv.global_theme.font.color = 'grey'

            menu(3)

            visual = int(input("Make a selection: "))

            if visual == 1:
                basic_plot()
                run = False
            elif visual == 2:
                interactive_plot()
                run = False
            elif visual == 3:
                print("Going back")
            elif visual == 4:
                run = False
            else:
                print("Enter 1, 2, or 3")

        elif selection == 4:
            run = False

    except ValueError:
        print("Please enter 1, 2, or 3")