import RPi.GPIO as GPIO
import time
import read_temp as temp
import plot_graph as plot
import mqtt_module as mqtt

# Setup GPIO for Peltier element
GPIO.setmode(GPIO.BCM)
PELTIER_PIN = 21
GPIO.setup(PELTIER_PIN, GPIO.OUT)

# Set DS18B20 id values 
water_sensor_id = '28-0b237359ef33'
room_sensor_id = '28-6102d446c2cf'

# Connect to MQTT topics
mqtt.connect_and_subscribe()

# Set temperature reference and tolerance (Celcius)
temp_tolerance = 0.5 

# Make arryas for time and water temperature 
timestamps = []
water_temp_val = []

try:
    time_start = time.time()
    while True:
        if mqtt.program_state():
            
            # Read temperatures
            water_temp = temp.read_temp(water_sensor_id)
            room_temp = temp.read_temp(room_sensor_id)
        
            # Publish temperatures to Node-RED GUI
            mqtt.publish(mqtt.temp_room_topic, room_temp)
            mqtt.publish(mqtt.temp_water_topic, water_temp)

            print(f"Water Temperature: {water_temp}C, Room Temperature: {room_temp}C ")
        
            # Log values for time and water temperature
            time_val = time.time() - time_start
            timestamps.append(time_val)
            water_temp_val.append(water_temp)
        
            # Get current temperature referense from GUI
            temp_ref = mqtt.get_temp_ref()
            
            # On-off control Peltier 
            if water_temp < temp_ref - temp_tolerance:
                GPIO.output(PELTIER_PIN, GPIO.HIGH)
                print("Peltier ON")
            elif water_temp > temp_ref + temp_tolerance:
                GPIO.output(PELTIER_PIN, GPIO.LOW)
                print("Peltier OFF")
            else:
                print("Temperature within reference range, Peltier remains unchanged")

        time.sleep(2)

except KeyboardInterrupt:
    print("Terminating program...")

finally:
    GPIO.cleanup()
    mqtt.disconnect()
    graph = plot.plot_graph(timestamps, water_temp_val, temp_ref)
