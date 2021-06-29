import utils.generate_information as generate
import core.airquality_observed_mqtt_client as aqo
import core.greenspace_record_soil as gsr
from config import config as cnf
config = cnf.Config()

DEVICE_TYPES = config.sensor_type
AQO_TEMP_SERVICE_NAME = config.air_quality_observed_mqtt_client
GSR_SERVICE_NAME = config.green_space_record_soil

def check_valid_payload(dict_payload):
	valid_payload = True
	
	if {"end_device_ids", "uplink_message"} <= set(dict_payload):
		inside_json_id = dict_payload["end_device_ids"]
		if not {"device_id"} <= set(inside_json_id):
			valid_payload = False
			
		inside_json_payload = dict_payload["uplink_message"]
		if not {"frm_payload", "received_at"} <= set(inside_json_payload):
			valid_payload = False
	else:
		valid_payload = False
	
	return valid_payload
	
def decoder_AM107(bytes_data):
	i = 0
	dict_data = {}
	
	while i < len(bytes_data):
		identifier_channel = i
		identifier_type = i+1
		channel_id = bytes_data[identifier_channel]
		#print(channel_id)
		channel_type = bytes_data[identifier_type]
		#print(channel_type)
		
		if channel_id == 0x01 and channel_type == 0x75:
			#print("Battery")
			dict_data["batteryLevel"] = float(bytes_data[i+2])
			#print("{0} %".format(dict_data["batteryLevel"]))
			i += 3
		elif channel_id == 0x03 and channel_type == 0x67:
			#print("Temperature")
			dict_data["temperature"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])*0.1
			#print("{0} ºC".format(dict_data["temperature"]))
			i += 4
		elif channel_id == 0x04 and channel_type == 0x68:
			#print("Relative humidity")
			dict_data["relativeHumidity"] = float(bytes_data[i+2])*0.5
			#print("{0} %".format(dict_data["relativeHumidity"]))
			i += 3
		elif channel_id == 0x05 and channel_type == 0x6a:
			#print("Motion activity")
			dict_data["motionActivity"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			#print("Activity level: {0}".format(dict_data["motionActivity"]))
			i += 4
		elif channel_id == 0x06 and channel_type == 0x65:
			#print("Illuminance")
			dict_data["illuminance"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			dict_data["visibleInfrared"] = float(bytes_data[i+5] << 8 | bytes_data[i+4])
			dict_data["infrared"] = float(bytes_data[i+7] << 8 | bytes_data[i+6])
			#print("Illumination: {0} lux".format(dict_data["illuminance"]))
			#print("Visible + Infrared: {0}".format(dict_data["visibleInfrared"]))
			#print("Infrared: {0}".format(dict_data["infrared"]))
			i += 8
		elif channel_id == 0x07 and channel_type == 0x7d:
			#print("CO2")
			dict_data["co2"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			#print("{0} ppm".format(dict_data["co2"]))
			i += 4
		elif channel_id == 0x08 and channel_type == 0x7d:
			#print("TVOC")
			dict_data["tvoc"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			#print("{0} ppb".format(dict_data["tvoc"]))
			i += 4
		elif channel_id == 0x09 and channel_type == 0x73:
			#print("Barometric Pressure")
			dict_data["atmosphericPressure"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])*0.1
			#print("{0} hPa".format(dict_data["atmosphericPressure"]))
			i += 4
		else:
			print("else")
			break
		
	return dict_data

def decoder_EM500_co2(bytes_data):
	i = 0
	dict_data = {}
	
	while i < len(bytes_data):
		identifier_channel = i
		identifier_type = i+1
		channel_id = bytes_data[identifier_channel]
		#print(channel_id)
		channel_type = bytes_data[identifier_type]
		#print(channel_type)
		
		if channel_id == 0x01 and channel_type == 0x75:
			#print("Battery")
			dict_data["batteryLevel"] = float(bytes_data[i+2])
			#print("{0} %".format(dict_data["batteryLevel"]))
			i += 3
		elif channel_id == 0x03 and channel_type == 0x67:
			#print("Temperature")
			dict_data["temperature"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])*0.1
			#print("{0} ºC".format(dict_data["temperature"]))
			i += 4
		elif channel_id == 0x04 and channel_type == 0x68:
			#print("Relative humidity")
			dict_data["relativeHumidity"] = float(bytes_data[i+2])*0.5
			#print("{0} %".format(dict_data["relativeHumidity"]))
			i += 3
		elif channel_id == 0x05 and channel_type == 0x7d:
			#print("CO2")
			dict_data["co2"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			#print("{0} ppm".format(dict_data["co2"]))
			i += 4
		elif channel_id == 0x06 and channel_type == 0x73:
			#print("Barometric Pressure")
			dict_data["atmosphericPressure"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])*0.1
			#print("{0} hPa".format(dict_data["atmosphericPressure"]))
			i += 4
		else:
			print("else")
			break
		
	return dict_data
	
def decoder_EM500_SMTC(bytes_data):
	i = 0
	dict_data = {}
	
	while i < len(bytes_data):
		identifier_channel = i
		identifier_type = i+1
		channel_id = bytes_data[identifier_channel]
		#print(channel_id)
		channel_type = bytes_data[identifier_type]
		#print(channel_type)
		
		if channel_id == 0x01 and channel_type == 0x75:
			#print("Battery")
			dict_data["batteryLevel"] = float(bytes_data[i+2])
			#print("{0} %".format(dict_data["batteryLevel"]))
			i += 3
		elif channel_id == 0x03 and channel_type == 0x67:
			#print("Soil temperature")
			dict_data["soilTemperature"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])*0.1
			#print("{0} ºC".format(dict_data["soilTemperature"]))
			i += 4
		elif channel_id == 0x04 and channel_type == 0x68:
			#print("Soil Moisture Vwc")
			dict_data["soilMoistureVwc"] = float(bytes_data[i+2])*0.5
			#print("{0} %".format(dict_data["soilMoistureVwc"]))
			i += 3
		elif channel_id == 0x05 and channel_type == 0x7f:
			#print("Soil Moisture Ec")
			dict_data["soilMoistureEc"] = float(bytes_data[i+3] << 8 | bytes_data[i+2])
			#print("{0} us/m".format(dict_data["soilMoistureEc"]))
			i += 4
		else:
			print("else")
			break
		
	return dict_data

def process_received_payload(device_id, time_data_received, payload_data_received):
	device_type = DEVICE_TYPES[device_id]
	dict_data = {}
	
	if device_type == "AM107":
		print(device_type)
		#dict_result = decoder_AM107(payload_data_received)
		#print(dict_result)
		#formatted_date_observed = generate.convert_datetime_loweris(time_data_received)
		#indoor.execute_indoor_sensor(INDOOR_SERVICE_NAME, device_id, formatted_date_observed, dict_result)
	elif device_type == "EM500-CO2":
		print(device_type)
		formatted_date_observed = generate.convert_datetime_loweris(time_data_received)
		print(formatted_date_observed)
		dict_result = decoder_EM500_co2(payload_data_received)
		print(dict_result)
		aqo.execute_airquality_observed_mqtt(AQO_TEMP_SERVICE_NAME, device_id, formatted_date_observed, dict_result)
	elif device_type == "EM500-SMTC":
		print(device_type)
		formatted_date_observed = generate.convert_datetime_loweris(time_data_received)
		print(formatted_date_observed)
		dict_result = decoder_EM500_SMTC(payload_data_received) 
		print(dict_result)
		gsr.execute_greenspace_record_soil(GSR_SERVICE_NAME, device_id, formatted_date_observed, dict_result)
	else:
		error_message = "Unknown device ID: {0}".format(device_id)
		raise Exception(error_message)