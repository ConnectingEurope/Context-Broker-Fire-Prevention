import core.silvan_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
region_name = config.region
country_info = config.country
NIFI_NOTIFY_URI = config.nifi_notify_uri
list_sub_parameters_elastic = config.ffs_dry_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_fire_forest_status_dry(service_name, date_observed, dry_detected, average_green, average_dry, latitude, longitude):
    module_name = 'execute_fire_forest_status_dry'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    id_ffs_dry = config.sensor_info["005"]["id"]
    name_value = config.sensor_info["005"]["name"]
    value_description = config.sensor_info["005"]["description"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate fire forest class
    custom_fire_forest_class = classes.FireForestStatusPointerGeneral(id_ffs_dry, region_name, country_info, name_value, value_description, latitude, longitude)
    
    # Generate dictionaries for the request (could be a for)
    dict_fire_forest_staus = custom_fire_forest_class.__dict__

    #Format new parameter values to python class
    dict_data_model_fire_forest_status = format_data.format_fire_forest_status_dry(dict_fire_forest_staus, dry_detected, average_green, average_dry, string_date_observed)
           
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_fire_forest_status]
    
    #Publish payloads
    #Create the necessary subscriptions
    #notify_test_api=API_NOTIFY_URI+"notifications/fire-forest"
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(module_name, ex)
        response = error_text
        print(error_text)
    
    return response

# Functions that create/update the information of AirQualityObserved in the Context Broker
def execute_fire_forest_status_dry_local(service_name, date_observed, dry_detected, average_green, average_dry, latitude, longitude):
    module_name = 'execute_fire_forest_status_dry_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    id_ffs_dry = config.sensor_info["005"]["id"]
    name_value = config.sensor_info["005"]["name"]
    value_description = config.sensor_info["005"]["description"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate fire forest class
    custom_fire_forest_class = classes.FireForestStatusPointerGeneral(id_ffs_dry, region_name, country_info, name_value, value_description, latitude, longitude)
    
    # Generate dictionaries for the request (could be a for)
    dict_fire_forest_staus = custom_fire_forest_class.__dict__

    #Format new parameter values to python class
    dict_data_model_fire_forest_status = format_data.format_fire_forest_status_dry(dict_fire_forest_staus, dry_detected, average_green, average_dry, string_date_observed)
           
    # Publish payloads
    # Check if data is already created
    list_dicts = [dict_data_model_fire_forest_status]
    
    #Publish payloads
    #Create the necessary subscriptions
    #notify_test_api=API_NOTIFY_URI+"notifications/fire-forest"
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(module_name, ex)
        response = error_text
        print(error_text)
    
    return response
