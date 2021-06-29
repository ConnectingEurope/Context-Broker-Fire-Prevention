import core.silvan_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
region_name = config.region
country_info = config.country
NIFI_NOTIFY_URI = config.nifi_notify_uri
list_sub_parameters_elastic = config.gsr_soil_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of GreenspaceRecord in the Context Broker -> receiving data from sensor -> inside docker container
def execute_greenspace_record_soil(service_name, device_id, date_observed, dict_payload):
    module_name = 'execute_greenspace_record_soil'
    
    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_gsr_soil = config.sensor_info[device_id]["id"]
    name_value= config.sensor_info[device_id]["name"]
    description_value= config.sensor_info[device_id]["description"]
    general_latitude= config.sensor_info[device_id]["latitude"]
    general_longitude= config.sensor_info[device_id]["longitude"]
    
    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    # Create classes: GreenspaceRecord
    greenspace_record_region = classes.GreenspaceRecordGeneral(id_gsr_soil, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
    
    # Sensor values
    soil_temperature = dict_payload["soilTemperature"]
    soil_moisture_vwc = dict_payload["soilMoistureVwc"]
    soil_moisture_ec = dict_payload["soilMoistureEc"]
    
    # Generate dictionaries for the request (could be a for)
    dict_greenspace_record_region = greenspace_record_region.__dict__

    #Format new parameter values to python class
    dict_data_model_greenspace_record_region = format_data.format_greenspace_record(dict_greenspace_record_region, soil_temperature, soil_moisture_vwc, soil_moisture_ec, string_date_observed)
    
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_greenspace_record_region]
    
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

# Functions that create/update the information of GreenspaceRecord in the Context Broker -> receiving data from sensor -> inside docker container
def execute_greenspace_record_soil_local(service_name, device_id, date_observed, dict_payload):
    module_name = 'execute_greenspace_record_soil_local'
    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_gsr_soil = config.sensor_info[device_id]["id"]
    name_value= config.sensor_info[device_id]["name"]
    description_value= config.sensor_info[device_id]["description"]
    general_latitude= config.sensor_info[device_id]["latitude"]
    general_longitude= config.sensor_info[device_id]["longitude"]
    
    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    # Create classes: GreenspaceRecord
    greenspace_record_region = classes.GreenspaceRecordGeneral(id_gsr_soil, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
    
    # Sensor values
    soil_temperature = dict_payload["soilTemperature"]
    soil_moisture_vwc = dict_payload["soilMoistureVwc"]
    soil_moisture_ec = dict_payload["soilMoistureEc"]
    
    # Generate dictionaries for the request (could be a for)
    dict_greenspace_record_region = greenspace_record_region.__dict__

    #Format new parameter values to python class
    dict_data_model_greenspace_record_region = format_data.format_greenspace_record(dict_greenspace_record_region, soil_temperature, soil_moisture_vwc, soil_moisture_ec, string_date_observed)
    
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_greenspace_record_region]
    
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

# Functions that create/update the information of GreenspaceRecord in the Context Broker -> random values
def execute_greenspace_record_soil_random(service_name, date_observed):
    module_name = 'execute_greenspace_record_soil_random'
    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_gsr_soil = config.sensor_info["007"]["id"]
    name_value= config.sensor_info["007"]["name"]
    description_value= config.sensor_info["007"]["description"]
    general_latitude=config.sensor_info["007"]["latitude"]
    general_longitude=config.sensor_info["007"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    # Create classes: GreenspaceRecord
    greenspace_record_region = classes.GreenspaceRecordGeneral(id_gsr_soil, region_name, country_info, name_value, description_value, general_latitude, general_longitude)
    
    # Generate dictionaries for the request (could be a for)
    dict_greenspace_record_region = greenspace_record_region.__dict__

    # Generate random values
    soil_temperature = generate.generate_soil_temperature_random(date_observed)
    soil_moisture_vwc = generate.generate_soil_moisture_vwc_random(date_observed)
    soil_moisture_ec = generate.generate_soil_moisture_ec_random(date_observed)
    
    #Format new parameter values to python class
    dict_data_model_greenspace_record_region = format_data.format_greenspace_record(dict_greenspace_record_region, soil_temperature, soil_moisture_vwc, soil_moisture_ec, string_date_observed)
    
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_greenspace_record_region]
    
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