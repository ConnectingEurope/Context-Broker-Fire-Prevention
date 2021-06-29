import utils.generate_information as generate
import rule_engine.rules.rules as rules
import rule_engine.alerts.alerts as alerts
import connectors.mysql_connector as mysql
import connectors.orion_connector_ld as orion
from config import config as cnf

config = cnf.Config()

RULE_ATTRIBUTE_COLUMNS = config.mysql_alert_columns
RULE_ENGINE_TABLE = config.mysql_alert_table
CB_URI_LD = config.context_broker_uri_ld
SUB_URI_LD = config.subscription_uri_ld
NIFI_NOTIFY_URI = config.nifi_notify_uri

#This method loads the rules from mysql
def load_rules():
    list_rules = []
    
    mysql_connector = mysql.connect()
    query = "SELECT {0} FROM {1}".format(RULE_ATTRIBUTE_COLUMNS, RULE_ENGINE_TABLE)
    mysql_result = mysql.select_query(mysql_connector, query)
    print(mysql_result)
    
    if len(mysql_result) > 0: 
        for (rule_id, service_name, entity_type, attribute_name, operator, max_threshold, value_category, value_subcategory, value_severity, subscription_id, recurrence_seconds) in mysql_result:
            list_rules.append(rules.Rule(rule_id, service_name, entity_type, attribute_name, operator, max_threshold, value_category, value_subcategory, value_severity, subscription_id, recurrence_seconds))
            
    return list_rules

#This method evaluates a rule (information stored in dict data_rule) considering the list of the rules.
def evaluate_rules(service_name_from, list_rules, data_rule):    
	if len(list_rules) > 0:
		for rule in list_rules:
			#match the attribute to evaluate with the corresponding rule
			if rule.attribute == data_rule['attribute']:     
				result = rule.evaluate(data_rule['value'])
			#if result is true, it will trigger the alert
				if result:         
					create_publish_alert(service_name_from, rule, data_rule)

#this method publish or update the information of the alert to orion/elastic  
def create_publish_alert(service_name_from, rule, data_rule):
    method_name = 'create_publish_alert'
    date_created = generate.datetime_time_tz()
    service_name = 'alerts'
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #CB connection parameters  
    list_sub_parameters_elastic = ["name", "description", "alertSource", "category", "subCategory", "severity", "dateIssued"]
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'
    
    #Define alert class values
    field_attribute = data_rule['attribute'] # the involved attribute
    alert_source = data_rule['dataProvider']['value'] # url of the device
    date_issued = data_rule['dateObserved']['value'] # date from alert that was detected
    current_field_value = data_rule['value']
    category = rule.category
    sub_category = rule.subCategory
    severity = rule.severity
    operator = rule.operator
    threshold = rule.threshold
    
    custom_alert_class = alerts.Alert(service_name_from, field_attribute, alert_source, date_issued, category, sub_category, severity, operator, threshold, current_field_value)
    
    #Generate dictionary for the request (could be a for)
    dict_custom_alert_class = custom_alert_class.__dict__
    
    list_dicts = [dict_custom_alert_class]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        print(response.status_code)
        print(response.content)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

#this method publish or update the information of the alert to orion/elastic  
def create_publish_alert_smoke(service_name_from, rule, data_rule, path_image_name):
    method_name = 'create_publish_alert_smoke'
    date_created = generate.datetime_time_tz()

    service_name = 'alerts'
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #CB connection parameters  
    list_sub_parameters_elastic = ["name", "description", "alertSource", "category", "subCategory", "severity", "dateIssued"]
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'
    #Define alert class values
    split_image_path = path_image_name.split("/")
    image_name = split_image_path[len(split_image_path)-1]
    field_attribute = data_rule['attribute'] # the involved attribute
    alert_source = "{0} - {1}".format(data_rule['dataProvider']['value'], image_name.replace(" ","_"))  # url of the device
    date_issued = data_rule['dateObserved']['value'] # date from alert that was detected
    current_field_value = data_rule['value']
    category = rule.category
    sub_category = rule.subCategory
    severity = rule.severity
    operator = rule.operator
    threshold = rule.threshold
    custom_alert_class = alerts.Alert(service_name_from, field_attribute, alert_source, date_issued, category, sub_category, severity, operator, threshold, current_field_value)
    #Generate dictionary for the request (could be a for)
    dict_custom_alert_class = custom_alert_class.__dict__
    
    list_dicts = [dict_custom_alert_class]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        print(response.status_code)
        print(response.content)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

#this method publish or update the information of the alert to orion/elastic  
def create_publish_alert_dry(service_name_from, rule, data_rule):
    method_name = 'create_publish_alert_dry'
    date_created = generate.datetime_time_tz()
    service_name = 'alerts'
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #CB connection parameters  
    list_sub_parameters_elastic = ["name", "description", "alertSource", "category", "subCategory", "severity", "dateIssued"]
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'
    
    #Define alert class values
    field_attribute = data_rule['attribute'] # the involved attribute
    alert_source = "{0} - {1}".format(data_rule['dataProvider']['value'], data_rule["fileName"].replace(" ","_"))  # url of the device
    date_issued = data_rule['dateObserved']['value'] # date from alert that was detected
    current_field_value = data_rule['value']
    category = rule.category
    sub_category = rule.subCategory
    severity = rule.severity
    operator = rule.operator
    threshold = rule.threshold
    
    custom_alert_class = alerts.Alert(service_name_from, field_attribute, alert_source, date_issued, category, sub_category, severity, operator, threshold, current_field_value)
    
    #Generate dictionary for the request (could be a for)
    dict_custom_alert_class = custom_alert_class.__dict__
    
    list_dicts = [dict_custom_alert_class]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        print(response.status_code)
        print(response.content)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)