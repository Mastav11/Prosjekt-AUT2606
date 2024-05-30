import paho.mqtt.client as mqtt

# MQTT settings
broker = "localhost"
port = 1883
# Set topics
temp_room_topic = "temp/room"
temp_water_topic = "temp/water"
temp_ref_topic = "temp/ref"
control_topic = "program/control"

# Default states and values
temp_ref = 25.0  
program_running = False

def on_message(client, userdata, message):
    global temp_ref, program_running
    topic = message.topic
    payload = message.payload.decode("utf-8")

    if topic == temp_ref_topic:
        temp_ref = float(payload)
        print(f"Updated temp_ref: {temp_ref}")
    elif topic == control_topic:
        if payload == "start":
            program_running = True
            print("Program started")
        elif payload == "stop":
            program_running = False
            print("Program stopped")

# Initialize MQTT client
client = mqtt.Client()
client.on_message = on_message

def connect_and_subscribe():
    client.connect(broker, port)
    client.subscribe([(temp_ref_topic, 0), (control_topic, 0)])
    client.loop_start()

def publish(topic, payload):
    client.publish(topic, payload)

def get_temp_ref():
    return temp_ref

def program_state():
    return program_running

def disconnect():
    client.loop_stop()
    client.disconnect()
