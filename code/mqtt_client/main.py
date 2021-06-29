import paho.mqtt.client as mqtt
import json
import datetime
import base64

import data_formatter.mqtt_formatter as format_data
import utils.generate_information as generate
from config import config as cnf
config = cnf.Config()

MQTT_USER = config.mqtt_user
MQTT_PASSWORD = config.mqtt_password
MQTT_SERVER = config.mqtt_server
MQTT_PORT = config.mqtt_port

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
	method_name = 'on_connect'
	try:
		if rc != 0:
			error_message = define_error_message(rc)
			raise Exception("Error connecting to the mqtt server. Error code: {0}. Error message: {1}".format(rc, error_message))
		else:
			print("{0} - Successful connection.".format(datetime.datetime.now()))  # Print result of connection attempt
			sub_topics = "#"
			client.subscribe(sub_topics)  # Subscribe to the topic “digitest/test1”, receive any messages published on it
			print("Subscribed to topics: {0}".format(sub_topics))
	except Exception as ex:
		error_text = "Exception in {0}: {1}".format(method_name, ex)
		print(error_text)
		raise Exception(error_text)

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
	method_name = 'on_message'
	try:
		string_now_tz, datetime_now_no_micro = generate.datetime_time_tz()

		print("Message received: {0}".format(string_now_tz))  # Print a received msg
		print("Topic: " + msg.topic)
		json_received = json.loads(msg.payload)
		#print("Payload: " + str(json_received))
		valid_payload = format_data.check_valid_payload(json_received)
		print("Valid payload: {0}".format(valid_payload))
		
		if valid_payload:
			time_data_received = json_received["uplink_message"]["received_at"]
			device_id = json_received["end_device_ids"]["device_id"]
			payload_data_received = json_received["uplink_message"]["frm_payload"]
			print("Data received: " + payload_data_received)
			
			data_received_base64 = base64.b64decode(payload_data_received)
			#print("Decoding base64: {0}".format(data_received_base64))
			
			format_data.process_received_payload(device_id, time_data_received, data_received_base64)
	except Exception as ex:
		error_text = "Exception in {0}. Exception: {1}".format(method_name, ex)
		print(error_text)
		#raise Exception(error_text)
		
def define_error_message(error_code):
	switcher={
		1: "Connection refused – incorrect protocol version",
		2: "Connection refused – invalid client identifier",
		3: "Connection refused – server unavailable",
		4: "Connection refused – bad username or password",
		5: "Connection refused – not authorised"	
	}
	
	return switcher.get(error_code, "Unknown")
	
if __name__ == "__main__":
	client = mqtt.Client("mqtt_subscriber")  # Create instance of client with client ID “digi_mqtt_test”
	client.on_connect = on_connect  # Define callback function for successful connection
	client.on_message = on_message  # Define callback function for receipt of a message

	client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
	print("Connecting")
	client.connect(MQTT_SERVER, MQTT_PORT)
	client.loop_forever()  # Start networking daemon
