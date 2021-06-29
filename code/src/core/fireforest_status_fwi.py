import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import algorithms.fwi.fire_weather_index as fwi
import core.silvan_classes_ld as classes
import config.config as cfg
config = cfg.Config()

SERVICE_AQO_TEMP = config.air_quality_observed_mqtt_client
SERVICE_AQO_WIND = config.air_quality_observed_weather_station
NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
notify_elastic = True
notify_api = False
list_sub_parameters_elastic = config.ffs_fwi_subs
list_sub_parameters_api = []
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

def execute_fire_forest_status_fwi(service_name, date_observed):
    module_name = 'execute_fire_forest_status_fwi'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    ID_AQO_TEMP= config.sensor_info["006"]["id"]
    ID_AQO_WIND= config.sensor_info["1"]["id"]
    ID_FFS_FWI = config.sensor_info["002"]["id"]
    ffs_polygon_coordinates = config.sensor_info["002"]["location"]
    name_value = config.sensor_info["002"]["name"]
    description_value = config.sensor_info["002"]["description"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    try:
        id_aqo_temp="urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(region_name, ID_AQO_TEMP)
        id_aqo_wind_speed="urn:ngsi-ld:AirQualityObserved:{0}:{1}:windSpeed".format(region_name, ID_AQO_WIND)
        id_aqo_wind_precipitation="urn:ngsi-ld:AirQualityObserved:{0}:{1}:precipitation".format(region_name, ID_AQO_WIND)
        list_id_wind = {"windSpeed": id_aqo_wind_speed, 
                        "precipitation": id_aqo_wind_precipitation}
        id_ffs_fwi="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region_name, ID_FFS_FWI)

        #GET VALUES from temphum and wind
        headers['fiware-service'] = SERVICE_AQO_TEMP
        existing_data_th = orion.check_existing_data_id(CB_URI_LD, headers, id_aqo_temp)

        if existing_data_th.status_code == 404 and (existing_data_th.json()["title"]=='No such tenant' or existing_data_th.json()["title"]=='Entity Not Found'):
            raise Exception("Error getting data from '{0}'. Exception: {1}".format(id_aqo_temp, existing_data_th.content))
        
        response_wind = {}
        for key in list_id_wind:
            headers['fiware-service'] = SERVICE_AQO_WIND
            existing_data_w = orion.check_existing_data_id(CB_URI_LD, headers, list_id_wind[key])
            response_wind[key] = existing_data_w

            if existing_data_w.status_code == 404 and (existing_data_w.json()["title"]=='No such tenant' or existing_data_w.json()["title"]=='Entity Not Found'):
                raise Exception("Error getting data from '{0}'. Exception: {1}".format(list_id_wind[key], existing_data_w.content))

        headers['fiware-service'] = service_name 
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, id_ffs_fwi)
        
        if existing_data.status_code == 404 and (existing_data.json()["title"]=='No such tenant' or existing_data.json()["title"]=='Entity Not Found'):
            FFMC_prev = 87.7
            DMC_prev = 8.5
            DC_prev = 19.1
            current_month = date_observed.month
        else:
            FFMC_prev = existing_data.json()["values"]["value"]["FFMCPrev"]
            DMC_prev = existing_data.json()["values"]["value"]["DMCPrev"]
            DC_prev = existing_data.json()["values"]["value"]["DCPrev"]
            current_month = date_observed.month

        precipitation = response_wind["precipitation"].json()["precipitation"]["value"]
        wind_speed = response_wind["windSpeed"].json()["windSpeed"]["value"]
        temperature = existing_data_th.json()["temperature"]["value"]
        relative_humidity = existing_data_th.json()["relativeHumidity"]["value"]

        #CALCULATE
        fire_class = fwi.FireWeatherIndex(temperature, relative_humidity, wind_speed, precipitation, FFMC_prev, DMC_prev, DC_prev, current_month)
        fire_class.calculate_fire_weather_index()
        fire_class.calculate_daily_severity_rating()
        
        #Create generic class ffs polygon
        class_fire_forest_status_fwi = classes.FireForestStatusPolygonGeneral(ID_FFS_FWI, region_name, country_info, name_value, description_value, ffs_polygon_coordinates)
        
        # Generate dictionaries for the request (could be a for)
        dict_fire_forest_staus = class_fire_forest_status_fwi.__dict__

        dict_data_model_fire_forest_status = format_data.format_fire_forest_status_fwi(dict_fire_forest_staus, string_date_observed, fire_class)
    
        list_dicts = [dict_data_model_fire_forest_status]

        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ""

        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}. Exception: {1}".format(module_name, ex)
        print(error_text)

