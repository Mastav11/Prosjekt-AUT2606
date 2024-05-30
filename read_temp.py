import os
import glob
import time

# Function for raw temperature data from DS10b20
def read_temp_raw(sensor_id):
    base_dir = '/sys/bus/w1/devices/'
    device_file = os.path.join(base_dir, sensor_id, 'w1_slave')
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

# Function for converting raw data value to degrees Celsius
def read_temp(sensor_id):
    lines = read_temp_raw(sensor_id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensor_id)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c