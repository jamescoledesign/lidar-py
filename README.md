# lidar-py
This program allows you to access raw data from LIDAR modules connected to serial ports via microcontrollers. The program can access any raw data printed to the serial monitor, but is currently designed to parse LIDAR data from the Garmin and RP Lidar modules.

Once data has been collected or imported, the program will render a basic point cloud plot or an interactive plot.

## Supported LIDAR modules: 

1. Garmin
2. RP Lidar

## Instructions

### 1. Install packages
#### For all: 
- pySerial: ```pip install pyserial```
- pandas:  ```pip install pandas```
- Matplotlib: ```pip install matplotlib```
- numpy: ```pip install numpy```
- PyVista: ```pip install pyvista```
- PyVistaQt: ```pip install pyvistaqt```

#### If using RP Lidar A1
- rplidar: ```pip install rplidar-roboticia```

### 2. Import packages

### 3. Run scan or Import data
#### Run scan 
- Get serial port information 
- Declare ports 
- Scan
- Clean data
- Export data (optional)

#### Import data
- Select file path

### 4. Plot point cloud using PyVista
- Create basic plot
- Create interactive plot



