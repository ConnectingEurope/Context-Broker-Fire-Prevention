import datetime
import time
import pytz
import random

def generate_random_co2(datetime_hour): 
	if(datetime_hour.hour < 7):
		co2= random.randint(0, 300)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 14):
		co2= random.randint(2000, 3000)
	elif (datetime_hour.hour >= 14 and datetime_hour.hour < 22):
		co2= random.randint(1000, 3000)
	elif (datetime_hour.hour >= 22 and datetime_hour.hour <= 23):
		co2= random.randint(0, 300)	
	else:
		co2= random.randint(0, 300)
	
	return co2

def generate_temperature_random(datetime_hour):
	if(datetime_hour.hour < 7):
		temperature= random.randint(5, 12)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		temperature= random.randint(15, 22)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		temperature= random.randint(18, 25)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		temperature= random.randint(12, 15)	
	else:
		temperature= random.randint(12, 15)
	
	return temperature

def generate_humidity_random(datetime_hour):
	if(datetime_hour.hour < 7):
		humidity= random.randint(50, 80)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		humidity= random.randint(10, 30)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		humidity= random.randint(0, 15)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		humidity= random.randint(20, 40)	
	else:
		humidity= random.randint(10, 30)
	
	return humidity

def generate_random_illuminance(datetime_hour): 
	if(datetime_hour.hour < 7):
		illuminance= random.randint(0, 50)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 14):
		illuminance= random.randint(300, 600)
	elif (datetime_hour.hour >= 14 and datetime_hour.hour < 19):
		illuminance= random.randint(200, 500)
	elif (datetime_hour.hour >= 19 and datetime_hour.hour <= 23):
		illuminance= random.randint(0, 50)	
	else:
		illuminance= random.randint(0, 50)
	
	return illuminance

# Functions that generates a random value of air quality index for pm10 -> 0-150+
def generate_random_ap(datetime_hour): 
	ap= random.randint(900, 1100)
	
	return ap
	
def generate_wind_speed_random(datetime_hour):
	if(datetime_hour.hour < 7):
		wind_speed= random.randint(0, 5)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		wind_speed= random.randint(10, 20)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		wind_speed= random.randint(15, 25)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		wind_speed= random.randint(5, 15)	
	else:
		wind_speed= random.randint(0, 20)
	
	return wind_speed

def generate_precipitation_random(datetime_hour):
	if(datetime_hour.hour < 7):
		precipitation= random.randint(0, 5)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		precipitation= random.randint(0, 10)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		precipitation= random.randint(0, 10)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		precipitation= random.randint(0, 5)	
	else:
		precipitation= random.randint(0, 5)
	
	return precipitation
	
def generate_wind_direction_random(datetime_hour):
	wind_direction = random.choice(['north', 'south', 'east', 'west'])
	
	return wind_direction

def generate_wind_direction_random_value(datetime_hour):
	wind_direction = random.uniform(-180.0, 180.0)
	
	return wind_direction

def generate_random_meteogalica_weather(datetime_hour):
	weather_type = random.choice(
	['SUNNY', 'HIGH_CLOUDS', 'PARTLY CLOUDY', 'OVERCAST', 'CLOUDY', 
	'FOG', 'SHOWERS', 'OVERCAST_AND_SHOWERS', 'INTERMITENT_SNOW','DRIZZLE',
	'RAIN', 'SNOW', 'STORMS', 'MIST', 'FOG_BANK', 'MID_CLOUDS', 'WEAK_RAIN',
	'WEAK_SHOWERS', 'STORM_THEN_CLOUDY', 'MELTED_SNOW', 'RAIN_HayL'
	])
	
	return weather_type

def generate_soil_temperature_random(datetime_hour):
	soil_temperature = random.randint(10, 30)
	
	return soil_temperature

def generate_soil_moisture_vwc_random(datetime_hour):
	soil_moisture_vwc = random.randint(0, 100)
	
	return soil_moisture_vwc

def generate_soil_moisture_ec_random(datetime_hour):
	soil_moisture_ec = random.randint(0, 500)
	
	return soil_moisture_ec
	
# Function that converts the datetime of LOWERIS to ISO 8601 - '2021-05-31T10:27:18.463753543Z'
def convert_datetime_loweris(string_datetime):
	datetime_split = string_datetime.split(".")
	datetime_zero = pytz.timezone("Etc/GMT+0")
	datetime_spain = pytz.timezone("Europe/Madrid")

	loweris_datetime = datetime.datetime.strptime(datetime_split[0], '%Y-%m-%dT%H:%M:%S')
	loweris_datetime_tz_0 = datetime_zero.localize(loweris_datetime)
	loweris_datetime_spain = loweris_datetime_tz_0.astimezone(datetime_spain)

	return loweris_datetime_spain
		
# Functions that generates a datetime from now to ISO 8601
def datetime_time_tz():
	datetime_spain = pytz.timezone("Europe/Madrid")
	datetime_now = datetime.datetime.now(datetime_spain)
	datetime_now_no_micro = datetime_now.replace(microsecond=0)
	string_now_tz = datetime_now_no_micro.isoformat()
	
	return string_now_tz, datetime_now_no_micro

def timepoch_to_datetime(time_epoch):
	str_datetime = ''
	datetime_zero = pytz.timezone("Etc/GMT+0")
	datetime_spain = pytz.timezone("Europe/Madrid")

	str_datetime = datetime.datetime.fromtimestamp(time_epoch).strftime('%Y-%m-%dT%H:%M:%S')
	updated_datetime = datetime.datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S')

	updated_datetime_tz_0 = datetime_zero.localize(updated_datetime)
	updated_datetime_spain = updated_datetime_tz_0.astimezone(datetime_spain)
	updated_string_spain = updated_datetime_spain.isoformat()

	return updated_string_spain, updated_datetime_spain

#NOT USED
def validate_payload_meteogalicia(dict_meteogalicia):
	valid_payload = True
	
	if {"features"} <= set(dict_meteogalicia):
		inside_json_0 = dict_meteogalicia["features"]
		if not {"properties"} <= set(inside_json_0):
			valid_payload = False
		else:
			inside_json_1 = dict_meteogalicia["properties"]
			if not {"days"} <= set(inside_json_1):
				valid_payload = False
			else:
				list_inside = dict_meteogalicia["days"]
				if len(list_inside) > 0:
					inside_json_2 = list_inside[0]
					if not {"variables"} <= set(inside_json_2):
						valid_payload = False
				else:
					valid_payload = False
	else:
		valid_payload = False
	
	return valid_payload