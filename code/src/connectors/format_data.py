# Function that parse the data from sensors to the data model class structure (TEMP + HUM + CO2)
def format_airquality_observed(object_airquality_observed, temperature, relative_humidity, co2, string_date_observed):		
	object_airquality_observed["temperature"] = {"type": "Property", "value": temperature}
	object_airquality_observed["relativeHumidity"] = {"type": "Property", "value": relative_humidity}
	object_airquality_observed["co2"] = {"type": "Property", "value": co2}
	object_airquality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_airquality_observed

# Function that parse the data from sensors to the data model class structure (TEMP + HUM + CO2)
def format_airquality_observed_weather_station(object_airquality_observed, dict_data, string_date_observed):		
	for key in dict_data:
		if key == 'temperature':
			object_airquality_observed["temperature"] = {"type": "Property", "value": dict_data["temperature"]}
		elif key == 'relativeHumidity':
			object_airquality_observed["relativeHumidity"] = {"type": "Property", "value": dict_data["relativeHumidity"]}
		elif key == 'atmosphericPressure':
			object_airquality_observed["atmosphericPressure"] = {"type": "Property", "value": dict_data["atmosphericPressure"]}		
		elif key == 'illuminance':
			object_airquality_observed["illuminance"] = {"type": "Property", "value": dict_data["illuminance"]}
		elif key == 'windSpeed':
			object_airquality_observed["windSpeed"] = {"type": "Property", "value": dict_data["windSpeed"]}
		elif key == 'windDirection':
			object_airquality_observed["windDirection"] = {"type": "Property", "value": dict_data["windDirection"]}
		elif key == 'precipitation':
			object_airquality_observed["precipitation"] = {"type": "Property", "value": dict_data["precipitation"]}

	object_airquality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_airquality_observed

# Function that parse the data from sensors to the data model class structure (METEOGALICIA)
def format_airquality_observed_meteo(object_airquality_observed, temperature, sky_state, wind_speed, wind_direction, precipitation, string_date_observed):
	object_airquality_observed["temperature"] = {"type": "Property", "value": temperature}
	object_airquality_observed["weatherType"] = {"type": "Property", "value": sky_state}
	object_airquality_observed["windSpeed"] = {"type": "Property", "value": wind_speed}
	object_airquality_observed["windDirection"] = {"type": "Property", "value": wind_direction}
	object_airquality_observed["precipitation"] = {"type": "Property", "value": precipitation}
	object_airquality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}
	object_airquality_observed["source"] = {"type": "Property", "value": "https://servizos.meteogalicia.gal"}

	return object_airquality_observed
	
# Function that parse the data from sensors to the data model class structure (greenspace record)
def format_greenspace_record(object_airquality_observed, soil_temperature, soil_moisture_vwc, soil_moisture_ec, string_date_observed):		
	object_airquality_observed["soilTemperature"] = {"type": "Property", "value": soil_temperature}
	object_airquality_observed["soilMoistureVwc"] = {"type": "Property", "value": soil_moisture_vwc}
	object_airquality_observed["soilMoistureEc"] = {"type": "Property", "value": soil_moisture_ec}
	object_airquality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_airquality_observed
	
def format_fire_forest_status_fwi(object_fire_forest_status, string_date_observed, fwi_class):
	object_fire_forest_status["fireWeatherIndex"] = {"type": "Property", "value": fwi_class.FWI}
	object_fire_forest_status["dailySeverityRating"] = {"type": "Property", "value": fwi_class.DSR}
	object_fire_forest_status["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}
	object_fire_forest_status["values"] = {"type": "Property", "value": fwi_class.__dict__}

	return object_fire_forest_status

def format_fire_forest_status_smoke(object_fire_forest_status, smoke_detected, smoke_confidence, string_date_observed):
	object_fire_forest_status["smokeDetected"] = {"type": "Property", "value": smoke_detected}
	object_fire_forest_status["smokeDetectedConfidence"] = {"type": "Property", "value": smoke_confidence}
	object_fire_forest_status["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_fire_forest_status

#this is for the dry detector
def format_fire_forest_status_dry(object_fire_forest_status, dry_detected, average_green, average_dry, string_date_observed):
	object_fire_forest_status["dryDetected"] = {"type": "Property", "value": dry_detected}
	object_fire_forest_status["greenLeaves"] = {"type": "Property", "value": average_green}
	object_fire_forest_status["dryLeaves"] = {"type": "Property", "value": average_dry}
	object_fire_forest_status["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_fire_forest_status
	
def parse_meteogalicia_data(reponse_json_meteogalicia):
	dict_meteogalicia = {}
	try:
		useful_data = reponse_json_meteogalicia["features"][0]["properties"]["days"][0]["variables"]
		for dict_data in useful_data:
			if dict_data["name"] == 'sky_state':
				dict_meteogalicia["weatherType"] = dict_data["values"][0]["value"]
			elif dict_data["name"] == 'temperature':
				dict_meteogalicia["temperature"] = dict_data["values"][0]["value"]
			elif dict_data["name"] == 'precipitation_amount':
				dict_meteogalicia["precipitation"] = dict_data["values"][0]["value"]
			elif dict_data["name"] == 'wind':
				dict_meteogalicia["windSpeed"] = dict_data["values"][0]["moduleValue"]
				dict_meteogalicia["windDirection"] = dict_data["values"][0]["directionValue"]
		
		dict_meteogalicia["status"] = True
	except Exception as ex:
		error_text = "Exception in parse_meteogalicia_data: {0}".format(ex)
		#print(reponse_json_meteogalicia)
		print(error_text)
		dict_meteogalicia["temperature"] = -1
		dict_meteogalicia["weatherType"] = -1
		dict_meteogalicia["windSpeed"] = -1
		dict_meteogalicia["windDirection"] = -1
		dict_meteogalicia["precipitation"] = -1
		dict_meteogalicia["status"] = False

	print(dict_meteogalicia)
	
	return dict_meteogalicia