from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
import json

import requests

import config.config as cnf
config = cnf.Config()

import data_formatter.data_formatter as formatter
import connectors.orion_connector_ld as orion
import core.silvan_classes_ld as classes
import core.airquality_observed_weather_station as aqows
import connectors.mysql_connector as mysql
import rule_engine.rule_engine as rule_engine 
import utils.generate_information as generate

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})
 
#ORION
CB_URI_LD = config.context_broker_uri_ld
SUB_URI_LD = config.subscription_uri_ld
CB_TYPES = config.context_broker_types
AQO_WS_SERVICE = config.air_quality_observed_weather_station

ENTITY_TYPES = config.entity_types
RULE_TABLE = config.mysql_alert_table

LIST_SAVE_CHARACTERISTICS = config.list_save_characteristics
LIST_QUEUE_WEATHER_STATION = []

#This API method check the health of the API
class Health(Resource):
    def get(self):
        return {"Status":"OK"}, 200

#This method received the notification of all dat from orion and it executes the rule engine
class Notifications(Resource):
	def post(self):
		try:
			#Get data from request received
			post_json_received  = request.get_json()
			service_name = request.headers["fiware-service"]
			dict_data = post_json_received["data"][0]
    
			#process received data
			list_attributes = formatter.parse_received_data_rule_engine()
			list_data_rule_engine = formatter.data_to_rule_engine(service_name, dict_data, list_attributes)
			
			#Load the rules in mysql
			list_rules = rule_engine.load_rules()
			
			#For every rule to be analyzed is processed into rule engine
			for data_rule in list_data_rule_engine:
				print(data_rule)
				rule_engine.evaluate_rules(service_name, list_rules, data_rule)
            
			return {"Status":"OK"}, 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class Categories(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT category.value FROM category "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'} 

		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class SubCategories(Resource):
	def get(self, category):
		try:
			mydb = mysql.connect()
			query_cat_id = "SELECT category.id FROM category WHERE category.value = '{0}'".format(category)
			query_cat_result = mysql.select_query(mydb, query_cat_id)
			single_value = query_cat_result[0][0]
			query = "SELECT subcategory.value FROM relational JOIN subcategory ON relational.id_subcategory = subcategory.id WHERE relational.id_category = {0}".format(single_value)
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response, {'Access-Control-Allow-Origin': '*'}

class Severity(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT severity.value FROM severity "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class RuleEngine(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format("silvan",RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)
			column_list = formatter.single_value_tuple_list_to_list(column_query)

			rule_query = "SELECT * FROM rules"#.format("rules")
			rule_query_result = mysql.select_query(mydb, rule_query)

			response = formatter.create_rule_json(rule_query_result, column_list)

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def delete(self, id):
		try:
			mydb = mysql.connect()
			service_subs_query = "SELECT service_name, subscription_id FROM {0} WHERE id = {1}".format(RULE_TABLE, id)
			service_subs = mysql.select_query(mydb, service_subs_query)
			query = "DELETE FROM {0} WHERE id = {1}".format(RULE_TABLE,id)
			response = mysql.delete_query(mydb, query)

			delete_header = {
								'fiware-service': service_subs[0][0],
								'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
							}

			orion.request_delete_data(SUB_URI_LD, delete_header, service_subs[0][1])
			#Delete from orion

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def post(self):
		try:
			post_json_received = request.get_json()
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format("silvan", RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)

			for rule in post_json_received:
				headers = {
							'fiware-service': rule["service_name"],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}
				response = ""
				bool_update = False
				request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
				if type(request_json) is dict:
					error_message = 'The service does not exists'
					raise Exception(error_message)
				rule["entity_type"] = ENTITY_TYPES[rule["service_name"]]
				if rule["id"] != "":
					try:
						#In case we need to delete subs and service changed
						query_service = "SELECT service_name FROM rules WHERE id = {0}".format(rule["id"])
						service_result = mysql.select_query(mydb, query_service)
						delete_header = {
							'fiware-service': service_result[0][0],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}

						rule_json_values = formatter.get_rule_values_from_json(rule)
						query_set = formatter.get_columns_string_for_update(column_query)
						query_set = query_set % rule_json_values
						query_set = query_set.rstrip(',')
						query = "UPDATE {0} SET {1} WHERE id={2}".format(RULE_TABLE, query_set, rule["id"])
						query_result = mysql.update_query(mydb,query)
						if query_result[0] != 0:
							
							#DELETE SUBS
							orion.request_delete_data(SUB_URI_LD, delete_header, rule["subscription_id"])

							subs_json = formatter.create_subscription_json(rule)

							response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
							bool_update = True
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
				else:
					try:
						#POST TO ORION
						subs_json = formatter.create_subscription_json(rule)
						response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
						
				if response != "" and response.status_code >= 200 and response.status_code < 300:
					subscription_id = ''
					check_subscription_content = orion.check_existing_sub(SUB_URI_LD, headers).json()
					
					if len(check_subscription_content) > 0:
						for i in range(len(check_subscription_content)):
							if subs_json["description"] == check_subscription_content[i]["description"]:
								subscription_id = check_subscription_content[i]["id"]
								break
								
					if subscription_id == '':
						error_message = 'Could not locate the id of the subscription'
						raise Exception(error_message)
					else:
						if bool_update:
							rule["subscription_id"]=subscription_id
							query = "UPDATE {0} SET subscription_id='{1}' WHERE id = {2}".format(RULE_TABLE, subscription_id, rule["id"])					
							response = mysql.update_query(mydb, query)
						else:
							rule["subscription_id"]=subscription_id		
							rule_json_values = formatter.get_rule_values_from_json(rule)
							column_list = []
							for column in column_query:
								column_list.append(column[0])
							column_tuple = tuple(column_list[1:])
							query = "INSERT INTO {0} {1} VALUES %s".format(RULE_TABLE, str(column_tuple).replace("'",""))					
							query = query % str(rule_json_values)
							response = mysql.insert_query(mydb, query)
			return 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class Attributes(Resource):
	def get(self, service):
		try:
			headers = {'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' , 'fiware-service': service}
			request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
			if type(request_json) is dict:
				error_message = 'The service does not exists, could not load attributes'
				raise Exception(error_message)
			else:
				response = request_json[0]["attributeNames"]
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class WeatherStation(Resource):
	def post(self):
		try:
			received_dict_data = {}
			received_data = request.get_data()
			string_now_tz, datetime_now_no_micro = generate.datetime_time_tz()
			print("Message received: {0} // Data: {1}".format(string_now_tz, received_data))  # Print a received msg

			encoding = 'utf-8'
			str_received_data = received_data.decode(encoding)

			if str_received_data.startswith('[') and str_received_data.endswith(']'):
				str_dict = str_received_data[1:-1]
				received_dict_data = json.loads(str_dict)

			#PARSE RECEIVED DATA ITEM
			dict_data = formatter.format_weather_station(received_dict_data)
			print(dict_data)

			aqows.execute_airquality_observed_weather_station(AQO_WS_SERVICE, dict_data["id"], dict_data["dateObserved"], dict_data)

			return 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

class User(Resource):
	def post(self):
		try:
			post_json_received = request.get_json()
			if post_json_received['register']:
				response, code = formatter.register_user(post_json_received)
			else:
				response, code = formatter.login_user(post_json_received)
			return response, code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500		
	def delete(self,id):
		try:
			# post_json_received = request.get_json()
			response, code = formatter.delete_user(id)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500
	def put(self):
		try:
			post_json_received = request.get_json()
			response, code = formatter.update_user(post_json_received)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

api.add_resource(Health, "/health")
api.add_resource(Notifications, "/notifications")
api.add_resource(Categories, "/categories")
api.add_resource(SubCategories, "/subcategories/<string:category>")
api.add_resource(Severity, "/severity")
api.add_resource(RuleEngine, "/rule-engine", "/rule-engine/<id>")
api.add_resource(Attributes, "/attributes/<string:service>")
api.add_resource(WeatherStation, "/weather-station")
api.add_resource(User, "/user")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) #use_reloader=False this can be removed 
