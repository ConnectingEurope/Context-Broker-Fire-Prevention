import requests
import json

# Request to UPDATE (patch) data to a 'put_url' using the headers 'put_headers' and the json data 'dict_data'
def request_patch_data(url, headers, dict_data):
	response = requests.patch(url, json=dict_data, headers=headers)
	return response
		
def request_post_data(url, headers, dict_data):
	response = requests.post(url, json=dict_data, headers=headers)
	return response

def request_delete_data(url, headers, entity_id):
	url = url + entity_id
	response = requests.delete(url, headers=headers)
	return response

# Functions that request the data from a sevice of CB
def check_existing_sub(sub_uri, headers):
	response = requests.get(sub_uri, headers=headers)
	
	return response
	
# Functions that request the data from a sevice of CB
def check_existing_data_type(cb_uri, headers, entity_type):
	url = cb_uri + "?type=" + entity_type
	response = requests.get(url, headers=headers)
	
	return response

# Functions that request the data from a sevice of CB
def check_existing_data_id(cb_uri, headers, entity_id):
	url = cb_uri + entity_id
	response = requests.get(url, headers=headers)
	
	return response

# Function that updates the data of a service of CB
def update_data(cb_uri, headers, dict_data_model):
	dict_data_model_copy = dict_data_model.copy()
	id_entity = dict_data_model.get('id')
	
	del dict_data_model_copy['id']
	del dict_data_model_copy['type']
			
	url = cb_uri + id_entity + '/attrs'
	response = request_patch_data(url, headers, dict_data_model_copy)
	
	return response
	
# Function that updates the data of a service of CB
def update_specific_data(cb_uri, entity_id, headers, dict_data_model):
	url = cb_uri + entity_id + '/attrs'
	response = request_patch_data(url, headers, dict_data_model)
	
	return response

#This method deletes the data information of orion url (entity data)
def delete_data(url, headers, entity_type):
	list_response = []
	existing_data = check_existing_data_type(url, headers, entity_type)
	list_response.append(existing_data)
	
	if existing_data.status_code >= 200 and existing_data.status_code < 300:
		for json in existing_data.json():
			print(json["id"])
			response = request_delete_data(url, headers, json["id"])
			list_response.append(response)

	return list_response	

#This method deletes the subscriptions information of orion url
def delete_data_sub(url, headers):
	list_response = []
	existing_data = check_existing_sub(url, headers)
	list_response.append(existing_data)
	
	if existing_data.status_code >= 200 and existing_data.status_code < 300:
		for json in existing_data.json():
			response = request_delete_data(url, headers, json["id"])
			list_response.append(response)

	return list_response	

#This method creates a generic subscription with no conditions
def create_json_subscription_no_condition(sub_description, data_model_type, list_parameters, notify_uri):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"type": "Subscription",
		"entities": [
			{"type": data_model_type}
		],
		"notification": {
			"attributes": list_parameters,
			"endpoint": {
				"uri": notify_uri,
				"accept": "application/json"
			}
		}
	}
	
	return json_subscription

#This method creates a specific subscription to publish the information to API considering the AQI
def create_json_subscription_aqi_condition_api(sub_description, data_model_type, list_parameters, notify_uri):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"type": "Subscription",
		"entities": [
			{"type": data_model_type}
		],
		"q": "airQualityIndex==-1",
		"notification": {
			"attributes": list_parameters,
			"endpoint": {
				"uri": notify_uri,
				"accept": "application/json"
			}
		}
	}
	
	return json_subscription

#This method creates a specific subscription to publish the information to nifi considering the AQI
def create_json_subscription_aqi_condition_nifi(sub_description, data_model_type, list_parameters, notify_uri):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"type": "Subscription",
		"entities": [
			{"type": data_model_type}
		],
		"q": "airQualityIndex>0",
		"notification": {
			"attributes": list_parameters,
			"endpoint": {
				"uri": notify_uri,
				"accept": "application/json"
			}
		}
	}
	
	return json_subscription

#This method creates an alert subscription with wait time
def create_json_subscription_alert_condition(sub_description, data_model_type, list_parameters, notify_uri, seconds_to_wait_notify):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"type": "Subscription",
		"entities": [
			{"type": data_model_type}
		],
		"notification": {
			"attributes": list_parameters,
			"endpoint": {
				"uri": notify_uri,
				"accept": "application/json"
			}
		},
		"throttling": seconds_to_wait_notify
	}
	
	return json_subscription

# Function that creates the data of a service of CB
def import_data(cb_uri, headers, dict_data_model):
	request_import_data = request_post_data(cb_uri, headers, dict_data_model)
	
	return request_import_data

#This method creates a subscription if there is not an already created subscription with the same description
def create_subscription(sub_uri, headers, subscription_json):
	#check active subscriptions
	check_subscription = check_existing_sub(sub_uri, headers)
	check_subscription_status_code = check_subscription.status_code
	check_subscription_content = check_subscription.json()
	subscription_detected = False
	
	#Check response code
	if check_subscription_status_code == 404:
		request_subs = request_post_data(sub_uri, headers, subscription_json)
	else:
		#check active subscription with the same description as the one we want to create
		if len(check_subscription_content) > 0:
			for i in range(len(check_subscription_content)):
				if subscription_json["description"] == check_subscription_content[i]["description"]:
					subscription_detected = True
					request_subs = check_subscription
					break
			    
		if subscription_detected == False:
			request_subs = request_post_data(sub_uri, headers, subscription_json)
	
	return request_subs

#This method publish to orion and creates the subscriptions if there is no data in orion entities/subscriptions
def orion_publish_update_data(cb_uri, sub_uri, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api):
	for i in range(0, len(list_dicts)):
		try:
			existing_data = check_existing_data_id(cb_uri, headers, list_dicts[i]["id"])
			if existing_data.status_code == 404 and (existing_data.json()["title"]=='No such tenant' or existing_data.json()["title"]=='Entity Not Found'):
				if notify_elastic:
					response_subs = create_subscription(sub_uri, headers, subscription_json_elastic)
					if response_subs.status_code < 200 or response_subs.status_code >=300:
						raise Exception(response_subs.content)             
				if notify_api:
					response_subs = create_subscription(sub_uri, headers, subscription_json_api)
					if response_subs.status_code < 200 or response_subs.status_code >=300:
						raise Exception(response_subs.content)
				response = import_data(cb_uri, headers, list_dicts[i])
				if response.status_code < 200 or response.status_code >= 300:
					raise Exception(response.content)      
			elif existing_data.status_code == 200 and len(existing_data.json()) >= 1:
				response = update_data(cb_uri, headers, list_dicts[i])
				if response.status_code < 200 or response.status_code >= 300:
					raise Exception(response.content)
			else:
				print("error")
				raise Exception(existing_data.content)
		except Exception as ex:
			error_text = "Exception in {0} - {1}".format(list_dicts[i]["id"], ex)
			response = error_text, 500
			print(error_text)
	return response