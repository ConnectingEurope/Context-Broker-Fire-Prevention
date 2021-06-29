import requests 
import config.config as cnf
import json

config = cnf.Config()

CB_URI = config.context_broker_uri #'http://localhost:1026/v2/entities/'
SUBS_URI = config.subscription_uri #'http://localhost:1026/v2/subscriptions/'

# Request to PUT data to a 'put_url' using the headers 'put_headers' and the json data 'dict_data'
def request_put_data(put_url, dict_data, put_headers):
	response = requests.put(put_url, data=json.dumps(dict_data), headers=put_headers)
	return response

def request_post_data(post_url, dict_data, post_headers):
    response = requests.post(post_url, data=json.dumps(dict_data), headers=post_headers)
    return response

def request_delete_data(delete_url, id_entity, service_name):
	delete_url = delete_url + id_entity
	response = requests.delete(delete_url, headers={'fiware-service': service_name})
	return response

def request_delete_data_ld(delete_url, id_entity, service_name):
    delete_url = delete_url + id_entity
    #print(delete_url)
    response = requests.delete(delete_url, headers={'fiware-service': service_name})
    return response

# Functions that request the data from a sevice of CB
def check_existing_data(cb_uri, service_name):
	existent_data = requests.get(cb_uri, headers={'fiware-service': service_name})
	
	return existent_data

# Functions that request the data from a sevice of CB
def check_existing_data_id(cb_uri, service_name, data_id):
	checking_uri = cb_uri + data_id
	existent_data = requests.get(checking_uri, headers={'fiware-service': service_name})

	return existent_data

# Function that updates the data of a service of CB
def update_data(service_name, headers, dict_data_model):
	dict_data_model_copy = dict_data_model.copy()
	id_parameter = dict_data_model.get('id')
	del dict_data_model_copy['id']
	del dict_data_model_copy['type']
			
	update_url = CB_URI + id_parameter + '/attrs' + '?options=keyValues'
	response = request_put_data(update_url, dict_data_model_copy, headers)
	
	return response

# Function that updates the data of a service of CB only some specific values
def update_specific_data(id_data, service_name, headers, dict_data):
	post_url = CB_URI + id_data + '/attrs' + '?options=keyValues'
	response = request_post_data(post_url, dict_data, headers)
	
	return response
	
def delete_data(url, service_name):
	list_response = []
	existing_data = check_existing_data(url, service_name)
	list_response.append(existing_data)
	#print("{0}: {1} : {2} : {3}".format(service_name, existing_data.status_code, len(existing_data.json()), existing_data.json()))
		
	for json in existing_data.json():
		response = request_delete_data(url, json["id"], service_name)
		list_response.append(response)
		#print(response.status_code)
		#print(response.content)

	return list_response	

def create_json_subscription_no_condition(id_pattern, sub_description, data_model_type, list_parameters, notify_uri):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"subject": {
			"entities": [{
				"type": data_model_type,
				"idPattern": "{0}.*".format(id_pattern)
			}],
			"condition": {
				"attrs": []
			}
		},
		"notification": {
			"http": {
				"url": notify_uri
			},
			"attrs": list_parameters
		}
	}
	
	return json_subscription

def create_json_subscription_aqi_condition(id_pattern, sub_description, data_model_type, list_parameters, notify_uri):
	json_subscription = {
		"description": "{0} {1}".format(sub_description, data_model_type),
		"subject": {
			"entities": [{
				"type": data_model_type,
				"idPattern": "{0}.*".format(id_pattern)
			}],
			"condition": {
				"expression": {
					"q": "airQualityLevel!=''"}
			}
		},
		"notification": {
			"http": {
				"url": notify_uri
			},
			"attrs": list_parameters
		}
	}
	
	return json_subscription
	
# Function that creates the data of a service of CB
def import_data(headers, dict_data_model):
	uri_import_data = CB_URI + '?options=keyValues'
	request_import_data = request_post_data(uri_import_data, dict_data_model, headers)
	#print('Creation of entity, response_code: {0} // content: {1}'.format(request_import_data.status_code, request_import_data.content))
	
	return request_import_data

def create_subscription(service_name, headers, subscription_json):
	#check active subscriptions
	check_subscription = check_existing_data(SUBS_URI, service_name)
	check_subscription_status_code = check_subscription.status_code
	check_subscription_content = check_subscription.json()
	
	subscription_detected = False

	if len(check_subscription_content) > 0:
		for i in range(len(check_subscription_content)):
			if subscription_json["description"] == check_subscription_content[i]["description"]:
				subscription_detected = True
				request_subs = check_subscription
				break
			    
	if subscription_detected == False:
		#print("create sub")
		request_subs = request_post_data(SUBS_URI, subscription_json, headers)
	
	return request_subs

def orion_publish_update_data(service_name, id_pattern, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api):
	headers = {'Content-Type': 'application/json', 'fiware-service': service_name}
	print(CB_URI)
    
	for i in range(0, len(list_dicts)):
		try:
			existing_data = check_existing_data_id(CB_URI, service_name, list_dicts[i]["id"])
			if existing_data.status_code == 404 and existing_data.json()["description"]=='The requested entity has not been found. Check type and id':
				response = import_data(headers, list_dicts[i])
				if response.status_code < 200 or response.status_code >= 300:
					raise Exception(response.content)
                        
				if notify_elastic:
					response_subs = create_subscription(service_name, headers, subscription_json_elastic)
					if response_subs.status_code < 200 or response_subs.status_code >=300:
						raise Exception(response_subs.content)
                            
				if notify_api:
					response_subs = create_subscription(service_name, headers, subscription_json_api)
					if response_subs.status_code < 200 or response_subs.status_code >=300:
						raise Exception(response_subs.content)
                        
			elif existing_data.status_code == 200 and len(existing_data.json()) >= 1:
				response = update_data(service_name, headers, list_dicts[i])
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
