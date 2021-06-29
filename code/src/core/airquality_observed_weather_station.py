import core.silvan_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
region_name = config.region
country_info = config.country
NIFI_NOTIFY_URI = config.nifi_notify_uri
list_sub_parameters_elastic = config.aqo_weather_station_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False

sub_description_api = 'Notify API of'

# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_airquality_observed_weather_station(service_name, device_id, date_observed, dict_payload):
    module_name = 'execute_airquality_observed_weather_station'
    
    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    list_sub_parameters_elastic = []
    key_payload = ''

    for key in dict_payload:
        if key == 'temperature':
            list_sub_parameters_elastic.append("temperature")
            key_payload = 'temperature'
        elif key == 'relativeHumidity':
            list_sub_parameters_elastic.append("relativeHumidity")
            key_payload = 'relativeHumidity'
        elif key == 'atmosphericPressure':
            list_sub_parameters_elastic.append("atmosphericPressure")
            key_payload = 'atmosphericPressure'	
        elif key == 'illuminance':
            list_sub_parameters_elastic.append("illuminance")
            key_payload = 'illuminance'
        elif key == 'windSpeed':
            list_sub_parameters_elastic.append("windSpeed")
            key_payload = 'windSpeed'
        elif key == 'windDirection':
            list_sub_parameters_elastic.append("windDirection")
            key_payload = 'windDirection'
        elif key == 'precipitation':
            list_sub_parameters_elastic.append("precipitation")
            key_payload = 'precipitation'

    if key_payload != '':
        list_sub_parameters_elastic.append("dateObserved")
        #print(list_sub_parameters_elastic)
        sub_description_elastic = 'Notify Elastic of {0}'.format(key_payload)
        id_aqo_weather_station = config.sensor_info[device_id]["id"] + ':{0}'.format(key_payload)
        name_value= config.sensor_info[device_id]["name"]
        description_value= config.sensor_info[device_id]["description"]
        general_latitude = config.sensor_info[device_id]["latitude"]
        general_longitude = config.sensor_info[device_id]["longitude"]

        string_date_observed = date_observed.isoformat()
        headers = {
            'fiware-service': service_name,
            'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
        
        # Create classes: AirQualityObserved
        airquaility_observed_region = classes.AirQualityObservedGeneral(id_aqo_weather_station, region_name, country_info, name_value, description_value, general_latitude, general_longitude)

        # Generate dictionaries for the request (could be a for)
        dict_airquaility_observed_region = airquaility_observed_region.__dict__

        #Format new parameter values to python class
        json_data_model_airquaility_observed_region = format_data.format_airquality_observed_weather_station(dict_airquaility_observed_region, dict_payload, string_date_observed)
        
        # Publish payloads
        # Check if data is already created
        list_dicts = [json_data_model_airquaility_observed_region]
        
        #Publish payloads
        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ''
        
        try:
            orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        except Exception as ex:
            error_text = "Exception in {0}: {1}".format(module_name, ex)
            print(error_text)

# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_airquality_observed_weather_station_local(service_name, device_id, date_observed, dict_payload):
    module_name = 'execute_airquality_observed_weather_station_local'
    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    list_sub_parameters_elastic = []
    key_payload = ''

    for key in dict_payload:
        if key == 'temperature':
            list_sub_parameters_elastic.append("temperature")
            key_payload = 'temperature'
        elif key == 'relativeHumidity':
            list_sub_parameters_elastic.append("relativeHumidity")
            key_payload = 'relativeHumidity'
        elif key == 'atmosphericPressure':
            list_sub_parameters_elastic.append("atmosphericPressure")
            key_payload = 'atmosphericPressure'	
        elif key == 'illuminance':
            list_sub_parameters_elastic.append("illuminance")
            key_payload = 'illuminance'
        elif key == 'windSpeed':
            list_sub_parameters_elastic.append("windSpeed")
            key_payload = 'windSpeed'
        elif key == 'windDirection':
            list_sub_parameters_elastic.append("windDirection")
            key_payload = 'windDirection'
        elif key == 'precipitation':
            list_sub_parameters_elastic.append("precipitation")
            key_payload = 'precipitation'

    if key_payload != '':
        list_sub_parameters_elastic.append("dateObserved")
        #print(list_sub_parameters_elastic)
        sub_description_elastic = 'Notify Elastic of {0}'.format(key_payload)
        id_aqo_weather_station = config.sensor_info[device_id]["id"] + ':{0}'.format(key_payload)
        name_value= config.sensor_info[device_id]["name"]
        description_value= config.sensor_info[device_id]["description"]
        general_latitude = config.sensor_info[device_id]["latitude"]
        general_longitude = config.sensor_info[device_id]["longitude"]

        string_date_observed = date_observed.isoformat()
        headers = {
            'fiware-service': service_name,
            'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
        
        # Create classes: AirQualityObserved
        airquaility_observed_region = classes.AirQualityObservedGeneral(id_aqo_weather_station, region_name, country_info, name_value, description_value, general_latitude, general_longitude)

        # Generate dictionaries for the request (could be a for)
        dict_airquaility_observed_region = airquaility_observed_region.__dict__

        #Format new parameter values to python class
        json_data_model_airquaility_observed_region = format_data.format_airquality_observed_weather_station(dict_airquaility_observed_region, dict_payload, string_date_observed)
        
        # Publish payloads
        # Check if data is already created
        list_dicts = [json_data_model_airquaility_observed_region]
        
        #Publish payloads
        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ''
        
        try:
            orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        except Exception as ex:
            error_text = "Exception in {0}: {1}".format(module_name, ex)
            print(error_text)