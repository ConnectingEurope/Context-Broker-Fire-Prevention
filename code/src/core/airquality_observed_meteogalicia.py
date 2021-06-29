import core.silvan_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import connectors.meteogalicia_connector as meteo
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
region_name = config.region
country_info = config.country
NIFI_NOTIFY_URI = config.nifi_notify_uri
list_sub_parameters_elastic = config.aqo_meteo_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_airquality_observed_meteogalicia(service_name, date_observed):
    module_name = 'execute_airquality_observed_meteogalicia'
    
    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_aqo_meteo = config.sensor_info["004"]["id"]
    name_value = config.sensor_info["004"]["name"]
    description_value = config.sensor_info["004"]["description"]
    general_latitude = config.sensor_info["004"]["latitude"]
    general_longitude = config.sensor_info["004"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Request MeteoGalicia
    reponse_meteogalicia = meteo.request_meteogalicia_forecast(general_latitude, general_longitude)
    dict_meteogalicia = format_data.parse_meteogalicia_data(reponse_meteogalicia)
       
    #Generate random values
    if dict_meteogalicia["status"] == True:
        temperature = dict_meteogalicia["temperature"]
        sky_state = dict_meteogalicia["weatherType"]
        wind_speed = dict_meteogalicia["windSpeed"]
        wind_direction = dict_meteogalicia["windDirection"]
        precipitation = dict_meteogalicia["precipitation"]

        # Create classes: AirQualityObserved
        airquaility_observed_region = classes.AirQualityObservedGeneral(id_aqo_meteo, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
        
        # Generate dictionaries for the request (could be a for)
        dict_airquaility_observed_region = airquaility_observed_region.__dict__

        #Format new parameter values to python class
        dict_data_model_airquaility_observed_region = format_data.format_airquality_observed_meteo(dict_airquaility_observed_region, temperature, sky_state, wind_speed, wind_direction, precipitation, string_date_observed)
    
        # Publish payloads
        # Check if data is already created
        list_dicts = [dict_data_model_airquaility_observed_region]
    
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
    else:
        print("UNAVAILABLE DATA FROM METEOGALICIA")
        
# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_airquality_observed_meteogalicia_local(service_name, date_observed):
    module_name = 'execute_airquality_observed_meteogalicia_local'
    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_aqo_meteo = config.sensor_info["004"]["id"]
    name_value = config.sensor_info["004"]["name"]
    description_value = config.sensor_info["004"]["description"]
    general_latitude = config.sensor_info["004"]["latitude"]
    general_longitude = config.sensor_info["004"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Request MeteoGalicia
    reponse_meteogalicia = meteo.request_meteogalicia_forecast(general_latitude, general_longitude)
    dict_meteogalicia = format_data.parse_meteogalicia_data(reponse_meteogalicia)
       
    #Generate random values
    if dict_meteogalicia["status"] == True:
        temperature = dict_meteogalicia["temperature"]
        sky_state = dict_meteogalicia["weatherType"]
        wind_speed = dict_meteogalicia["windSpeed"]
        wind_direction = dict_meteogalicia["windDirection"]
        precipitation = dict_meteogalicia["precipitation"]

        # Create classes: AirQualityObserved
        airquaility_observed_region = classes.AirQualityObservedGeneral(id_aqo_meteo, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
        
        # Generate dictionaries for the request (could be a for)
        dict_airquaility_observed_region = airquaility_observed_region.__dict__

        #Format new parameter values to python class
        dict_data_model_airquaility_observed_region = format_data.format_airquality_observed_meteo(dict_airquaility_observed_region, temperature, sky_state, wind_speed, wind_direction, precipitation, string_date_observed)
    
        # Publish payloads
        # Check if data is already created
        list_dicts = [dict_data_model_airquaility_observed_region]
    
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
    else:
        print("UNAVAILABLE DATA FROM METEOGALICIA")
  
# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_airquality_observed_meteogalicia_random(service_name, date_observed):
    module_name = 'execute_airquality_observed_meteogalicia_random'
    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_aqo_meteo = config.sensor_info["004"]["id"]
    name_value = config.sensor_info["004"]["name"]
    description_value = config.sensor_info["004"]["description"]
    general_latitude = config.sensor_info["004"]["latitude"]
    general_longitude = config.sensor_info["004"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    # Create classes: AirQualityObserved
    airquaility_observed_region = classes.AirQualityObservedGeneral(id_aqo_meteo, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
    
    #Generate random values
    temperature = generate.generate_temperature_random(date_observed)
    sky_state = generate.generate_random_meteogalica_weather(date_observed)
    wind_speed = generate.generate_wind_speed_random(date_observed)
    wind_direction = generate.generate_wind_direction_random_value(date_observed)
    precipitation = generate.generate_precipitation_random(date_observed)
    
    # Generate dictionaries for the request (could be a for)
    dict_airquaility_observed_region = airquaility_observed_region.__dict__

    #Format new parameter values to python class
    dict_data_model_airquaility_observed_region = format_data.format_airquality_observed_meteo(dict_airquaility_observed_region, temperature, sky_state, wind_speed, wind_direction, precipitation, string_date_observed)
    
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_airquaility_observed_region]
    
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