def execute_fire_forest_status_fwi_local(service_name, date_observed):
    module_name = 'execute_fire_forest_status_fwi_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    ID_AQO_TEMP= config.sensor_info["006"]["id"]
    ID_AQO_WIND= config.sensor_info["1"]["id"]
    ID_FFS_FWI = config.sensor_info["002"]["id"]
    ffs_polygon_coordinates = config.sensor_info["002"]["location"]
    name_value = config.sensor_info["002"]["name"]
    description_value = config.sensor_info["002"]["description"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    try:
        id_aqo_temp="urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(region_name, ID_AQO_TEMP)
        id_aqo_wind_speed="urn:ngsi-ld:AirQualityObserved:{0}:{1}:windSpeed".format(region_name, ID_AQO_WIND)
        id_aqo_wind_precipitation="urn:ngsi-ld:AirQualityObserved:{0}:{1}:precipitation".format(region_name, ID_AQO_WIND)
        list_id_wind = {"windSpeed": id_aqo_wind_speed, 
                        "precipitation": id_aqo_wind_precipitation}
        id_ffs_fwi="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region_name, ID_FFS_FWI)

        #GET VALUES from temphum and wind
        headers['fiware-service'] = SERVICE_AQO_TEMP
        existing_data_th = orion.check_existing_data_id(CB_URI_LD, headers, id_aqo_temp)

        if existing_data_th.status_code == 404 and (existing_data_th.json()["title"]=='No such tenant' or existing_data_th.json()["title"]=='Entity Not Found'):
            raise Exception("Error getting data from '{0}'. Exception: {1}".format(id_aqo_temp, existing_data_th.content))
        
        response_wind = {}
        for key in list_id_wind:
            headers['fiware-service'] = SERVICE_AQO_WIND
            existing_data_w = orion.check_existing_data_id(CB_URI_LD, headers, list_id_wind[key])
            response_wind[key] = existing_data_w

            if existing_data_w.status_code == 404 and (existing_data_w.json()["title"]=='No such tenant' or existing_data_w.json()["title"]=='Entity Not Found'):
                raise Exception("Error getting data from '{0}'. Exception: {1}".format(list_id_wind[key], existing_data_w.content))

        headers['fiware-service'] = service_name 
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, id_ffs_fwi)
        
        if existing_data.status_code == 404 and (existing_data.json()["title"]=='No such tenant' or existing_data.json()["title"]=='Entity Not Found'):
            FFMC_prev = 87.7
            DMC_prev = 8.5
            DC_prev = 19.1
            current_month = date_observed.month
        else:
            FFMC_prev = existing_data.json()["values"]["value"]["FFMCPrev"]
            DMC_prev = existing_data.json()["values"]["value"]["DMCPrev"]
            DC_prev = existing_data.json()["values"]["value"]["DCPrev"]
            current_month = date_observed.month

        precipitation = response_wind["precipitation"].json()["precipitation"]["value"]
        wind_speed = response_wind["windSpeed"].json()["windSpeed"]["value"]
        temperature = existing_data_th.json()["temperature"]["value"]
        relative_humidity = existing_data_th.json()["relativeHumidity"]["value"]

        #CALCULATE
        fire_class = fwi.FireWeatherIndex(temperature, relative_humidity, wind_speed, precipitation, FFMC_prev, DMC_prev, DC_prev, current_month)
        fire_class.calculate_fire_weather_index()
        fire_class.calculate_daily_severity_rating()
        
        #Create generic class ffs polygon
        class_fire_forest_status_fwi = classes.FireForestStatusPolygonGeneral(ID_FFS_FWI, region_name, country_info, name_value, description_value, ffs_polygon_coordinates)
        
        # Generate dictionaries for the request (could be a for)
        dict_fire_forest_staus = class_fire_forest_status_fwi.__dict__

        dict_data_model_fire_forest_status = format_data.format_fire_forest_status_fwi(dict_fire_forest_staus, string_date_observed, fire_class)
    
        list_dicts = [dict_data_model_fire_forest_status]

        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ""

        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}. Exception: {1}".format(module_name, ex)
        print(error_text)